Title: A Job Queue in BASH
Author: Tim Henderson
Date: 2017-02-11
Category: Blog


A Job Queue is typically a first in first out queue of "work items" or "jobs" to
be processed. Ideally, a good job queue should support multiple workers (also
called readers) so multiple jobs can be processed at one time. For production
systems and clusters there are many robust options availble. Sometimes you need
a job queue for a local system but cannot install (or do not want to install)
one of the many networked job queues. But, if you are running Linux you probably
have GNU BASH installed which can be used to create a relatively simple and
robust job queue.

Below is an example BASH Job Queue made with `fifo`s and `flock`s. A `fifo` is a
first in first out UNIX pipe ([see `man
fifo`](https://linux.die.net/man/4/fifo)). A `flock` ([see `man
flock`](https://linux.die.net/man/1/flock)) is a "file lock" which lets the
queue support multiple readers.  This queue may or may not work for other shells
as it relies on the BASH [built in
`read`](http://tldp.org/LDP/Bash-Beginners-Guide/html/sect\_08\_02.html). You
will need to consult the man pages for your shell to determine if this will work
for you.

```bash
#!/usr/bin/env bash

## this is the "job" function which is does whatever work
## the queue workers are supposed to be doing
job() {
  i=$1
  work=$2
  ## run the work ....
}

# make the files
START=$(mktemp -t start-XXXX)
FIFO=$(mktemp -t fifo-XXXX)
FIFO_LOCK=$(mktemp -t lock-XXXX)
START_LOCK=$(mktemp -t lock-XXXX)

## mktemp makes a regular file. Delete that an make a fifo.
rm $FIFO
mkfifo $FIFO
echo $FIFO

## create a trap to cleanup on exit if we fail in the middle.
cleanup() {
  rm $FIFO
  rm $START
  rm $FIFO_LOCK
  rm $START_LOCK
}
trap cleanup 0

## This is the worker to read from the queue.
work() {
  ID=$1
  ## first open the fifo and locks for reading.
  exec 3<$FIFO
  exec 4<$FIFO_LOCK
  exec 5<$START_LOCK

  ## signal the worker has started.
  flock 5                 # obtain the start lock
  echo $ID >> $START      # put my worker ID in the start file
  flock -u 5              # release the start lock
  exec 5<&-               # close the start lock file
  echo worker $ID started

  while true; do
    ## try to read the queue
    flock 4                      # obtain the fifo lock
    read -su 3 work_id work_item # read into work_id and work_item
    read_status=$?               # save the exit status of read
    flock -u 4                   # release the fifo lock

    ## check the line read.
    if [[ $read_status -eq 0 ]]; then
      ## If read gives an exit code of 0 the read succeeded.
      # got a work item. do the work
      echo $ID got work_id=$work_id work_item=$work_item
      ## Run the job in a subshell. That way any exit calls do not kill
      ## the worker process.
      ( job "$work_id" "$work_item" )
    else
      ## Any other exit code indicates an EOF.
      break
    fi
  done
  # clean up the fd(s)
  exec 3<&-
  exec 4<&-
  echo $ID "done working"
}

## Start the workers.
WORKERS=4
for ((i=1;i<=$WORKERS;i++)); do
  echo will start $i
  work $i &
done

## Open the fifo for writing.
exec 3>$FIFO
## Open the start lock for reading
exec 4<$START_LOCK

## Wait for the workers to start
while true; do
  flock 4
  started=$(wc -l $START | cut -d \  -f 1)
  flock -u 4
  if [[ $started -eq $WORKERS ]]; then
    break
  else
    echo waiting, started $started of $WORKERS
  fi
done
exec 4<&-

## utility function to send the jobs to the workers
send() {
  work_id=$1
  work_item=$2
  echo sending $work_id $work_item
  echo "$work_id" "$work_item" 1>&3 ## the fifo is fd 3
}

## Produce the jobs to run.
i=0
for item in {dataset-A,dataset-B,dataset-C,dataset-D}; do
  send $i $data
  i=$((i+1))
done
## close the filo
exec 3<&-
## disable the cleanup trap
trap '' 0
## It is safe to delete the files because the workers
## already opened them. Thus, only the names are going away
## the actual files will stay there until the workers
## all finish.
cleanup
## now wait for all the workers.
wait
```

#### References

- <http://wiki.osdev.org/Unix_Pipes>
- <https://beej.us/guide/bgipc/output/html/multipage/fifos.html>
- <http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_08_02.html>
- <https://linux.die.net/man/1/flock>


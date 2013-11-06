Title: Announcing swork - Simplify your Shell Configuration
Author: Tim Henderson
Date: 2011-05-18
Category: Blog

If you are like me, and if you are reading this you may very well be,
you spend an inordinate amount of time juggling inane details, like
shell environment variables, while programming. Now there is nothing
wrong with setting, exporting, and then unsetting variables, mounting
and unmounting FUSE partitions, starting routine backups, and so on but
it does get tedious after a while. Eventually, you may have written a
host of scripts to solve these various problems. Today I present
[swork](https://github.com/timtadh/swork) (or start work) a command line
utility to help manage these little one off scripts with ease.

Don't Repeat Yourself
=====================

A typical pattern seen in scripts, such as virtualenv's activate script,
is the storing of old environment variables such that the changes made
by the script can be easily undone. Every non-trivial script I write
seems to include this detail, and I am tired of it. It is boring, it is
simple, and it is abstract-able. So I have abstracted. swork frees you
from needing to write this code. When you want to go back the original
state of the shell, you simply type:

    $ swork restore

As long as you have run swork at some point in the past on the current
shell (or rather the current bash process) swork will restore
environment of the shell to the state it originally found it.

Writing Configuration Scripts
=============================

While, swork saves you the trouble of saving and restoring variables,
you still have to write the scripts to run. Fortunately, this is very
easy. You simply write a bash script (or any executable) then you add it
to the \~/.sworkrc (located conveniently in your home directory).

### Example setenv file:

    :::bash
    #!/usr/bin/env bash

    source env/bin/activate # activate a virtualenv
    export SOMEVAR="new value"
    export PATH="some/new/stuff":$PATH
    export PYTHONPATH="more/new/stuff":$PYTHONPATH

### example .sworkrc file:

    :::json
    {
        "project1" : {
            "root":"/path/to/project1/root",
            "start_cmd":"source /path/to/project1/root/then/setenv"
            "teardown_cmd":"echo 'project1 teardown'"
        },
        "project2" : {
            "root":"/path/to/project2/root",
            "start_cmd":"source /path/to/scripts/project2_setenv"
            "teardown_cmd":"echo 'project2 teardown'"
        }
    }

Wrapping Up
===========

swork makes it easy for you to manage the environment on you shell
allowing you to switch contexts with minimum fuss. It currently
implements the minimum functionality to be useful, but is just waiting
for your feature request!

check it out on github:
[https://github.com/timtadh/swork](https://github.com/timtadh/swork)


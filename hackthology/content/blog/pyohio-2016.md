Title: Managing Infrastructure with Python, Fabric and Ansible
Author: Tim Henderson
Date: 2016-08-01
Category: Blog


For [PyOhio](http://pyohio.org/) 2016 I gave a short talk on managing
infrastructure. You can watch the talk on [youtube](http://youtu.be/4qav2EuXsGU)
or look at the
[slides]({filename}/pdfs/managing-infrastructure-with-python.pdf). The talk
starts with a short poem printed below for posterity. I also created a super
simple demo which I did not have time to show. You can download a [tarball of
the demo]({filename}/tars/ops-example.tar.gz). To run the demo you are going to
need vagrant and the "hasicorp/precise64" box. No guarantees it works, I wrote
it in an hour or so to make sure everything in the presentation was sensible.

## The World is Changing

by Tim Henderson

### death of a sys-admin

One person.<br/>
Alone.<br/>
Do the many keyboards<br/>
Make the work light?<br/>

In the dead of the night,<br/>
How the flickers<br/>
Of the tubes<br/>
Shine so bright.<br/>

Two hands<br/>
Ten fingers<br/>
Typing so swift.<br/>
On keys, mechanical,<br/>
You can hear them click.<br/>

A machine.<br/>
One then another,<br/>
Fixed.<br/>
The backlog clean.<br/>

Now it is June,<br/>
An evening star in the sky.<br/>
The sys-admin feels the breeze<br/>
As seagulls fly by.<br/>

Back in the office<br/>
Are the keyboards lonely?<br/>
A customer wonders:<br/>
Why do my pages<br/>
Load slowly?<br/>

### there are too many machines

The flickering screens,<br/>
Can not keeps pace<br/>
With the whirring fans.<br/>

The blades spin<br/>
As the AC hums.<br/>
The metal racks gleam<br/>
The floor it glows.<br/>

But. Not enough,<br/>
Not enough dollars.<br/>
For too few cents,<br/>
Per page view is made.<br/>

Where is the sys-admin?<br/>
They left last May.<br/>
None to replace them,<br/>
For we couldn’t pay.<br/>

### now, we have become root

The humble programmer.<br/>
One keyboard,<br/>
One screen!<br/>

No rituals on approach.<br/>
No doors to knock.<br/>
Just expensive headphones<br/>
Fuzzing with static.<br/>

In the fields of desks<br/>
By the window so small<br/>
Sits the humble programmer<br/>
Trying to stay away<br/>
From it all.<br/>

But alas!<br/>
The servers are down.<br/>
Sys-admins?<br/>
None to be found!<br/>

To the command-line?<br/>
Neigh! <br/>
To the ansible, we pray!<br/>

Provision<br/>
Config<br/>
Deploy<br/>

The chant <br/>
Doth resound.<br/>



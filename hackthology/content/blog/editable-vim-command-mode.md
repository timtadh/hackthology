Title: Always Go To Editable Command Mode in Vim
Author: Tim Henderson
Date: 2014-06-06
Category: Blog

A useful trick in vim is an editable command mode with previous commands in the
buffer. To get to this mode go to normal mode (ie. hit ESC) and then type `q:`
this places you in editable command mode. If you always want to go to that mode
you can remap `:` with the following command:

```vim
nmap : q:i
```

Happy Hacking!


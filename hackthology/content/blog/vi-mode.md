Title: Vi Mode in Python Shell, IRB, and Elsewhere!
Author: Tim Henderson
Date: 2014-02-04
Category: Blog

Enable vi mode in irb, python shell, and other readline based systems:

    cat <<END >>~/.inputrc
    > set -o vi
    > set editing-mode vi
    > END

Now everything has vi key bindings! You are welcome.


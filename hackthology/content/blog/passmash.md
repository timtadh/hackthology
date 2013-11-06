Title: Passmash - The Site Specific Password Munger
Author: Tim Henderson
Date: 2012-01-30
Category: Blog


[Passmash](https://github.com/timtadh/passmash) is a new commandline
password munger. It has been tested to work on Linux with X and on
MacOS. It should also work on Windows.

What is a Munger?
-----------------

A munger takes a password and turns it into another password, "munging"
it. In particular `passmash` takes

-   A password (supplied interactively at the prompt)
-   A URL (or other identifier) (supplied as a command line argument)
-   A secret key (kept at \~/.ssh/passmash.key)

and returns a password. It has the advantages of a password manager
without having to worry about syncing a password database. The key file
is static, so simply keep a (possibly encrypted) backup of it. If you
loose the key file, you will not be able to recover your passwords.

Example Usage
-------------

In most circumstances you will want to use the `pm` command

    :::bash
    $ pm myurlhere.com
    Password:

This command automatically generates and copies the password to you
clipboard. On Linux it uses `xclip -selection clipboard`, on Mac OS X it
uses `pbcopy` and on Windows it uses `clip`.

If it is on another operating system (like OpenBSD) it will pretty print
the password for easy typing. eg.

    :::bash
    $ pm myurlhere.com
    ## We don't yet support OpenBSD for autoclipboard copying
    Password:

    5KrUw4pBgC89LGxggXEIFtjM41aPc+/GxH+cumCuTo4
    5KrUw - 4pBgC - 89LGx - ggXEI - FtjM4 - 1aPc+ - /GxH+ - cumCu - To4

Technical Details
-----------------

Passmash uses a SHA256 based HMAC with [key
strengthening](http://en.wikipedia.org/wiki/Key_stretching).

    :::python
    def mash(key, url, password):
        h = hmac.new(key, password, sha256)
        h.update(url)
        for i in xrange(250000):
            h.update(h.digest())
        return h.digest()

On my machine (a 2.0 Ghz Core2) it takes around 1 second to derive a
password using this function. A more secure version of the same utility
could make use of `bcrypt` or `scrypt`. However, either would add an
external dependency.

This password derivation function should provide strong defense against
an attacker who has

-   A password generated from the function (perhaps obtained from a
    hacked website).
-   The algorithm. (eg. they know you use this program to generate your
    passwords).

And optionally:

-   The key file
-   *or* the "master" password (but not both)

If your "master" password has sufficient
[entropy](http://en.wikipedia.org/wiki/Entropy_%28information_theory%29)
then your other passwords generated with the same key should be
reasonably secure against a brute force attack.

### [Happy Munging!](https://github.com/timtadh/passmash)


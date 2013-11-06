Title: How To: Write Self Updating Python Programs Using Pip and Git
Author: Tim Henderson
Date: 2011-05-23
Category: Blog

If you are a pip[^1] and virtualenv user you already know how easy it is
to install python packages. Unlike the bad old days when I started
programming in Python, 9 years ago, it is now easy to add, remove and
manage python modules. In fact we can leverage pip to create an `update`
command for a python program, for example and ease of illustration, a
shell utility.

### Table of Contents

1.  Desired Features
2.  Basic Idea
3.  Implementation

Desired Features
----------------

- Uses a server controlled by the owner (instead of the Python Package
  Index).
- Install an arbitrary version of the program.
- Defaults to updating to the newest version of the major release one
  is tracking.

I often want my programs to update themselves from a specific location.
For instance an internal server or perhaps my github account.
Fortunately pip already supports such nicities with the `-e` for the
`install` command.

Additionally, when running a generic update you often want to stay on
the same major revision and simply get the bug fixes. However, it is
important to provide the option to update to any arbitrary release
including tracking the master branch.

Basic Idea
----------

Use Pip and the `-e` option plus a base URL to automatically update your
software. eg. Have you software run pip for the user.

example command:

    pip install --upgrade --src="$HOME/.src" -e git+<URL>@<REV>#egg=PACKAGE_NAME

#### Tracking Major Versions

To track major version updates some care must be taken in setting up the
repository. I use branches instead of tags to track major releases. This
allows me to push out bug fix updates for every one tracking that
release. I tag minor releases to allow users to install a specific
version.

Branches

- master
- stable
- r0.1
- r0.2
- ...
- rN

Tags

- r0.1
- r0.1.1
- r0.1.x
- ...
- rN

#### Pip Gotcha

When checking out branches using pip you have to supply
`origin/branchname` ex:

    pip install --upgrade --src="$HOME/.src" -e git+https://github.com/user/repo.git@origin/branch#egg=PACKAGE_NAME

While when checking out a commit you should not supply origin

    pip install --upgrade --src="$HOME/.src" -e git+https://github.com/user/repo.git@COMMIT_ID#egg=PACKAGE_NAME

Why does pip work like this? Because of the commands it executes. For
the command:

    pip install --upgrade --src="$HOME/.src" -e git+https://github.com/user/repo.git@<VERSION>#egg=PACKAGE_NAME

pip runs

    git fetch -q git reset --hard -q <VERSION>

#### Store the tracked version in the source

To ensure the update command installs the correct updates I put which
release to checkout in the source code. This allows me to "release" a
version by creating a branch and then changing the RELEASE constant to
point the name of the branch.

Implementation
--------------

Note: This is example code only, you should modify for security and
stability of your enviroment.

Note: I didn't include virtualenv support in this code but it is trivial
to add.

    :::python

    from subprocess import check_call as run 
    from getopt import getopt, GetoptError 
    RELEASE = 'master' # default release 
    SRC_DIR = "$HOME/.src" # checkout directory 
    UPDATE_CMD = ( # base command 
    'pip install --src="%s" --upgrade -e ' 
    'git://github.com/timtadh/swork.git@%s#egg=swork' 
    ) 

    @command 
    def update(args): 
        try: 
            opts, args = getopt(args, 'sr:', ['sudo', 'src=', 'release=', 'commit=']) 
        except GetoptError, err: 
            log(err) 
            usage(error_codes['option']) 

        sudo = False 
        src_dir = SRC_DIR 
        release = RELEASE 
        commit = None 
        for opt, arg in opts: 
            if opt in ('-s', '--sudo'): 
                sudo = True 
            elif opt in ('-r', '--release'): 
                release = arg 
            elif opt in ('--src',): 
                src_dir = arg 
            elif opt in ('--commit',): 
                commit = arg 

        if release[0].isdigit(): ## Check if it is a version 
            release = 'r' + release 
        release = 'origin/' + release ## assume it is a branch 

        if commit is not None: ## if a commit is supplied use that 
            cmd = UPDATE_CMD % (src_dir, commit) 
        else: 
            cmd = UPDATE_CMD % (src_dir, release) 

        if sudo: 
            run('sudo %s' % cmd) 
        else: 
            run(cmd)

[^1]: [http://www.pip-installer.org/en/latest/index.html](http://www.pip-installer.org/en/latest/index.html) "A Python package installer."


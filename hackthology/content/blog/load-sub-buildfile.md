Title: How to Re-Use a Sub-Project's Buildfile in Apache Buildr
Author: Tim Henderson
Date: 2014-03-14
Category: Blog


[Apache Buildr](http://buildr.apache.org) is a nice build system for Java and
other JVM langauges. It is based on Ruby's Rake system and makes it easy to
setup a multi-project build. However, by default, there is no support for
re-using a `Buildfile` from another project.  The intreprepid hacker can fix that
problem by loading the sub-project's `Buildfile` like this:

    ::ruby

    if File::exists?('sub-project/Buildfile')
      pwd = Dir.pwd
      Dir.chdir File::join(pwd, 'sub-project')
      load "./Buildfile"
      puts project('sub-project').base_dir  ## HACK: pins the project to the
                                            ## proper directory!
      Dir.chdir pwd
    end

If you don't access `base_dir` before you reset the current working directory
then it will eventually get set to the wrong directory causing build failures.

After you have loaded the `Buildfile` you can run:

    ::bash

    $ pwd
    /path/to/project
    $ buildr help:projects
    (in /path/to/project, development)
    /path/to/project/sub-project
      main-project
      sub-project
      other-project
      another-project


All of the tasks from you sub-project should now work as expected from the
parent project. Happy Buildring!


Title: Research
Author: Tim Henderson
Date: 2013-11-05
Category: Research

My academic research is in the area of Software Engineering. Software
Engineering develops tools and processes to create higher quality software
systems. The field itself was born out of a software "crisis" in the 1960s
in the NATO defense community. In recent years, developments in program
analysis have lead to the emergence of high quality commercial static analysis
tools for widely used programming languages.

However, despite the availability of automated program verification for
interesting program properties, usage has remained restricted to specialized
domains. Most development teams today do not write formal specifications or
correctness properties for their business logic.  Instead, they rely on
testing. Unfortunately, testing is necessarily optimistic and cannot ensure a
program is bug free. Program verification, when it is used, is employed only
to check very general properties, such as the absence of buffer overflow
errors.

There are three major problems today preventing the widespread adoption of
software analysis tools for verification purposes. First, it is difficult to
write correctness properties for programs. My research in specification mining
addresses this problem by learning program correctness properties. Second,
false positive warnings from static analysis systems remain a persistent
problem. My investigations into test case generation determines the accuracy
of a static analysis warning. Finally, bug finding tools produce an abundance
of findings. Some findings are duplicates, some are false positives and some
are actual faults in the program. In order make the analyst more efficient, I
am creating a finding triage system which clusters results together affording
the analyst the ability to examine groups of findings.

I also work on a static analysis system for JVM languages called
[JavaPDG](http://selserver.case.edu:8080/javapdg/) and on related tool called
[jpdg](https://github.com/timtadh/jpdg).

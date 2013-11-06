Title: Research
Author: Tim Henderson
Date: 2013-11-05
Category: Research


My academic research in the area of Software Engineering. Software Engineering
tries to find tools and process to create higher quality software systems. The
field itself was born out of a software "crisis" in the 1960s in the NATO
defense community.

A major thrust of research in computer science from the early days of the
discipline was on *program verification*, or proving correctness properties on
programs. In the 1960's this was done manually but eventually automated methods
were developed for verifying various classes of properties. In recent years
developments in program analysis have lead to the emergence of high quality
commercial static analysis tools for widely used languages.

However, despite the availability of automated program verification for
interesting program properties usage has remained restricted to specialized
domains. Most programming teams today do not write formal specifications or
correctness properties for their business logic. They rely instead on unit and
functional level testing of this logic which is necessarily optimistic.
Verification when it is used is used to check very general properties, such as
the absence of a buffer overflow error.

My research focuses on how to address the problems with current approaches to
program analysis with:

1. Specification Inference
2. Clustering of Static Analysis Findings
3. Automatic Test Case Generation

I also work on a static analysis system for JVM languages called
[JavaPDG](http://selserver.case.edu:8080/javapdg/).

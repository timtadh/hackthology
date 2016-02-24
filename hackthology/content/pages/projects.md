Title: Projects
Author: Tim Henderson
Date: 2016-02-24
Category: Projects


I have worked on number of projects over the years. Here are some that I am
currently trying to find time to hack on.


## Data Structures

### data-structures

Golang's standard library lacks many useful and important structures. This
library attempts to fill the gap. I have implemented data-structure's as I have
needed them.

More at [hackthology.com/data-structures](http://hackthology.com/data-structures/)


### fs2 (File Structures 2)

One of my hobbies is writing database indices. This project is about exploring
memory mapped structures in the go programming language. It has a high
performance B+Tree with duplicate key support. It support variably sized keys
and values up to 2^31 - 1 bytes in length. It also includes a memory mapped
list. Finally, there is a code generator for creating wrappers around go types
solving the "no generics in go problem."

More at
[hackthology.com/fs2](http://hackthology.com/fs2/)


### File Structures

My previous work on file-structures using the read/write interface. This project
collects several file-structures I have written in Go together in one place. It
includes: BTree, B+Tree with duplicate key support, Linear Virtual Hashing, and
a Blob store.

More at
[github.com/timtadh/file-structures](https://github.com/timtadh/file-structures)


## Netgrid

Netgrid is a distributed map-reduce like computation platform. Written in Go it
supports iterative jobs which makes it more suitable for a variety of tasks. I
originally implemented it to support my research objectives in Frequent Subgraph
Mining. It is not currently open source but I am exploring the possibility.


## Programming Langauges

### TCEL

This is a simple language with a static type checker. It is a compiled or
interpreted expression oriented functional language.  It features: First class
functions, Closures, Integers, floats, strings, booleans, and Conditional
expressions.  This language is evolving fast and may have undocumented features
or bugs. It started out as an example I wrote for the compilers class I teach,
EECS 337 Compiler Design, at Case Western Reserve University.

More at [github.com/timtadh/tcel/](https://github.com/timtadh/tcel/)


### Slang

Slang is a programming language which I have been developing on to help me
teach the principles of compilation and program analysis. It is currently in an
unfinished state as it lacks many features I would like it to have the in the
future. However, it does demonstrate lexing, parsing, intermediate code
generation, control flow analysis, structural data flow analysis, and machine
code generation.

More at [github.com/timtadh/slang](https://github.com/timtadh/slang)


### PyFlowr

A query language for Python Object Hierarchies. It is loosely inspired by
XQuery/XPath and OQL. It allows schema-less queries of complex Python
data structures. It is a fun little query language with an easily extensible
parser for adding more syntax.

More at [github.com/timtadh/pyflwor](http://github.com/timtadh/pyflwor)


## Tree Edit Distance

I have a great implementation of exact tree edit distance using the
Zhang-Shasha algorithm. People seem to email me fairly regularly about it so
someone out there is finding it useful.

More at
[github.com/timtadh/zhang-shasha](https://github.com/timtadh/zhang-shasha)


## Command Line Utilities

1. [swork](https://github.com/timtadh/swork) A shell environment manager. I use
   this to help manage all my projects.
2. [optutils](https://github.com/timtadh/optutils) A python library to help me
   write command line utilities. I write a lot of these.
3. [passmash](https://github.com/timtadh/passmash) A site specific password
   munger.
4. Lots of random utilities here and there.

<br>


## More on the github

I have a lot more projects over on my github. These are just some of the
highlights. Beyond the github, there are my
[research projects]({filename}/pages/research.md)


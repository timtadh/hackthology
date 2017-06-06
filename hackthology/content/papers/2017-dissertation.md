Title: Frequent Subgraph Analysis and its Software Engineering Applications
Author: <a href="http://hackthology.com">Tim Henderson</a>
Citation: <strong>Tim A. D. Henderson</strong>. <i>Frequent Subgraph Analysis and its Software Engineering Applications</i>. Case Western Reserve University. Doctoral Dissertation. 2017.
CiteAuthor: <strong>Tim A. D. Henderson</strong>.
Publication: Case Western Reserve University. Doctoral Dissertation. 2017
Date: 2017-08-18
Category: Paper


**Tim A. D. Henderson**. *Frequent Subgraph Analysis and its Software Engineering Applications*.
[Case Western Reserve University](http://case.edu/). Doctoral Dissertation 2017.
<br/>
[PDF]({filename}/pdfs/dissertation.pdf).
[WEB]({filename}/papers/2017-dissertation.md).

#### Abstract

Frequent subgraph analysis is a class of techniques and algorithms to find
repeated sub-structures in graphs known as frequent subgraphs or graph
patterns. In the field of Software Engineering, graph pattern discovery can
help detect semantic code duplication, locate the root cause of bugs, infer
program specifications, and even recommend intelligent auto-complete
suggestions.  Outside of Software Engineering, discovering graph patterns has
enabled important applications in personalized medicine, computer aided drug
design, computer vision, and multimedia.

As promising as much of the previous work in areas such as semantic code
duplication detection has been, finding all of the patterns in graphs of a
large program's code has previously proven intractable.  Part of what makes
discovering all graphs patterns in a graph of a large program difficult is the
very large number of frequent subgraphs contained in graphs of large programs.
Another impediment arises when graphs contain frequent patterns with many
automorphisms and overlapping embeddings. Such patterns are pathologically
difficult to mine and are found in real programs.

I present a family of algorithms and techniques for frequent subgraph analysis
with two specific aims. One, address pathological structures. Two, enable
important software engineering applications such as code clone detection and
fault localization without analyzing all frequent subgraphs. The first aim is
addressed by novel optimizations making the system faster and more scalable
than previously published work on both program graphs and other difficult to
mine graphs. The second aim is addressed by new algorithms for sampling,
ranking, and grouping frequent patterns.  Experiments and theoretical results
show the tractability of these new techniques.

The power of frequent subgraph mining in Software Engineering is demonstrated
with studies on duplicate code (code clone) identification and fault
localization.  Identifying code clones from program dependence graphs allows
the identification of potential semantic clones. The proposed sampling
techniques enable tractable dependence clone identification and analysis.
Fault localization identifies potential locations for the root cause of bugs
in programs. Frequent substructures in dynamic program behavior graphs to
identify suspect behaviors which are further isolated with fully automatic
test case minimization and generation.

## Introduction


*Frequent subgraph analysis* (FSA) is a family of techniques to discover
recurring subgraphs in graph databases. The databases can either be composed of
many individual graphs or a single large connected graph. This dissertation
discusses my contributions to frequent subgraph analysis and applies the
technique to address two pressing problems in software engineering: code clone
detection and automatic fault localization.

The work on frequent subgraph analysis was motivated by the software engineering
problems. Large programs are composed of repeated patterns arising organically
through the process of program construction. Some regions of programs are
duplicated (intentionally or unintentionally). The duplicated regions are
referred to as *code clones* (or just *clones*). Other regions are
similar to each other because they perform similar tasks or share development
histories.

Code clones may arise from programmers copying and pasting code, from
limitations of a programming language, from using certain APIs, from following
coding conventions, or from a variety of other causes.  Whatever their causes,
the existing clones in a code base need to be managed. When a programmer
modifies a region of code that is cloned in another location in the program
they should make an active decision whether or not to modify the other location.
Clearly, such decisions can only be made if the programmer is aware of the other
location.

One type of duplication which is particularly difficult to detect is so called
*Type-4 clones* or *semantic clones*. Semantic clones are semantically
equivalent regions of code which may or may not be textually similar.
Differences could be small changes such as different variable names or large
changes such as a different algorithms which perform the same function. In
general identifying semantically equivalent regions is undecidable as a
reduction from the halting problem.

Frequent subgraph analysis (FSA) can be used to identify some *Type-4* clones
(as well as easier to identify clone classes). I use FSA to analyze a graphical
representation of the program called the *Program Dependence Graph* (PDG)
{[Ferrante 1987](https://doi.org/10.1145/24039.24041)}. Dependence graphs strip
away syntactic information and focus on the semantic relationships between
operations.  Non-semantic re-orderings of operations in a program do not effect
the structure of its dependence graph {[Horwitz
1990](https://doi.org/10.1145/93548.93574), [Podgurski
1989](https://doi.org/10.1145/75309.75328), [Podgurski
1990](https://doi.org/10.1109/32.58784)}. Since PDGs are not sensitive to
unimportant syntactic changes some of the *Type-4* clones in a program may
be identified with FSA.

The other motivating application I applied FSA to is automatic fault
localization.  When programs have faults, defects, or bugs it is often time
consuming and sometimes difficult to find the cause of the bug. To address this
the software engineering community has been working on a variety of techniques
for *automatic fault localization*.  The family of statistical fault
localization techniques analyzes the behavior of the program when the faults
manifest and when they do not. These techniques then identify statistical
associations between execution of particular program elements and the occurrence
of program failures.

While statistical measures can identify suspicious elements of a program they
are blind to the relationships between the elements. If program behavior is
modeled through *Dynamic Control Flow Graphs*, then execution relationships
between operations can be analyzed using FSA to identify suspicious
interactions. These suspicious interactions represent larger *behaviors* of
the program which are statistically associated with program failure. The
behaviors serve as a context of interacting suspicious program elements which
potentially makes it easier for programmers to comprehend localization results.

Much of the previous work in frequent subgraph analysis has focused on finding
all of the frequent subgraphs in a graph database (called *frequent subgraph
mining* {[Inokuchi 2000](https://dx.doi.org/10.1007/3-540-45372-5_2)}). I
have shown that finding all of the frequent subgraphs in a database of graphs is
not an efficient or effective way to either detect code clones or automatically
localize faults. Program dependence graphs of large programs have huge numbers
of recurring subgraphs.  Experiments on a number of open source projects (see
Chapter 4) showed that moderately sized Java programs (~70 KLOC) have more than
a hundred of million subgraphs that recur five or more times. Mining all
recurring subgraphs is an impractical way to either identify code clones or
localize faults.

Furthermore, it turns out that program dependence graphs are particularly
difficult to analyze for recurring subgraphs. These graphs often have certain
structures which contain many *automorphisms*. A structure with an automorphism
can be rotated upon itself. Each rotation appears to be a recurrence to
traditional frequent subgraph mining algorithms. However, because it is merely a
rotation, humans (e.g. programmers) do not perceive these rotations as instances
of duplication.

To enable scalable frequent subgraph analysis of large programs new techniques
were needed. I developed novel optimizations for mining frequent subgraphs and
created a state of the art miner (REGRAX) for connected graphs (Chapter 3).  To
detect code clones from program dependence graphs, I developed an algorithm
(GRAPLE) to collect a representative sample of recurring subgraphs (Chapter 4).
Finally, a new algorithm (SWRW) was created for localizing faults from dynamic
control flow graphs, which outperforms previous algorithms (Chapter 6).

REGRAX contains low level optimizations to the process of identifying frequent
subgraphs. Chapter 2 provides the necessary background on frequent subgraph
mining for understanding these optimizations. An extensive empirical study was
conducted on REGRAX to quantify the effect of each of the new optimizations on
databases from the SUBDUE corpus {[Cook
1994](https://dl.acm.org/citation.cfm?id=1618595.1618605)}, on program
dependence graphs, and on random graphs.

GRAPLE is a new algorithm to sample a representative set of frequent subgraphs
and estimate statistics characterizing properties of the set of all frequent
subgraphs. The sampling algorithm uses the theory of absorbing Markov chains to
model the process of extracting recurring subgraphs from a large connected
graph. By sampling a representative set of recurring subgraphs GRAPLE is able to
conduct frequent subgraph analysis on large programs which normally would not be
amenable to such analysis.

One of the questions in code clone detection is: "are code clones detected from
program dependence graphs understandable to programmers?" GRAPLE was used to
answer this question, as it not only collects a sample of frequent subgraphs but
allows researchers to estimate the prevalence of features across the entire
population of frequent subgraphs (including those which were not sampled).
Chapter 4 details a case study which was conducted at a software company to
determine whether their programmers could make use of code clones detected from
program dependence graphs. The study would not have been possible without the
estimation framework in GRAPLE, as the software contained too many code clones
to be reviewed in the allocated budget.

To apply frequent subgraph analysis to automatic fault localization, a new
algorithm named Score Weighted Random Walks (SWRW) was developed. SWRW samples
discriminative, suspicious, or significant subgraphs from a database of graphs.
The database is split into multiple classes where some graphs are labeled
"positive" and others "negative." In fault localization the "positive" graphs
were those dynamic control flow graphs collected from program executions which
exhibited a failure of some type. The "negative" graphs are from executions
which did not fail.

SWRW, like GRAPLE, models the problem using the theory of absorbing Markov
chains. Unlike GRAPLE, it uses an *objective function* (drawn from the
statistical fault localization literature {[Lucia
2014](https://dx.doi.org/10.1002/smr.1616)}) to guide the sampling process. In
comparison to previous work in fault localization using graph mining, a much
wider variety of objective functions can applied. This allows for functions
better suited to statistical fault localization to be used as the objective
function. SWRW outperforms previous approaches which used discriminative mining
to localize faults in terms of fault localization accuracy.

#### Summary

This dissertation makes important and novel contributions to frequent subgraph
analysis which enable scalable semantic code clone detection and behavioral
fault localization. These advances can help programmers maintain their software
more efficiently leading to more stable and secure software for everyone. The
software engineering advances are built on new frequent subgraph analysis
algorithms. The new algorithms improve code clone detection time, fault
localization latency and accuracy, and enable analysis of larger and more
complex programs.

[Read the full dissertation]({filename}/pdfs/dissertation.pdf).


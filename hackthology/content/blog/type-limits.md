Title: The Limits of Type Systems
Author: Tim Henderson
Date: 2013-09-03
Category: Blog

[E.W.Dijkstra Archive: The Humble Programmer (EWD 340)](http://www.cs.utexas.edu/users/EWD/transcriptions/EWD03xx/EWD340.html)

> Argument three is based on the constructive approach to the problem of program
> correctness. Today a usual technique is to make a program and then to test it.
> But: program testing can be a very effective way to show the presence of bugs,
> but is hopelessly inadequate for showing their absence. The only effective way
> to raise the confidence level of a program significantly is to give a
> convincing proof of its correctness.  But one should not first make the
> program and then prove its correctness, because then the requirement of
> providing the proof would only increase the poor programmer’s burden. On the
> contrary: the programmer should let correctness proof and program grow hand in
> hand.  Argument three is essentially based on the following observation. If
> one first asks oneself what the structure of a convincing proof would be and,
> having found this, then constructs a program satisfying this proof’s
> requirements, then these correctness concerns turn out to be a very effective
> heuristic guidance. By definition this approach is only applicable when we
> restrict ourselves to intellectually manageable programs, but it provides us
> with effective means for finding a satisfactory one among these.

Essentially what Dijkstra is advocating here is what the approach the most
advanced type theories are striving for. They aim to allow the programmer to
specify in the type system (a proof system) important semantic invariants of the
application. The type system is constructed in such a way the program is only
well typed if the specified invariants hold. The hope of the type theorists is
that with a sufficiently powerful type (proof) system most if the not all
properties one cares to prove are in fact provable (for certain programs).

The difficulty for the practicing programmer is most type systems are not nearly
powerful enough to specify properties which are actually interesting.  This
leaves the programmer doing essentially the proof equivalent of book keeping
with no benefit. I should distinguish here between dynamically checked types
(properties) and statically checked types.  Dynamically checked, that is at run
time, are always enormously helpful to the programmer because they provide
runtime safety. However, statically checked types can be overly burdensome if
they require lots of book keeping without sufficiently powerful proofs.

Unfortunately, for a wide variety of statically checked programming languages
the available proofs are uninteresting and the burden is high.  This is the
challenge to the Dijkstra-ist.


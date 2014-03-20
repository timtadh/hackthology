Title: Private Methods and Functions Should be Tested
Author: Tim Henderson
Date: 2014-03-20
Category: Blog


Recently I became engaged in a debate around whether or not private methods
should usually have unit tests. Rather than writing up a quick off hand reply to
the question I decided to write up a detailed stance on the matter.


# Testing Theory

Why is software tested? It is tested for two reasons:

1. To reveal defects and deviations from a **specification**. Does the software
   function properly? This is called Software **Verification**.
2. To ensure the software meets the needs of the end user. Are we meeting the
   needs of our users? This is called Software **Validation**.

To validate software, engineers employ a variety of techniques such as user
testing, case studies on user needs, surveys, runtime observations, alpha/beta
testing, and acceptance testing. These techniques not only look for bugs and
defects in the software but also try and understand whether it effectively
solves problems for the user. This process informs the iterative development of
the software and can lead to changes in functional requirements.

In order to verify the correct functioning of software, engineers check the
software to ensure it satisfies the specification. A specification states how
the software should function. Unfortunately, a complete and accurate
specification never exists. Engineer carefully determine what to check and based
on their estimations on the accuracy and completeness of a specification.

The modern engineer has many techniques that can be used to verify software.
Broadly they fit into two categories: testing and program analysis. Program
analysis uses various techniques to prove specific properties about a program.
For exampled, in statically type checked languages (such as Java or Haskell) the
type checker proves the absence of type errors. I will not discuss these
techniques in this essay as there availability varies by language and
environment.

Testing runs a program with specified inputs and checks that the result is
correct. It is the primary way software is verified. While the advanced program
analysis techniques are neat almost all software should be rigorously tested.
Well what does "rigorously" mean. If software is rigorously tested does that then
mean: the software will be dependable (and/or correct)?

Unfortunately, no matter what techniques are used to test software, tests can
never ensure software is correct. However, it can give the development team
confidence (with the right techniques) in the dependability of the software.


## Rigorous Testing

What are some suitable criteria that can be used to determine if a test suite is
adequate for verifying the software? Designing a adequate testing criteria has
many pitfalls. Consider the following requirement:

> A test suite must cover (execute) every statement in the program.

This requirement only looks useful. For instance, it doesn't say that the
individual tests should check each component functioned properly. Rather, it
only says that the component was executed.

The abstract requirements I often use for tests at the unit (function or method
level) is:

1. A method should checked that it behaves properly in both nominal and
   exceptional cases.
2. If a model of how the method should function is available it should be
   checked against that model.
3. Path coverage, how many control flow paths through a method are taken, can be
   used a heuristic to guide the tester towards methods which may require
   further testing.
4. When required methods should be checked for security and language level
   faults such as: buffer overflows, SQL injection errors, cross site scripting
   errors, etc...
5. Public methods should be checked against all elements of their specified API
   contract.
6. Unit tests should assume the methods used by the method under test behave
   correctly if each of those methods has good tests.

These requirements will not ensure that a program has no bugs. However, it gives
confidence that all methods in the program work properly because it forces the
programmer to think about how each method should work. Not only think about it,
but think how to test it, how to to check every control flow path, how to check
all parts of the specified API. By engaging the programmer in this way bugs can
be caught not only in the method but in the specification for the method.


# Should Private Methods be Tested?

According to my theory on testing methods at the unit level *private methods
should be tested*. My theory has the inductive hypothesis that methods used by a
method under test can only be assumed to work if each of those methods has good
tests.  If that hypothesis is not met, one loses confidence in the test suite.
Furthermore, the programmer is no longer forced to think critically about the
function of every method.

I have received some important counter points to this point of view. I am going
to address those individually.


### If private methods are tested then how can we locate dead code?

One can solve this problem in several ways. My recommendation is to mark tests
for private methods in such a way that they can be excluded from test suite
runs.


### Tests on private methods make the test suite brittle

Here the tester needs to use their best judgement on whether the specification
on some area is in too much flux to formalize a test. They should also use there
judgement on what to check. If the output format is likely to change rather than
checking it precises can it be checked to ensure it meets certain properties?

#### negative example

This test is very brittle. Slight changes to the code can easily break by
re-ordering fields or adding and removing them.

    ::java

    String E = "edge {\"src\":0,\"targ\":1,\"label\":\"cfg\",\"src_label\":\"a\",\"targ_label\":\"b\"}";

    @Test
    public void Edge() {
        Graph g = new Graph();
        int a = g.addNode("a", "x.y", "c", "m", "t", 1, -1, 2, -1);
        int b = g.addNode("b", "x.y", "c", "m", "t", 1, -1, 2, -1);
        int c = g.addNode("c", "x.y", "c", "m", "t", 1, -1, 2, -1);
        Edge e = new Edge(a, b, "cfg", g);
        assertThat(e.Serialize(), is(E));
    }

#### positive example

This test is better because it looks for just the properties of the
serialization which are important (the source, target, and edge label are set
correctly).

    ::java

    @Test
    public void Edge() {
        Graph g = new Graph();
        int a = g.addNode("a", "x.y", "c", "m", "t", 1, -1, 2, -1);
        int b = g.addNode("b", "x.y", "c", "m", "t", 1, -1, 2, -1);
        int c = g.addNode("c", "x.y", "c", "m", "t", 1, -1, 2, -1);
        Edge e = new Edge(a, b, "cfg", g);
        String E = e.Serialize();
        assertThat(E.contains("\"src\":0"), is(true));
        assertThat(E.contains("\"targ\":1"), is(true));
        assertThat(E.contains("\"label\":\"cfg\""), is(true));
    }


### Testing private methods pulls away from BDD

BDD (Behavior Driven Development), tries to help projects stay on target by
keeping them aligned to user needs.  In this sense it is a validation technique
which integrates validation into the development process. However, high level
behavioural tests rely on the software underneath the high level functionality
functioning properly. Verification of that functionality is needed regardless of
its relationship to customer requirements.

For instance a customer would never specify that items from a sorted array
should be retrieved with a binary search. But, if a programmer needs to retrieve
an item from a sorted array and uses a binary search that search must work in
order to meet whatever functional requirement the programmer is implementing.
Furthermore, security requirements are typically not functional or behavioural
but none the less they must be checked.

Testing private methods and methods which implement basic functionality does not
conflict with BDD it enables it.


### Testing private methods is time consuming

It is often difficult to know when the proper time is to write a test for a
method. TDD (Test Driven Development) advocates for writing tests before a
method is written. The TDD method can be useful in some circumstances but I
would not advocate for universal application of it. I will give the advice that
it is easier to write a test for a method at the time of development rather than
later on. If the method needs to be modified in some way later on (especially in
a way that does not break existing functionality) then the tests serve as a
"safety belt" when extending it. If the change to the method changes existing
functionality then the old tests can be safely deleted (but new tests should
likely be created).

I don't think testing private methods is in particular time consuming. Rather,
program verification and validation is in general time consuming. However,
performing these activities is what separates high quality software from low
quality software.


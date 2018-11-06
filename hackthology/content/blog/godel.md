Title: Gödel's Incompleteness Theorem Does Have Philosophical Implications
Author: Tim Henderson
Date: 2018-11-05
Category: Blog

In 1931 Kurt Gödel published a paper in German that has continued to
reverberate through the scientific community:

> K. Gödel, "On Formally Undecidable Propositions of Principia Mathematica and
> Related Systems," Monatshefte für Math. und Phys., vol. 38, pp. 173–198, Jan.
> 1931.
>
> Translation: [doi](https://doi.org/10.1111/j.1468-0149.1963.tb00774.x)
> [pdf](http://hope.simons-rock.edu/~pshields/cs/cmpt300/easiergoedel.pdf)

This paper sets clear limits on what is "rationally computable" and what that
means. There have been those that argue this work has little to no philosophical
significance. I believe it does have philosophical significance as I explain at
the end.

## First some definitions.

By rational I mean reasoning (that is thinking) through the means of logical
inference without outside facts or "intuition." Such a manner of thought would
have been foreign to most in 1931 (except those pursuing [*formal*
mathematics](https://en.wikipedia.org/wiki/Principia_Mathematica)). Today it has
become explicit through our interaction with computers -- who can only reason
rationally.\*

By computable I mean a question (such as does 2 + 2 = 4?) can be provably
answered in a finite number of discrete steps in the logical system of choice.
By logical system of choice I mean the allowed methods of reasoning and the set
of base "facts" (called axioms). For example:

> Facts:
>
> 1. 0 == 0
> 2. 0 + 1 != 0
> 3. x + 1 == y + 1 ---> x == y
> 4. x + (y + 1) == (x + y) + 1
> 5. 0 + x == x
>
> allowed deductions:
>
> if A is true and A implies B then B is true
>
> 2 + 2 == 4?
>
> - 2 ==> 0 + 1 + 1 ("de-sugaring the natural number")
> - 4 ==> 0 + 1 + 1 + 1 + 1 ("de-sugaring the natural number")
> - (0 + 1 + 1) + (0 + 1 + 1) == (0 + 1 + 1 + 1 + 1) ("restatement of lemma")
> - ((0 + 1 + 1) + (0 + 1)) + 1 (rule 4)
> - ((0 + 1 + 1) + (0)) + 1 + 1 (rule 4)
> - (0 + 1 + 1) + 1 + 1 (rule 5)
> - (0 + 1) + 1 + 1 + 1 (rule 4)
> - 0 + 1 + 1 + 1 + 1 (rule 4)
> - (0 + 1 + 1 + 1 + 1) == (0 + 1 + 1 + 1 + 1) ("restatement of lemma using previous step")
> - (0 + 1 + 1 + 1) == (0 + 1 + 1 + 1) (rule 3)
> - (0 + 1 + 1) == (0 + 1 + 1) (rule 3)
> - (0 + 1) == (0 + 1) (rule 3)
> - 0 == 0 (rule 3)
> - true (rule 1)

## What did Gödel prove?

In laymen's terms, Gödel proved that any logical system with finite "axioms"
(read: starting facts) could not be both "complete" and "consistent." By
complete logicians mean the system can answer any question. By consistent
logicians mean the system never gives two answers (both true and false) to a
single question.\*\*

## Why does this matter?

It matters because, like [the Halting
Theorem](https://en.wikipedia.org/wiki/Halting_problem), the Incompleteness
Theorem shows there are computations (answers to logical questions) which cannot
be decided by mechanistic means -- that is they are *uncomputable*.

Some say that these results are both ordinary and without profound implications.
For instance consider this comment from [an interview with Tim
Maudlin](https://blogs.scientificamerican.com/cross-check/philosophy-has-made-plenty-of-progress/):

> > Does Gödel's incompleteness theorem have implications beyond mathematics? Is
> > it a worm in the apple of rationality? 
> 
> No. Absolutely no one should have ever been surprised that mathematical truth
> cannot be equated with theoremhood in some finite axiomatic system. An
> infinitude of mathematical truths are uninteresting trivia, with no obvious
> route to being proved. Example: let's say that the decimal expressions of the
> square root of 17 and pi to the 27th power “match” just in case either they
> have the same digit in the tenths place, or the same two digits in the next
> two places, or the same three digits in the next three places, etc. If we
> treat these decimal expressions as essentially random sequences of digits,
> then the a priori chance that these two numbers match is one out of nine.
> 
> Now: how do we tell if they match or not? Well, we can just calculate out the
> sequences of digits and check. And if they match we will eventually find the
> match and prove that they match. But what if, as is likely, they don't match?
> No amount of just grinding out the digits and checking will ever prove it:
> there are always more digits to check. And I see zero prospect of any other
> way to prove that they don't match. So if they don't match, that is an
> unprovable mathematical fact. It is also a very, very, very uninteresting one.
> All Gödel did was find a clever way to construct a provably unprovable
> mathematical fact, given any consistent and finite set of axioms to work with.
> The work is clever but in no way profound. It should have come as no surprise
> at all.

However, it is (particularly in the historical context) profound to be able to
*prove* that a particular question has no *computable* answer. The answer may be
out there but if we (humans) discover it will be by luck not will. There are
limits and important ones about what we as humans and machines can and cannot
prove and know. From a philosophical point of view this argues for the concept
of *mystery*. That there are and will be those areas of truth for which we can
grasp but never hold, for we reach for but do not touch. Thus, we must strive on
in our collective quest to know who and what we. All the while *knowing* there are
parts of the world and ourselves for which there is no final a HA!

----

\* - Of course those who work on stochastic algorithms and machine learning may
quibble on this point. However, I believe even those algorithms and systems --
and indeed our brains at a fundamental level -- reason rationally. Indeed this
is *why* Gödel's theorem is of such interest.

\*\* - This and this article necessarily simplifies and collapses much of the
nuance in the work. For instance there are actually 2 incompleteness theorems
that work in concert with each other. I am interested in this article with the
effect of the theorems not in giving a rigorous introduction to them.

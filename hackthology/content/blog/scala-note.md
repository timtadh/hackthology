Title: Scala Notes
Author: Tim Henderson
Date: 2014-08-18
Category: Blog

My notes as I relearn Scala. I am reading through [Programming in Scala (2nd
ed.)](http://www.worldcat.org/title/programming-in-scala/oclc/731510960)



# Quibble with the Functional List

> \> *from page 43*
> ### Why not append to lists?
>
> Class `List` does offer an append operation -- it's written `:+` and is
> explained in Chapter 24 -- but this operation is rarely used, because the time
> it takes to append to a list grows linearly with the size of the list, whereas
> prepending with `::` take constant time. Your options if you want to build a
> list efficiently by append elements is to prepend them, then when you're done
> call `reverse`; or use a `ListBuffer` a mutable list that does offer an
> `append` operation, and when you're done call `toList`. `ListBuffer` will be
> described in Section 22.2.


I have always found the functional linked list to be a bit of an anachronism
when appearing as core concept in a modern language. It is a limited data
structure in terms of functionality, especially when compared to it
non-functional mutable counter part (the doubly linked list with pointers to the
head and the tail). The mutable doubly linked list can prepend, append, and swap
elements in constant time. This makes it a highly useful data structure for a
variety of tasks, including the wonderful Least Recently Used (LRU) cache
replacement algorithm. In comparison, the traditional functional list of `cons`
cells really only supports constant time prepend.

Scala should provide a immutable list implementation with all of the features
one can expect of an ArrayList, such as the one found in Python or Ruby. Like
the Python or Ruby list Scala can simply refer to the list as `list` and
provide details about the algorithms used to achieve the functionality as
documentation. In fact a quick Google reveals Scala has such a structure and it
calls it a `Vector`. Why not simply call the `Vector` a `list`? Or at least
introduce `Vector`s as the primary list like structure to use.

Using the `List` class as the example general purpose container type is just
asking for trouble. Beginners would be better served by being introduced to
`Vector` or a similar structure right away.

Other than this quibble about the book, I think the Scala [collections
library](https://github.com/scala/scala/tree/v2.11.2/src/library/scala/collection/)
is great. A wide variety of data-structures with solid implementations.

# Values vs. Variables

> \> *from page 62*
>
> <sup>1</sup> The reason parameters are `vals` is that `vals` are easier to
> reason about. You needn't look further to determine if a `val` is reassigned,
> as you must do with a `var`.

Perfectly true, but why should I care? The compiler will have no trouble
determining whether or not a `var` is re-assigned. In fact if this was an
imperative language the first step of the optimizer would likely be to convert
the code into Single Static Assignment (SSA) form. Once in (SSA) form every
variable has exactly one definition and code re-arrangement optimizations can
proceed without difficulty.

So using `vals` instead of `vars` must be for *(in)*convenience of the
programmer. Scala does recommend using `val` over `var` when possible. So the
choice is consistent with the philosophy of the language.

My question is why prioritize the immutable against the mutable? The benefits of
this choice are not clearly explained. It is true that it is easier to write
certain proofs if you don't have to deal with changing data on the heap however
today we have the (mathematical) tools to deal with that situation.  There are
real benefits of mutable data-structures and algorithms, state mutation can be
very efficient. For instance, the [Union-Find
algorithm](http://en.wikipedia.org/wiki/Disjoint-set\_data\_structure) has a
straight forward and optimal imperative implementation. It is significantly
harder to achieve an optimal immutable version as demonstrated by [this paper
from 2007](https://www.lri.fr/~filliatr/ftp/publis/puf-wml07.pdf).





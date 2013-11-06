Title: Lessons Learned While Implementing a B+Tree
Author: Tim Henderson
Date: 2010-04-10
Category: Blog


B+Trees are complex disk based trees used to index large amounts of
data. They are used in everything from file systems, to relation
databases, to new style databases gaining popularity today. Sometimes a
domain specific application needs to index a large amount of data, but
cannot use a traditional database, or one of the NoSQL databases. In
such instances the development team needs to roll their own indices.
Here is an introduction to the B+Tree (one of the indexes my team
created) and lessons I learned while implementing it.

Introduction to the B+Tree
--------------------------

B+Trees are one of the fundamental index structures used by databases
today. This includes new style SQL free databases. The B+Tree popularity
stems from their performance approaching optimal performance in terms of
disk reads for range queries in a 1 dimensional space. What is a 1
dimensional space when talking about computer data which could be
anything (not just numbers)? It is any collection of objects where the
user accesses the object using only one attribute at a time.

For example if we have an object which has X, Y, and Z as attributes
queries would only take place on X, or Y, or Z, but never on XY, or YZ,
or XZ, or XYZ. A collection where multiple attributes are used to access
the data elements are known as multidimensional spaces. For these spaces
there are many other structures which have better performance than
B+Trees.

B+Trees perform particularly well (in comparison to some other indices)
when executing range queries. A range query is typically expressed as
inequality such as "give me all strings between 'blossom' and 'brunet.'"

When I say their performance is approaching optimal in number of disk
reads what do I mean? Why are we not measuring performance in number of
instructions executed (like we do when we analyze a binary search)? In
memory algorithms and structures like sorted arrays and binary searches
are largely bound by the number CPU cycles it takes to execute the
algorithm. We usually neglect CPU cache performance and memory locality
when analyzing them, arguing these are constant in terms of the
asymptotic performance of the algorithm. However, for a disk based
structure like B+Trees the time it takes to read (or write) to a disk
becomes the dominant term, since disks are extremely slow in comparison
to main memory. Therefore for disk structures we analyze their
performance in terms of disk reads/writes.

Basic Structure of the B+ Tree
------------------------------

While I will not give a through explanation of the exact structure and
properties of B+ Tree (I leave that to algorithm and database textbooks
by the likes of Knuth, Sedgewick, and Ullman), I will describe its basic
structure.

A B+Tree is best thought of as a key-value store. It is structured as a
generalized tree. Instead of having only one key in each node it has N
keys in each node, where N is referred to as the *degree* of the B+Tree.
In the B+Tree there are 2 kinds of nodes, interior nodes, and exterior
(leaf) nodes. The interior nodes hold keys and pointers to nodes. The
exterior nodes hold keys and their associated values. This indicates
that the interior nodes have a different (usually higher) degree than
the exterior nodes.

The reason the tree is structured this way is because it is rooted in
the nature of disk access. Disks to not return 1 byte when you ask for 1
byte instead they return what is called the disk block to which that
byte belongs, the operating system then sorts out which byte it is that
you need. B+Tree exploit the situation by making their nodes fit exactly
into the size of one disk block. Since the degree of the interior nodes
is high, this makes the tree extremely wide, which is a good thing since
it means fewer disk reads to find the value associated with any one key.


<div style="text-align:center">
  <a href="/images/bptree1.png">
    <img
      alt="Example B+Tree"
      style="width:720px; "
      src="/images/bptree1.png"/>
  </a>
</div>
Figure 1. **An Example B+Tree**

 

In figure 1 you can see an example B+Tree. For this illustration I
neglect showing the values, and have the order of the interior nodes
equal to the order of the exterior nodes. In general this will not be
the case. One thing to note in this simple example is how the exterior
nodes are chained together in order. This is why it is efficient to
execute a range query on the B+Tree. One can simply find the first key
in the range, and then traverse the leaf nodes until the last key has
been found.

Implementing the B+Tree
-----------------------

I made the decision to use TDD (Test Driven Development) for
implementing the B+Tree. TDD has a lot of pluses when trying to create a
data structure of any kind. When implementing a data structure one
typically knows exactly how the structure should function, what it
should do, and what it should never do. By writing tests first, you can
ensure that when you finish a method, it actually works. This speeds
development time especially since you already know how the structure
should function. It makes it quicker to find bugs, and to battle test
the B+Tree. Since I have released the B+Tree to the rest of my team to
use, there has not yet been a bug filled against it.

So knowing that we are using TDD, and knowing what the structure is and
how it performs. What is the best way to begin implementing this complex
structure? The way I started was to create a general structure called a
block file. My block files abstracted the notion of reading and writing
blocks (and buffering them). I also created objects to model a block
that could contain either keys and pointers, or keys and records
(instead of values from here on I will use the term records). Actually
my blocks are even more general than that as I intend to reuse them for
other disk based index structures like linear hashing in the future.

I also created what I called a ByteSlice. My ByteSlice was an array of
bytes of arbitrary length. I use it to represent, keys, records, and
pointers; everything in the B+Tree. My ByteSlice implemented a
comparator, so it could be sorted, and conversions from integer types of
various lengths to the ByteSlice and back again. By implementing this
general type my B+Trees can easily deal with any kind of data and
perform in exactly the same way.

After the infrastructure was created I began working on my first
iteration of the B+Tree. The first iteration was based on the algorithms
give by Robert Sedgewick in his excellent book "Algorithms in C++." I
managed to get this implementation up, running, and fully tested in a
matter of days. However, the version given by Sedgewick which inspired
my implementation did not deal gracefully with duplicate keys. Thus, I
need to invent my own way of handling duplicate keys.

Approaches to Handling Duplicate Keys in B+Trees
------------------------------------------------

There are several different ways of handling duplicate keys. One way is
use an unmodified insert algorithm which allows duplicate keys in blocks
but is otherwise unchanged. The issue with a structure such as this is
the search algorithm must be modified to take into account several
corner cases which arise. For instance one of the invariants of a B+Tree
may be violated in this structure. Specifically if there are many
duplicate keys, a copy of one of the keys may be in a non-leaf block.
However, the key may appear in blocks that which appear logically before
the block which is pointed at by the key in the internal block. Thus the
search algorithm must be modified to look in the previous blocks to the
one suggested by the unmodified search algorithm. This will slow down
the common case for search.

There is another issue with this straight forward implementation, if
there are many duplicate keys in the index, the index size may be taller
than necessary. Consider a situation were for each unique key there are
perhaps hundreds of duplicates, the index size will be proportional to
the total number of keys in the main file, however, you only need to
index an index on the unique keys. One of the files indexed in our
program will be indexing has such characteristics to its data. It
indexes strings (as the keys) with associated instances where those
strings show up in our documents. There can be hundreds to thousands of
instances of each unique string.

Therefore the approach I took was to store only the unique keys in the
index, and have the duplicates captured in overflow blocks in the main
file. An example of such a tree can be seen in figure 2. Consider key 6;
there are 5 instances of this key in the tree. The tree is order 3,
indicating the keys cannot all fit in one block. To handle this
situation an overflow block is chained to the block which is indexed by
the tree structure. The overflow block then points to the next relevant
block in the tree.

<div style="text-align:center">
  <a href="/images/bptree2.png">
    <img
      alt="Example B+Tree with Duplicate Keys"
      style="width:720px; "
      src="/images/bptree2.png"/>
  </a>
</div>

Figure 2. **A B+Tree with duplicate keys and overflow blocks.**

 

To create a structure such as this, the insert algorithm had to be
modified. Like the previous version these modifications do not come
without a cost, in particular the invariant which states all block must
be at least half full has been relaxed. This is not true in this B+Tree,
some blocks like the one containing key number 7, are not half full.
This problem could be partially solved by using key rotations to balance
the tree better. However, there are still corner cases where there would
be a block which is under-full. One such corner case includes when a key
falls between two keys which have overflow blocks. It must then be in a
block by itself, since this B+Tree has the invariant which state that if
a block is overflowing it can only contain one unique key. In the future
we would like to implement key rotations to help partially alleviate the
problem of under-full blocks.

The advantage of this approach to B+Trees with duplicate keys is the
index size is small no matter how the ratio of duplicate keys to the
total number of keys in the file. This property allows our searches to
be conducted quicker. Since the overflow blocks are chained into the
B+Tree structure we still have the property of being able to fast
sequential scans. One consequence is we have defined all queries on our
B+Trees to be range queries. This is fine because all of our queries
were already range queries. In conclusion we relax the condition that
all blocks must be at least half full to gain higher performance during
search.

The Lessons Learned
-------------------

The biggest lessons learned through the journey:

1.  *The Value of Test Driven Development* The impact TDD had on the
    development time of the B+Tree vs. other structures in the project
    cannot be understated. TDD dramatically reduced the time it took to
    develop the structure (from over a month for some of the other
    structures to under two weeks for the B+Tree), and has ensured
    reliability of the structure once it entered production.

2.  *The Value of the Iterative Approach* By starting simple, testing,
    and then adding complexity I was able to get a better grasp on the
    problems posed by the modifications we needed to make to the
    structure. For instance I before I tried method 2 for duplicate
    keys, I modeled the data we would be putting into our tree and
    visualized the resulting structure. I found the structure would
    perform poorly. However, the same code allowed my to visualize
    method 2 and see that it would perform well.

3.  *Visualizations as Part of Development* Writing code allowing you to
    visualize the structure you are developing can really help you find
    bugs quicker. The best tool to do this with is graphviz. The
    pictures used in this blog where generated as part of unit test
    cases. My building a visualization framework early as part of your
    unit tests you can further reduce development time. When a bug a
    appears it can be enormously helpful to visualize the actual
    structure of the tree at the time the bug manifested.

Conclusions
-----------

When the right choice for your project isn't DBMS, but you still need to
index large data, don't fear you can write the index structures
yourself. By using TDD, iterating, and visualizing as you go you can
ensure the index structure you create will perform well, and will never
get into an incorrect state. Databases are not a black box, and they are
not always the right answer. When required you can create you own
system.


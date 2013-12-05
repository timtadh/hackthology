Title: The Ruby For Loop
Author: Tim Henderson
Date: 2013-11-21
Category: Blog

I am taking some time to learn Ruby this fall from [Eloquent
Ruby](www.worldcat.org/title/eloquent-ruby/oclc/676726142). The second chapter
on choosing the right control structures has this paragraph (emphasis mine):

> Since the two versions of the “print my fonts” code are essentially
> equivalent,[1] why prefer one over the other? Mainly it is a question of
> eliminating one level of indirection. Ruby actually defines the for loop in
> terms of the each method: When you say for font in fonts, Ruby will actually
> conjure up a call to fonts.each. Given that the for statement is really a call
> to each in disguise, **why not just pull the mask off and write what you
> mean?**

> > [1] Almost. The code block in the each version actually introduces a new
> > scope. Any variables introduced into a code block are local to that block
> > and go away at the end of the block. The more traditional for version of the
> > loop does not introduce a new scope, so that variables introduced inside a
> > for are also visible outside the loop.

## Why not just pull the mask off?

We should not avoid constructs that potentially clarify the meaning of our code
because under the hood they become something else. By that argument one would
always write x86 machine code, memnonic assemblers are not for *real*
programmers! Real programmers assemble the code in their heads!

I think that a for-each loop of the style of Ruby or Python or `____` are a very
clear idiom. It reads nicely, every programmer who has a background in a C
family language will know instantly what you mean. I don't see any benefit in
avoiding the for loop in Ruby any more than I can see benefit in avoiding in C
when I could be using a goto and an if statement. Which reads better to you?
(Say the words out loud!)

    ::ruby
    fonts.each do |font|
    # fonts each do font :-(

or

    ::ruby
    for font in fonts
    # for font in fonts :-)

The for loop gets my vote.


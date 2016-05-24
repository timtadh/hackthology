Title: Writing a Lexer in Go with LexMachine
Author: Tim Henderson
Date: 2016-05-25
Category: Blog


A **lexer** is a software component that analyzes a string and breaks it up into its
component parts. Each part is tagged with what type of thing it is. This is
called *lexical analysis*. For natural languages (such as English) lexical
analysis can be difficult to do automatically but is usually easy for a human to
do. Let's look at an example of lexically analyzing the following English
sentence often used in typing practice (because it uses every letter in the
alphabet).

> The quick brown fox jumped over the lazy dog.

The sentence breaks down into individual word each of which has a part of speech

```
<article>, "The"
<adjective>, "quick"
<adjective>, "brown"
<noun>, "fox"
<verb>, "jumped"
<adverb>, "over"
<article>, "the"
<adjective>, "lazy"
<noun>, "dog"
```

Note, the word "over" can actually be either a preposition or an adverb. In this
case the context of the sentence (it modifies the verb) makes it an adverb. Many
words in natural languages have this property where the context of the overall
sentence or paragraph determines the role they play in the sentence.

Luckily, the situation is much simpler for computer languages. Most *compilers*,
which are programs translate computer languages into other computer languages,
start by lexically analyzing their input. They can also be used in a number of
other scenarios where a program needs to understand data in textual forms.

In this article, I am going to write and explain a lexer for the
[graphviz](http://www.graphviz.org) [dot
language](http://www.graphviz.org/doc/info/lang.html). `graphviz` is a tool to
visualize [graphs](https://en.wikipedia.org/wiki/Graph_\(abstract_data_type\)).
`graphviz` takes a string such as:

    digraph {
      rankdir=LR;
      a [label="a" shape=box];
      c [<label>=<<u>C</u>>];
      b [label="bb"];
      a -> c;
      c -> b;
      d -> c;
      b -> a;L
      b -> e;
      e -> f;
    }

And produces :

[![Dot Example](/images/dot-example.png)](/images/dot-example.png)

## Lexing Graphviz's `dot` language

Before one can "lex" (short for lexically analyze) a language one needs to know
what it is made up of. English is made up of punctuation marks, nouns, verbs and
that sort of thing. Computer languages also have punctuation but also have
keywords, strings, numbers, comments and so forth.

When a lexer splits up a string into parts the parts are called *tokens*. The
process of splitting up is also called *tokenizing*. Let's take a look at how
the previous example would get tokenized:


    Type    | Lexeme
    -------------------
    DIGRAPH | "digraph"
    LCURLY  | "{"
    ID      | "rankdir"
    EQUAL   | "="
    ID      | "LR"
    SEMI    | ";"
    ID      | "a"
    LSQUARE | "["
    ID      | "label"
    EQUAL   | "="
    ID      | "a"
    ID      | "shape"
    EQUAL   | "="
    ID      | "box"
    RSQUARE | "]"
    SEMI    | ";"
    ID      | "c"
    LSQUARE | "["
    ID      | "label"
    ID      | "label"
    EQUAL   | "="
    ID      | "<u>C</u>"
    RSQUARE | "]"
    SEMI    | ";"
    ID      | "b"
    .
    .
    .
    RCURLY  | "}"

Note, that like when the English sentence was analyzed spaces, newlines, tabs
and other extraneous characters where dropped. Only the syntactically important
characters are output.

Each token has two parts: the *type* and the *lexeme*. The type indicates the
role the token plays. The lexeme is the string the token was extracted from.


### Specifying Tokens

To specify how a string should be tokenized a formalism called *regular
expressions* is used. If you don't already know about regular expressions you
could start with [Wikipedia
page](https://en.wikipedia.org/wiki/Regular_expression). For a more advanced
introduction see Russ Cox's [articles](https://swtch.com/~rsc/regexp/) or Alex
Aiken's [video lectures](https://www.youtube.com/watch?v=SRhkfvqeA1M) on the
subject.

To review, a regular expression is a way of specifying a "pattern" which
matches certain strings. For instance, `a+b*a` matches `aaa` and `abbbba` but
not `aab`. To see why, note that the pattern says a string must start with 1 or
more `a` characters. So all three strings `aaa`, `abbbba` and `aab` satisfy the
first requirement. Next, the pattern says a string can have 0 or more `b`
characters. The first string, `aaa` has none (and that is ok). The second
string, `abbbba` has 4 `b` characters. The third string, `aab` has 1 `b`. So all
three strings satisfy the second requirement. Finally the pattern says a string
must end in an `a`. The first and the second string both end in `a`. However,
the third string, `aab`, do not. Therefore, the first and second strings match
the pattern but the third string does not.

#### The Token's for the `dot` Language

The `dot` language has keywords, punctuation, comments, and a rather unusual
definition for identifier (called `ID`). In the listing below, the token type is
on the left side and the regular expression or literal (in quotation marks) is
on the right.

    NODE = "node"
    EDGE = "edge"
    GRAPH = "graph"
    DIGRAPH = "digraph"
    SUBGRAPH = "subgraph"
    STRICT = "strict"
    LSQUARE = "["
    RSQUARE = "]"
    LCURLY = "{"
    RCURLY = "}"
    EQUAL = "="
    COMMA = ","
    SEMI = ";"
    COLON = ":"
    ARROW = "->"
    DDASH = "--"
    COMMENT = (/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*$)
    ID = ([a-zA-Z_][a-zA-Z0-9_]*)|("([^\"]|(\\.))*")|ID-HTML

Every token type but `ID` and `COMMENT` a literals: either a keyword or a
punctuation mark. A comment is defined by a complicated regular expression which
defines "c-style" range comments or line comments. Since the comment expression
is defined by a regular expression no nesting is allowed.

The `ID` token is more complicated. It consists of three parts:

1. The usual form as a name `[a-zA-Z_][a-zA-Z0-9_]*`

2. A string, `"([^\"]|(\\.))*"`. Thus `"\\\""` and `"asdf\""` are valid but
   `"\\""` is not.

3. A HTML string, which is non-regular (specified here in BNF):

        CHAR = [^<>]
        ID-HTML = IdHTML

        IdHTML : Tag ;
        Tag : < Body > ;
        Body : CHAR Body ;
             | Tag Body
             | e                    // denotes epsilon, the empty string
             ;

    Thus `<<xyz<xy>xyz><asdf>>` is valid but `<<>` is not

The reason the HTML string is not-regular (and therefore cannot be matched by
regular expressions) is the angle brackets, `<` and `>`, have to be properly
matched. That is, every opening bracket `<` must be matched with a closing
bracket `>`. This is not possible to specify regular expressions because they
cannot "count." For a formal explanation see the [Pumping
Lemma](https://en.wikipedia.org/wiki/Pumping_lemma_for_regular_languages).

#### Consequences of Non-Regular Tokens

If all tokens were regular (that is specifiable by a regular expression) then
the full implementation of the lexer could be generated from the regular
expressions for each of the tokens. Since the `dot` language contains at least
one token which is non-regular special consideration needs to be taken.

This turns out to be a fairly common situation in lexer implementation. For
instance, if you want to support c-style comments such as `/* comment */` which
support properly nested comments `/* asdf /* asdf */ asdf*/` then the comment
token will not longer be regular. Furthermore, many languages (such as C)
require collaboration between the parser and lexer to properly identify whether
symbols should be variable names or type names. This can also introduce a degree
of non-regularity.

Thus, to properly lexically analyze such languages our framework must have an
"escape hatch" that allows the analysis of non-regular tokens on demand while
still leverage [theory](https://swtch.com/~rsc/regexp/) for most of the work.



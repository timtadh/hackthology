Title: Faster Tokenization with a DFA Backend for Lexmachine
Author: Tim Henderson
Date: 2017-11-21
Category: Blog

<style>
div.dfa-scroller {
    overflow-x: unset;
}
div.dfa-scroller img {
    margin-left: -25%;
}
@media screen and (max-width: 1100px) {
    div.dfa-scroller {
        overflow-x: scroll;
    }
    div.dfa-scroller img {
        margin-left: unset;
    }
}
aiv.dfa-scroller {
	overflow-x: unset;
}
div.dfa-scroller img {
	margin-left: -25%;
}
@media screen and (max-width: 1100px) {
	div.dfa-scroller {
		overflow-x: scroll;
	}
	div.dfa-scroller img {
		margin-left: unset;
	}
}
</style>
<script src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

[Lexmachine](https://github.com/timtadh/lexmachine) is a lexical analysis (or
tokenization) library for Go (golang) and it just got faster thanks to a new
backend I wrote. This article is going to explain the new backend, how it works,
and why it is faster. If you want to use lexmachine checkout the
[documentation](https://github.com/timtadh/lexmachine#documentation) or the
[tutorial]({filename}lexmachine.md).

Lexical analysis is the process of breaking strings up into substrings, called
*lexemes*, and putting them into categories called *tokens*. This process is
also called *tokenization* is the first step in parsing complex file formats,
programming languages, network protocols, and other information. Let's look at a
quick example, suppose we wanted to process a custom configuration file format.
For instance, [sensors.conf](https://linux.die.net/man/5/sensors.conf) which
describes how libsensors should translate the raw readings hardware monitoring
chips to real-world values -- such as voltage and temperature. The first part of
my laptop's sensons.conf starts contains the following:

```conf
# It is recommended not to modify this file, but to drop your local
# changes in /etc/sensors.d/. File with names that start with a dot
# are ignored.

chip "lm78-*" "lm79-*" "lm80-*" "lm96080-*"

    label temp1 "M/B Temp"


chip "w83792d-*"

    label in0 "VcoreA"
    label in1 "VcoreB"
    label in6 "+5V"
    label in7 "5VSB"
    label in8 "Vbat"

    set in6_min  5.0 * 0.90
    set in6_max  5.0 * 1.10
    set in7_min  5.0 * 0.90
    set in7_max  5.0 * 1.10
    set in8_min  3.0 * 0.90
    set in8_max  3.0 * 1.10
```

Accoring to the [man page](https://linux.die.net/man/5/sensors.conf), there are
several syntactic elements in this file: keywords (`chip`, `label`, `set`, ...),
names (`in0`, `in6_min`, ..., `"lm78-*"`, `"VcoreA"`, ...), floats (`5.0`,
`0.90`, ...), operators (`+`, `-`, `*`, ...), and comments which start with `#`.
A lexical analysis would break down the file as follows:

```
Type    | Lexeme
-------------------
COMMENT | # It is recommended not to modify this file, but to drop your local
COMMENT | # changes in /etc/sensors.d/. File with names that start with a dot
COMMENT | # are ignored.
CHIP    | chip
NAME    | "lm78-*"
NAME    | "lm78-*"
NAME    | "lm79-*"
NAME    | "lm80-*"
NAME    | "lm96080-*"
LABEL   | label
NAME    | temp1
NAME    | "M/B Temp"
CHIP    | chip
NAME    | "w83792d-*"
...
SET     | set
NAME    | in8_max
FLOAT   | 3.0
STAR    | *
FLOAT   | 1.10
```

The categories are defined by *patterns* which are expressed as [regular
expressions](https://github.com/timtadh/lexmachine#regular-expressions).  As a
quick review, regular expressions (regex) are a "pattern" which describe a set
of strings. A regex is made up of characters (`a`, `b`, `0`, `@`, ...) which
combine with the operators: concatenation `abc`, alternation `a|b`, grouping
`a(b|c)d`, and repetition `a*`. Some examples:

- `abc` matches {`"abc"`}
- `a|b` matches {`"a"`, `"b"`}
- `a(b|c)d` matches {`"abd"`, `"acd"`}
- `a*` matches {`""`, `"a"`, `"aa"`, ...}
- `a(b(c|d))*` matches {`"a"`, `"abc"`, `"abd"`, `"abcbc"`, `"abcbd"`, ...}

In the running example of the `sensors.conf` file one might define the following
patterns:

- AT: `@`
- PLUS: `+`
- STAR: `*`
- DASH: `-`
- SLASH: `\`
- CARROT: `^`
- BACKTICK: <code>\`</code>
- LPAREN: `(`
- RPAREN: `)`
- BUS: `bus`
- CHIP: `chip`
- LABEL: `label`
- COMPUTE: `compute`
- IGNORE: `ignore`
- SET: `set`
- NUMBER: `[0-9]*\.?[0-9]+`
- NAME: `[a-zA-Z_][a-zA-Z0-9_]*|"[^"]*"`


These patterns define how text in the input should categorized according to the
rules for the `sensors.conf` file.

# Efficiently Categorizing Substrings with Automatons

Now we turn our attention from *what* lexical analysis is to *how* it works.
Specifically we are going to concern ourselves with the following matters:

1. How the lexical analysis problem is different than the one solved by standard
   implementations of regular expression engines (such as the `regexp` standard
   library package).
2. How to solve the lexical analysis problem with non-deterministic
   finite automatons (NFA).
3. How to more deterministic automatons improve on the solution presented by
   NFAs
4. And a brief sketch describing the conversion from regular expressions to
   automatons.

## The Lexical Analysis Problem

The [regular expression](https://en.wikipedia.org/wiki/Regular_expression)
problem decides whether a *pattern* (as specified by a regular expression)
*matches* a given *string*. If the pattern does describe the string a regular
expression engine will answer: yes it matches. Otherwise, it answers: no it does
not.

The lexical analysis problem on the other hand seeks to break up (tokenize) a
long piece of text based on an ordered set of regular expressions. It does this
by proceeding from the start of the string and finding the longest *prefix* of
the string that matches at least one pattern. It then chooses a matching pattern
with the *highest precidence* and outputs the matched text (*lexeme*) and the
category the pattern defines (*token type*).  Solving the lexical analysis
problem is possible with a standard regular expression engine is possible but it
not efficient. The whole piece of text has to be repeatedly scanned for each
token to decide on the longest prefix match and highest precedence token type to
use.

However, we can use the theory that is used to implement efficient regular
expression engines to implement efficient lexical analysis engines. The
following adjustments must be made:

1. Prefixes of a string are matched
2. Several patterns are matched at once
3. The pattern which matches the longest prefix wins
4. In case of ties, the pattern with the highest precedence wins

## Finite Automata

[Efficient regular expression engines](https://swtch.com/~rsc/regexp/) are
implemented using the theory of finite automata. Automata or automatons are
theoretical mathematical constructs which specify a machine. Specifically, a
machine that reads a string, character by character, and decides whether it is
in some *language* or not (see Figure 1). The language is a type of formal
language called a *regular* language or a Type-3 language in the Chomsky Formal
Language Hierarchy.

![Finite Automata](/images/regex-machine.png)
<div style="text-align: center; margin-top: -2em;">
<strong>Figure 1.</strong> A Simple Finite State Automaton.<br/>
If the string matches the Accept light lights up, otherwise the error light
lights up.
</div>

<p> Finite state automatons encode their matching "program" as a set of states
<span class="math">\(S\)</span>, an alphabet <span
class="math">\(\Sigma\)</span>, and a transition function which maps the current
state and next symbol to the next state <span class="math">\( T: S \times \Sigma
\rightarrow S \)</span>. There are several distinguished states: the
<em>starting state</em>, and one or more <em>accepting states</em>. At each step
through the input string the machine reads a character and consults the
transition function to determine the next state. If at the end of the string the
state has reached an <em>accepting state</em> the string is said to match the
automaton.
</p>

![Non-deterministic Finite Automata](/images/nfa.png)

<div style="text-align: center; margin-top: -2em;">
<div class=dfa-scroller>
<img alt="Deterministic Finite Automata" src="/images/dfa.png" style="width: 150%;">
</div>
<strong>Figure 1.</strong> A Simple Finite State Automaton.<br/>
If the string matches the Accept light lights up, otherwise the error light
lights up.
</div>

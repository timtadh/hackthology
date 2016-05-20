Title: Object Oriented Inheritance in Go
Author: Tim Henderson
Date: 2016-05-20
Category: Blog


The Go (golang) programming language is not a traditional object oriented
language like Smalltalk or Java. A key feature supporting traditional object
oriented design is inheritance.  Inheritance supports sharing of code and data
between related objects. It used to be that inheritance was the dominant design
for sharing code and data but today another (older) technique called composition
has seen a resurgence.

Before we jump into how to use inheritance in Go (which has some interesting
edge cases) let's see how it is used in Java.

### Inheritance vs. Composition in Java

Let's look at an example from one of my favorite topics: compilers! A compiler
is made up of a pipeline of transformations that take "plain text" and transform
it either to machine code, assembly language, bytecode, or another programming
language. The first stage of the pipeline the *lexer* performs what is called
*lexical analysis* of the programming language. It traditionally splits the text
up into the different components as: keywords, identifiers, punctuation,
numbers, etc... Each component is tagged with the class of component it is. So
for this fragment of Java:

```java
public class Main {}
```

The "components" (called *tokens*) would be:

```
<public keyword>, "public"
<class keyword>, "class"
<idenitifier>, "Main"
<left-bracket>, "{"
<right-bracket>, "}"
```

The tokens have two parts:

1. The *token type*
2. The *lexeme*, or the string the token was extracted from

This leads to the following Java design

```java
public enum TokenType {
    KEYWORD, IDENTIFIER, LBRACKET, RBRACKET, ...
}
```

```java
public class Token {
    public TokenToken type;
    public String lexeme;
}
```

For some tokens, such as numeric constants, it convenient to specialize the
`Token` object to contain some extra information. In the case of numeric
constants the numerical value of the lexeme is convenient in to store directly in
the `Token`. The traditional way to accomplish this is to have the numeric
tokens *inherit* from the `Token` class.

```java
public class IntegerConstant extends Token {
    public long value;
}
```

Another way this can be achieved is to use composition where the `IntegerConstant`
instead of extending the `Token` class contains a reference to the token.

```java
public class IntegerConstant {
    public Token type;
    public long value;
}
```

It turns out, in this particular case, inheritance is the better choice. The
reason is the `Lexer` which produces the tokens needs to return a common type.
Consider the interface of the Lexer:

```java
public class Lexer {
    public Lexer(InputStream in)
    public boolean EOF()
    public Token peek() throws Error
    public Token next() throws Error
}
```

Since in the first design (which uses inheritance) a `IntegerConstant` *is a*
`Token` it can be used in the Lexer. Now, this isn't the only design that can be
used and maybe isn't even the best design but it is valid. Let's take a look at
how it translates to into Go.

### Inheritance and Composition in Go

Composition is very natural in Go (as it is in most languages). To compose two
structures simply provide a pointer or embedding to the collaborating structure.


```go
type TokenType uint16

const (
    KEYWORD TokenType = iota
    IDENTIFIER
    LBRACKET
    RBRACKET
    INT
)

type Token struct {
  Type   TokenType
  Lexeme string
}

type IntegerConstant struct {
  Token *Token
  Value uint64
}
```

This would be the usual way to share code and data in Go. However, if you feel
the need for inheritance then how can we use it? 

#### Why would you want to use inheritance in go?

One of the obvious alternative designs for the `Token` is to make it and
interface. This works equally well in both Java and Go:

```go
type Token interface {
  Type()   TokenType
  Lexeme() string
}

type Match struct {
  toktype TokenType
  lexeme  string
}

type IntegerConstant struct {
  token Token
  value uint64
}

func (m *Match) Type() TokenType {
  return m.toktype
}

func (m *Match) Lexeme() string {
  return m.lexeme
}

func (i *IntegerConstant) Type() TokenType {
  return i.token.Type()
}

func (i *IntegerConstant) Lexeme() string {
  return i.token.Lexeme()
}

func (i *IntegerConstant) Value() uint64 {
  return i.value
}
```

The Lexer can then easily return return the `Token` interface which both `*Match`
and `*IntegerConstant` satisfy.

#### Simplifying with inheritance

One of the problems with the previous design is the manual work in
`*IntegerConstant` calling `i.token.Type()` and `i.token.Lexeme()`. It turns out
we can use Go's built in support for inheritance to avoid this work.

```go
type IntegerConstant struct {
  Token
  value uint64
}

func (i *IntegerConstant) Value() uint64 {
  return i.value
}
```
By not giving the `Token` field a name in `IntegerConstant`, it "inherits" the
methods (and fields if `Token` was a `struct`) from `Token`. This pretty cool!
We can write code like this:

```go
t := IntegerConstant{&Match{KEYWORD, "wizard"}, 2}
fmt.Println(t.Type(), t.Lexeme(), t.Value())
x := Token(t)
fmt.Println(x.Type(), x.Lexeme())
```
(try it in the playground <https://play.golang.org/p/PJW7VShpE0>)

So wow! Not only did we not have implement `Type()` and `Value()` but
`*IntegerConstant` also implements the `Token` interface. Pretty nice.

#### Inheriting from `structs`

There are three ways to do inheritance in Go. You have already seen one,
inheriting from an `interface` by putting it as the first member without a field
name. It turns out your can do the same thing with `struct`s and you have two
choices

1. Inherit by embedding

        ::go

        type IntegerConstant struct {
          Match
          value uint64
        }

2. Inherit with a pointer

        ::go

        type IntegerConstant struct {
          *Match
          value uint64
        }

On gotcha of all of these options, you can't have a Field and a method with the
same name. So if you are inheriting from a `struct` called `Foo` which
precludes you from having a method called `Foo` and prevents you from
implementing a "Fooer" interface: `type Fooer interface { Foo() }`.


### Sharing Data, Code or Both

In Go the line between inheritance and composition is pretty blurry in
comparison with Java. There is no `extends` keyword. Syntactically, inheritance
looks almost identical to composition. The only difference between composition
and inheritance in Go, is a `struct` which inherits from another `struct` can
directly access the methods and fields of the parent `struct`.

```go
type Pet struct {
  name string
}

type Dog struct {
  Pet
  Breed string
}

func (p *Pet) Speak() string {
  return fmt.Sprintf("my name is %v", p.name)
}

func (p *Pet) Name() string {
  return p.name
}

func (d *Dog) Speak() string {
  return fmt.Sprintf("%v and I am a %v", d.Pet.Speak(), d.Breed)
}

func main() {
  d := Dog{Pet: Pet{name: "spot"}, Breed: "pointer"}
  fmt.Println(d.Name())
  fmt.Println(d.Speak())
}
```
(try in the playground <https://play.golang.org/p/Pmkd27Nqqy>)

**Output**:

```
spot
my name is spot and I am a pointer
```

### Conclusion

So it turns out, while it isn't a headline feature of Go, its ability for
`struct`s to inherit from `struct` pointers, `struct`s, and `interface`s is
powerful and flexible. It allows innovative designs that can solve real
problems. For more details checkout the
[Embedding](https://golang.org/doc/effective_go.html#embedding) section of
[Effective Go](https://golang.org/doc/effective_go.html).




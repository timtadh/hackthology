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

> Thank you 李浩 (Hao Li) for translating this article into Mandarin:
> <a href="/golangzhong-de-mian-xiang-dui-xiang-ji-cheng.html" title="Golang中的面向对象继承">Golang中的面向对象继承</a>

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

For some tokens, such as numeric constants, it is convenient to specialize the
`Token` object to contain some extra information. In the case of numeric
constants the numerical value of the lexeme is convenient to store directly in
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

One of the obvious alternative designs for the `Token` is to make it an
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

The Lexer can then easily return the `Token` interface which both `*Match` and
`*IntegerConstant` satisfy.

#### Simplifying with inheritance

One of the problems with the previous design is the manual work in
`*IntegerConstant` calling `i.token.Type()` and `i.token.Lexeme()`. It turns out
we can use Go's built in support for
[*embedding*](https://twitter.com/hackthology) to avoid this work. Embedding is
a limited form of inheritance which allows types to share data and code.

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

#### "Inheriting" from `structs`

There are three ways to do "inheritance" in Go. You have already seen one,
"inheriting" from an `interface` by putting it as the first member without a field
name. It turns out your can do the same thing with `struct`s and you have two
choices

1. Inherit by embedding the `struct` by value

        ::go

        type IntegerConstant struct {
          Match
          value uint64
        }

2. Inherit by embedding a pointer to a `struct`

        ::go

        type IntegerConstant struct {
          *Match
          value uint64
        }

In all cases, the difference from a regular field is the lack of an explicit
name. However, the field still has a name. It is the name of the embedded type.
In the case of `IntegerConstant` the `Match` field is named `Match`. This is
true whether one embeds a pointer to a struct or a struct by value.

On gotcha of all of these options, you can't have a Field and a method with the
same name. A `struct` `Bar` is embedding a `struct` `Foo` precludes `Bar` from
having a method called `Foo`. It also prevents `Bar` from implementing `type
Fooer interface { Foo() }`.


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

### Limitations of Embedding as Inheritance

In comparison to a language like Java, Go's form of inheritance is quite
limited. There are multiple designs which can be easily accomplished in Java
which are not possible in Go. Let's look at some of them.

#### Overriding Methods

In the pet example above, `Dog` "overrides" the `Speak()` method. However, if
`Pet` had another method `Play()` which invokes `Speak()` that `Dog` does not
override the `Dog`'s implementation of `Speak()` would not be used:

```go
package main

import (
	"fmt"
)

type Pet struct {
	name string
}

type Dog struct {
	Pet
	Breed string
}

func (p *Pet) Play() {
	fmt.Println(p.Speak())
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
	d.Play()
}
```
(try it on the playground: <https://play.golang.org/p/id-aDKW8L6>)

**Output**:
```
spot
my name is spot and I am a pointer
my name is spot
```

Contrast this to Java, in Java it would work as expected!

```java
public class Main {
  public static void main(String[] args) {
    Dog d = new Dog("spot", "pointer");
    System.out.println(d.Name());
    System.out.println(d.Speak());
    d.Play();
  }
}

class Pet {
  public String name;

  public Pet(String name) {
    this.name = name;
  }

  public void Play() {
    System.out.println(Speak());
  }

  public String Speak() {
    return String.format("my name is %s", name);
  }

  public String Name() {
    return name;
  }
}

class Dog extends Pet {
  public String breed;

  public Dog(String name, String breed) {
    super(name);
    this.breed = breed;
  }

  public String Speak() {
    return String.format("my name is %s and I am a %s", name, breed);
  }
}
```

**Output**
```
$ javac Main.java && java Main
spot
my name is spot and I am a pointer
my name is spot and I am a pointer
```

This is a pretty big difference as it essentially precludes the use of abstract
methods as you might want to define them. However, there is a work around:

```go
package main

import (
	"fmt"
)

type Pet struct {
	speaker func() string
	name    string
}

type Dog struct {
	Pet
	Breed string
}

func NewPet(name string) *Pet {
	p := &Pet{
		name: name,
	}
	p.speaker = p.speak
	return p
}

func (p *Pet) Play() {
	fmt.Println(p.Speak())
}

func (p *Pet) Speak() string {
	return p.speaker()
}

func (p *Pet) speak() string {
	return fmt.Sprintf("my name is %v", p.name)
}

func (p *Pet) Name() string {
	return p.name
}

func NewDog(name, breed string) *Dog {
	d := &Dog{
		Pet:   Pet{name: name},
		Breed: breed,
	}
	d.speaker = d.speak
	return d
}

func (d *Dog) speak() string {
	return fmt.Sprintf("%v and I am a %v", d.Pet.speak(), d.Breed)
}

func main() {
	d := NewDog("spot", "pointer")
	fmt.Println(d.Name())
	fmt.Println(d.Speak())
	d.Play()
}
```
(try it on the playground <https://play.golang.org/p/9iIb2px7jH>)

**Output**:
```
spot
my name is spot and I am a pointer
my name is spot and I am a pointer
```

Now, it works "as expected" but it is much more verbose and difficult than in
Java. You manually have to override the method yourself. Furthermore, it is
rather fragile because if the struct is initialized incorrectly it will crash
when `Speak()` is called because `speaker()` will not have been correctly
initialized.

#### Subtyping

In Java, when the class `Dog` extends `Pet` it *is* a `Pet`. That means in every
place you need an object of type `Pet` you can use a `Dog` object. `Dog` is
said to *substitute* for `Pet`. This relationship is known as *subtyping* (`Dog`
is a *subtype* of `Pet`). This relationship is also called subtype polymorphism
and it does not exist in the Go programming language for `struct` types.

Let's look at an example:

```go
package main

import (
	"fmt"
)

type Pet struct {
	speaker func() string
	name    string
}

type Dog struct {
	Pet
	Breed string
}

func NewPet(name string) *Pet {
	p := &Pet{
		name: name,
	}
	p.speaker = p.speak
	return p
}

func (p *Pet) Play() {
	fmt.Println(p.Speak())
}

func (p *Pet) Speak() string {
	return p.speaker()
}

func (p *Pet) speak() string {
	return fmt.Sprintf("my name is %v", p.name)
}

func (p *Pet) Name() string {
	return p.name
}

func NewDog(name, breed string) *Dog {
	d := &Dog{
		Pet:   Pet{name: name},
		Breed: breed,
	}
	d.speaker = d.speak
	return d
}

func (d *Dog) speak() string {
	return fmt.Sprintf("%v and I am a %v", d.Pet.speak(), d.Breed)
}

func Play(p *Pet) {
	p.Play()
}

func main() {
	d := NewDog("spot", "pointer")
	fmt.Println(d.Name())
	fmt.Println(d.Speak())
	Play(d)
}
```
(try it out on the playground <https://play.golang.org/p/e1Ujx0VhwK>)

**Output**:
```
prog.go:62: cannot use d (type *Dog) as type *Pet in argument to Play
```

However, not all is lost because subtyping does exist for `interface` types!
Let's try it out:

```go
package main

import (
	"fmt"
)

type Pet interface {
	Name() string
	Speak() string
	Play()
}

type pet struct {
	speaker func() string
	name    string
}

type Dog interface {
	Pet
	Breed() string
}

type dog struct {
	pet
	breed string
}

func NewPet(name string) *pet {
	p := &pet{
		name: name,
	}
	p.speaker = p.speak
	return p
}

func (p *pet) Play() {
	fmt.Println(p.Speak())
}

func (p *pet) Speak() string {
	return p.speaker()
}

func (p *pet) speak() string {
	return fmt.Sprintf("my name is %v", p.name)
}

func (p *pet) Name() string {
	return p.name
}

func NewDog(name, breed string) *dog {
	d := &dog{
		pet:   pet{name: name},
		breed: breed,
	}
	d.speaker = d.speak
	return d
}

func (d *dog) speak() string {
	return fmt.Sprintf("%v and I am a %v", d.pet.speak(), d.breed)
}

func Play(p Pet) {
	p.Play()
}

func main() {
	d := NewDog("spot", "pointer")
	fmt.Println(d.Name())
	fmt.Println(d.Speak())
	Play(d)
}
```
(try it on the playground <https://play.golang.org/p/WMH-cr4AJf>)

**Output**:
```
spot
my name is spot and I am a pointer
my name is spot and I am a pointer
```

Thus, `interface`s can be used to acheive a form of subtyping. However, if they
do not change the equation on method overriding. If you want a method overridden
correctly you still have to use the "trick" I presented above.

### Conclusion

So it turns out, while it isn't a headline feature of Go, its ability for
`struct`s to embed `struct` pointers, `struct`s, and `interface`s is powerful
and flexible. It allows innovative designs that can solve real problems.
However, in comparison to Java it is limited because of a lack of direct support
for subtyping and method overriding. It does contain one feature that Java does
not, the ability to embed an `interface`. For more details on embedding checkout
the [Embedding](https://golang.org/doc/effective_go.html#embedding) section of
[Effective Go](https://golang.org/doc/effective_go.html).

----

Thank you to echlebek, Alexander Staubo, spriggan3, and breerly for reading and
providing thoughtful feedback on this post.


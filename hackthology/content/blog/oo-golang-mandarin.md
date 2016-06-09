Title: 使用对象在Golang面向继承
Author: Tim Henderson
Date: 2016-05-20
Category: Mandarin

Golang的面向对象机制与Smalltalk或者Java等传统面向对象的编程语言不同。传统面向对象编程语言的一个重要特性是继承机制。因为继承机制支持在关联对象间进行代码复用和数据共享。继承机制曾在代码复用和数据共享的设计模式占据主导地位，但是目前组合这一古老的技术重新焕发了活力。

> 本篇文章转自Tim Henderson的 "Object Oriented Inheritance in Go"， 原文地址是 <http://hackthology.com/object-oriented-inheritance-in-go.html> 。非常感谢李浩用于翻译的文章。

在我们探讨如何在Go中实现继承机制之前（该机制会有悖于我们对继承机制的常规印象），我们先看一下Java中如何实现继承机制。

### 继承与组合

让我们先看一下我最喜欢的话题之一：编译器！编译器由管道转换构成，该管道读取text文本并将其转化为机器代码、汇编语言、字节码或者其他的编程语言。管道首先会使用语法分析器对目标变成语言进行语法分析。一般情况下文本会被分解为不同的组成部分，例如：关键词、标识符、标点和数字等等。每个组成部分都会被相应的数据类型标记。例如下面这个Java数据类型：

```java
public class Main {}
```


这些组成部分（可以称作标记）如下所示：

```
<public keyword>, "public"
<class keyword>, "class"
<idenitifier>, "Main"
<left-bracket>, "{"
<right-bracket>, "}"
```

这些标记可以划分为两个部分：

1. 标记类型
2. 语义部分

这会导致我们进行如下的Java设计方式：

```java
public enum TokenType {
    KEYWORD, IDENTIFIER, LBRACKET, RBRACKET, ...
}

public class Token {
    public TokenToken type;
    **Here, I think TokenToken should be "TokenType"**
    public String lexeme;
}
```

对于一些标记类型来说，例如数值常量，标记类型最好能够将包含这些属性信息。就数值常量来说，在他的标记类型里应该包括常量值这一属性。实现这一设计的传统方式是使用继承机制产生Token子类。

```java
public class IntegerConstant extends Token {
    public long value;
}
```

另外一种完成该设计的方式是利用组合方式产生IntegerConstant，IntegerConstant包含token的引用：

```java
public class IntegerConstant {
    public Token type;
    public long value;
}
```

在这个例子中，继承机制是一个比较恰当的选择。理由是语法分析器需要返回一个通用类型。考虑一下语法分析器的接口设计：

```java
public class Lexer {
    public Lexer(InputStream in)
    public boolean EOF()
    public Token peek() throws Error
    public Token next() throws Error
}
```

在继承机制中，IntegerConstant 属于Token类型，所以它可以在Lexer中调用。这不是唯一可用或者最好的设计，但是这种设计方式是有效的。让我们看一下Go是如何完成这一目的的。

### Inheritance and Composition in Go

Go中实现组合是一件十分容易的事情。简单组合两个结构体就能够构造一个新的数据类型。

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

这就是Go中实现代码和数据共享的常用方式。然而如果你想实现继承机制，我们该如何去做？

#### Why would you want to use inheritance in go

一个可选的方案是将Token设计成接口类型。这种方案在Java和Go都适用：

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

这样分析器就可以返回满足Token接口的*Match 和 *IntegerConstant类型。

#### 继承机制的简化版

上面的实现方案的一个问题是*IntegerConstant的方法调用中，出现了重复造轮子的问题。但是我们可以使用Go内建的嵌入机制来避免此类情况的出现。嵌入机制(匿名嵌入)允许类型之前共享代码和数据。

```go
type IntegerConstant struct {
  Token
  value uint64
}

func (i *IntegerConstant) Value() uint64 {
  return i.value
}
```

IntegerConstant中匿名嵌入了Token类型，使得IntegerConstant"继承"了Token的字段和方法。很酷的方法！我们可以这样写代码：

```go
t := IntegerConstant{&Match{KEYWORD, "wizard"}, 2}
fmt.Println(t.Type(), t.Lexeme(), t.Value())
x := Token(t)
fmt.Println(x.Type(), x.Lexeme())
```
(可以在这里试一下 ：<https://play.golang.org/p/PJW7VShpE0>)

我们没有编写Type()和Value()方法的代码，但是*IntegerConstant也实现了Token接口，非常棒。

#### 结构体的"继承"机制

Go中有三种方式完成”继承“机制，您已经看到了第一种实现方式：在结构体的第一个字段匿名嵌入接口类型。你还可以利用结构体实现其他两种”继承“机制：

    1. 匿名嵌入结构体实例
```go
type IntegerConstant struct {
  Match
  value uint64
}
```
    2. 匿名嵌入结构体实例指针

```go
type IntegerConstant struct {
  *Match
  value uint64
}
```

在所有的例子中，与正常嵌入类型不同的是我们使用匿名嵌入。然而，这个字段还是有字段名称的，名称是嵌入类型名称。在IntegerConstant 的Match字段中，字段名称是Match，无论嵌入类型是实例还是指针。

在以上的方案中，你不能嵌入与嵌入类型相同的方法名。例如结构体Bar匿名嵌入结构体Foo后，就不能拥有名称为Foo的方法，同样也不能实现type Fooer interface { Foo() }接口类型。

### 共享代码、共享数据或者两者兼得

相比于Java，Go在继承和聚合之间的界限是很模糊的。Go中没有extends关键词。在语法的层次上，继承看上去与聚合没有什么区别。Go中聚合跟继承唯一的不同在于，继承自其他结构体的struct类型可以直接访问父类结构体的字段和方法。

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

(可以试一下  <https://play.golang.org/p/Pmkd27Nqqy>)

输出：

```
spot
my name is spot and I am a pointer
```

### 嵌入式继承机制的的局限

相比于Java， Go的继承机制的作用是非常有限的。有很多的设计方案可以在Java轻松实现，但是Go却不可能完成同样的工作。让我们看一下：

#### Overriding Methods

上面的Pet例子中，Dog类型重载了Speak()方法。然而如果Pet有另外一个方法Play()被调用，但是Dog没有实现Play()的时候，Dog类型的Speak()方法则不会被调用。

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

(试一下  <https://play.golang.org/p/id-aDKW8L6>)

输出：

```
spot
my name is spot and I am a pointer
my name is spot
```

但是Java中就会像我们预想的那样工作：

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

输出：

```
$ javac Main.java && java Main
spot
my name is spot and I am a pointer
my name is spot and I am a pointer
```

这个明显的区别是因为Go从根本上阻止了抽象方法的使用。让我们看看下面这个例子：

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

(试一下 <https://play.golang.org/p/9iIb2px7jH>)

输出：

```
spot
my name is spot and I am a pointer
my name is spot and I am a pointer
```

现在跟我们预想的一样了，但是跟Java相比略显冗长和晦涩。你必须手工重载方法签名。而且，代码在结构体未正确初始化的情况下会崩溃，例如当调用Speak()时，speaker()却没有完成初始化工作的时候。

#### Subtyping

在Java中，Dog继承自Pet，那么Dog类型就是Pet子类。这意味着在任何需要调用Pet类型的场景都可以使用Dog类型替换。这种关系称作多态性，但Go的结构体类型不存在这种机制。

让我们看下面的例子：

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

(试一下  <https://play.golang.org/p/e1Ujx0VhwK>)

输出：

```
prog.go:62: cannot use d (type *Dog) as type *Pet in argument to Play
```

然而，接口类型中存在子类化的多态机制！

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

(试一下  <https://play.golang.org/p/WMH-cr4AJf>)

输出：

```
spot
my name is spot and I am a pointer
my name is spot and I am a pointer
```

所以接口类型可以用来实现子类化的机制。但是如果你想正确的实现方法重载，需要了解以上的技巧。

## Conclusion

事实上，虽然这不是Go的主打特性，但是Go语言在结构体嵌入结构体或者接口方面的能力确实为实际工作增加了很大的灵活性。Go的这些特性为我们解决实际问题提供了新的解决方案。但是相较于Java等语言，由于Go缺少子类化和方法重载支持还有存在一些局限性。Go含有一项Java没有的特性--接口嵌入。关于接口嵌入的细节请参考Golang的官方文档的Embedding部分。

非常感谢echlebek, Alexander Staubo, spriggan3和breerly对这篇文章提供的支持！



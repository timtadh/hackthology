Title: Exceptions for Go as a Library
Author: Tim Henderson
Date: 2016-05-19
Category: Blog


Go (golang) lacks support for exceptions found in many other languages. There
are good reasons for Go to not include exceptions. For instance, by making
error handling explicit the programmer is forced to think concretely about
the correct action to take. Fined grained control over the handling of errors
using multiple return parameters is one of Go's strengths.

However, there are cases where Go programs do not universally benefit from
the explicit handling of errors. For instance, consider the following code:

```go
func DoStuff(a, b, c interface{}) error {
	x, err := foo(a)
	if err != nil {
		return err
	}
	y, err := bar(b, x)
	if err != nil {
		return err
	}
	z, err := bax(c, x, y)
	if err != nil {
		return err
	}
	return baz(x, y, z)
}
```

If Go had exceptions such code could be easily simplified:

```go
func DoStuff(a, b, c interface{}) throws error {
	x := foo(a)
	y := bar(b, x)
	baz(x, y, bax(c, x, y)
}
```

### Adding Exceptions with a Library

I created a [library](https://github.com/timtadh/data-structures/exc) which adds
support for exceptions to the go programming language.  This library allow you
to write go with exceptions and try-catch-finally blocks. It is not appropriate
for all situations but can simplify some application code. Libraries and
external APIs should continue to conform to the Go standard of returning error
values.

Here is an example of the `DoStuff` function where foo, bar and baz all throw
exceptions instead of returning errors. (We will look at the case where they
return errors that you want to turn into exceptions next). We want DoStuff to
be an public API function and return an error:

```go
func DoStuff(a, b, c interface{}) error {
	return exc.Try(func() {
		x := foo(a)
		y := bar(b, x)
		baz(x, y, bax(c, x, y)
	}).Error()
}
```

#### Catch Blocks

Now let's consider the case where we want to catch the exception log and
reraise it:

```go
func DoStuff(a, b, c interface{}) error {
	return exc.Try(func() {
		x := foo(a)
		y := bar(b, x)
		baz(x, y, bax(c, x, y)
	}).Catch(&exc.Exception{}, func(t exc.Throwable) {
		log.Print(t)
		exc.Rethrow(t, exc.Errorf("rethrow after logging"))
	}).Error()
}
```

Rethrow will chain the Throwable `t` with the new `*Error` created such that
if/when the exception reaches the top level you know exactly how it was
created and where it was re-thrown.

#### Throwing Errors

Ok, what about interacting with regular Go APIs which return errors? How can
we turn those errors into exceptions? The easy was is to use the
`ThrowOnError` function which is a sugar for:

```go
if err != nil {
	ThrowErr(ErrorFrom(err)
}
```

So converting out original `DoStuff` function we get

```go
func DoStuff(a, b, c interface{}) { // Throws
	x, err := foo(a)
	exc.ThrowOnError(err)
	y, err := bar(b, x)
	exc.ThrowOnError(err)
	z, err := bax(c, x, y)
	exc.ThrowOnError(err)
	exc.ThrowOnError(baz(x, y, z))
}
```

This package also supports: catching user defined exceptions, catching
multiple exception types, `Close` which works like the "try with resources"
construct in Java 7+, (multiple) finally blocks, and a choice between
propagating exceptions with `Unwind` or retrieving the error/exception with
`Error` and `Exception` functions.

One Gotcha! The `Try()` function creates a `*Block` struct. To execute the
block you must either call: `Unwind`, `Error`, or `Exception`. `Unwind`
executes the block, if there is an exception coming out of the block it
continues to cause the program stack unwind. `Error` and `Exception` execute
the block, but return the exception as a value to deal with in the usual Go
way.

#### Finally Blocks

Finally blocks are a great feature of exceptions. They allow you to have a block
of code run unconditionally after a try and catch block even if there was an
un-handled exception or re-raised exception. In this example I use a finally
block to log the timing information of the DoStuff function.

```go
func DoStuff(a, b, c interface{}) error {
	start := time.Now()
	return exc.Try(func() {
		x := foo(a)
		y := bar(b, x)
		baz(x, y, bax(c, x, y)
	}).Catch(&exc.Exception{}, func(t exc.Throwable) {
		log.Print(t)
		exc.Rethrow(t, exc.Errorf("rethrow after logging"))
	}).Finally(func() {
		end := time.Now()
		log.Printf("Do stuff took: %v", end.Sub(start))
	}).Error()
}
```

#### Automatically Closing Resources

One common situation is to open a resource (like a file) and want it to close no
matter what. In Go this is often accomplished with a `defer` function. However,
we can accomplish the same thing with finer granularity using the `Close`
function which acts like a `Try` but automatically closes a created resource
when the block exits:

```go
Close(func() io.Closer {
	f, err := os.Create("/tmp/wizard")
	ThrowOnError(err)
	return f
}, func(c io.Closer) {
	f := c.(*os.File)
	_, err := f.WriteString("wizardry")
	ThrowOnError(err)
}).Unwind()
```

In the above code, the file created in the first function will always be closed
at the end of the *Block even if WriteString had an error. This get more
interesting if you imagine passing the resource to other functions which could
throw exceptions.


#### User Defined Exception Types

To create a user defined exception simply create a struct which inherits from
the `exc.Exception` struct by embedding it as the first member.

```go
type MyException struct {
	exc.Exception
}
```

Then you can catch *MyException with *Exception. eg:

```go
exc.Try(func() {
	Throw(&MyException{*Errorf("My Exception").Exception()})
}).Catch(&Exception{}, func(t Throwable) {
	log.Log("caught!")
}).Unwind()
```

This should work with heirarchies of exceptions allowing your code to declare
specific exceptions for specific errors.

### How does it work?

Go provides `panic` and `recover` as [built-in
functions](https://golang.org/ref/spec#Handling_panics). `panic(.)` allows you
to cause the program to halt and the stack to "unwind". This means stack frame
by stack frame the each function is halted and any deferred functions are run.
Let's look at an example:

```go
package main

import (
	"fmt"
)

func a() {
	defer func() {
		fmt.Println("defer a")
	}()
	fmt.Println("a")
	b()
}

func b() {
	defer func() {
		fmt.Println("defer b")
	}()
	fmt.Println("b")
	c()
}

func c() {
	defer func() {
		fmt.Println("defer c")
	}()
	fmt.Println("c")
	panic("c panic")
}

func main() {
	a()
}
```

**Output**:

```
a
b
c
defer c
defer b
defer a
panic: c panic

goroutine 1 [running]:
panic(0x128360, 0x1040a140)
	/usr/local/go/src/runtime/panic.go:481 +0x700
main.c()
	/tmp/sandbox797297488/main.go:28 +0x180
main.b()
	/tmp/sandbox797297488/main.go:20 +0x140
main.a()
	/tmp/sandbox797297488/main.go:12 +0x140
main.main()
	/tmp/sandbox797297488/main.go:32 +0x20
```

(try it on the playground <https://play.golang.org/p/0Vp4jq0978>)

So panic by default kills your program but gives you a nice stack trace. It also
runs your `defer`ed functions which allows some cleanup to happen. Recognizing
this was rather limited and their are times even in Go when it is nice to
recover from what is usually a fatal error (like in webservers) Go also provides
`recover`.

The `recover` function can be thought of as a limited panic catching function.
It can only meaingfully be used inside of defer functions. When a `recover` is
found it will stop the panic (that is stop unwinding the stack) and allow the
function the `defer`ed `recover` is in to exit normally. Let's look at another
example:

```go
package main

import (
	"fmt"
)

func a() {
	defer func() {
		fmt.Println("defer a")
	}()
	fmt.Println("a")
	b()
	fmt.Println("end a")
}

func b() {
	defer func() {
		fmt.Println("defer b")
		recover()
	}()
	fmt.Println("b")
	c()
	fmt.Println("end b")
}

func c() {
	defer func() {
		fmt.Println("defer c")
	}()
	fmt.Println("c")
	panic("c panic")
	fmt.Println("end c")
}

func main() {
	fmt.Println("start")
	a()
	fmt.Println("end")
}
```

**Output**:

```
start
a
b
c
defer c
defer b
end a
defer a
end
```

(Try it on the playground: <https://play.golang.org/p/WTzKywhey2>)

This time, instead of the program crashing it exited normally. Functions, `a`
and `main`, who invocations occurred before `b` which invoked `recover` exited
normally. However, using recover like this will stop all errors and not explain
what the problem is. Luckily, recover reports whether or not a panic was
recovered and what the argument to the panic was. Here is an example:

```go
package main

import (
	"fmt"
)

func a() {
	defer func() {
		fmt.Println("defer a")
		if e := recover(); e != nil {
			fmt.Println("recovered", e)
		}
		fmt.Println("end defer of a")
	}()
	fmt.Println("a")
	b()
	fmt.Println("end a")
}

func b() {
	defer func() {
		fmt.Println("defer b")
		if e := recover(); e != nil {
			fmt.Println("recovered", e)
		}
		fmt.Println("end defer of b")
	}()
	fmt.Println("b")
	c()
	fmt.Println("end b")
}

func c() {
	defer func() {
		fmt.Println("defer c")
	}()
	fmt.Println("c")
	panic("c panic")
	fmt.Println("end c")
}

func main() {
	fmt.Println("start")
	a()
	fmt.Println("end")
}
```

**Output**:

```
start
a
b
c
defer c
defer b
recovered c panic
end defer of b
end a
defer a
end defer of a
end
```

(Try it on the playground: <https://play.golang.org/p/agxBcqgCb8>)

This time the value passed into panic was returned by the call to `recover` in
`b`. In `a` which contains the same code as `b` to recover the panic nothing is
returned by `recover`.

#### Implementation

To implement exceptions, `panic` is used to throw the `Throwable` objects. Then
a special function `exec` is created to execute the `try` functions:

```go
func (b *Block) exec() (err Throwable) {
	defer func() {
		if e := recover(); e != nil {
			switch exc := e.(type) {
			case Throwable:
				err = exc
			default:
				panic(e)
			}
		}
	}()
	b.try()
	return
}
```

This function simply calls the function passed into `Try()`. However, `exec` also
registers a `defer` which changes the returned value of `exec` if a `Throwable`
is discovered. Thus, we can throw exceptions with `panic` (no changes
necessary!) and catch them with `recover`. The final piece is implementing the
semantics of try, catch, finally. This is accomplished by a function called
`run`:

```go
func (b *Block) run() (Throwable) {
	err := b.exec()
	if err != nil {
		t := reflect.TypeOf(err)
		for _, c := range b.catches {
			if isa(t, c.exception) {
				err = Try(func(){c.catch(err)}).exec()
				break
			}
		}
	}
	for _, finally := range b.finallies {
		finally()
	}
	return err
}
```

The `run` function first executes the `try` and gets the error if any. If there
is an error it tries to find a catch function to handle it (using the `isa`
helper function to identify the catcher). Then whether or not a catch function
was found, all `finally` functions are run in order of declaration. The final
trick is the `catch` functions are run inside of a `Try` block and `exec`
directly in case they re-throw exceptions. That is it! Check out the [source
code](https://github.com/timtadh/data-structures/tree/master/exc) for more
details.

## Conclusion

There are good reasons why Go does not include exceptions at the language level.
However, at times their absence can become annoying. So I created this little
library that adds them to Go. You probably shouldn't make public APIs based on
it, but it may help you write certain internal code more clearly. One clear use
case is during a refactor adding `Throw` call in a deep internal function which
should have always returned an error. Then at the entry points to the API simply
wrap up in a `Try().Catch().Error()` which would accomplish the same thing as
adding a returned error throughout the library.

I hope you enjoy this little experiment of mine and don't send me too much hate
mail! I know that exceptions are controversal in the Go community. This library
tries to demonstrate how close `panic` and `recover` are to exceptions and how
to emulate exceptions using `panic` and `recover`.

Now go [read the docs](https://godoc.org/github.com/timtadh/data-structures/exc).


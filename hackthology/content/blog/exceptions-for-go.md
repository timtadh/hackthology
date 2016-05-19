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

I created a [library](https://github.com/timtadh/data-structures/exc) which
adds support for exceptions to the go programming langauge.

<a href="https://godoc.org/github.com/timtadh/data-structures/exc"><img src="https://godoc.org/github.com/timtadh/data-structures/exc?status.svg" alt="GoDoc"></a>

This library allow you to write go with exceptions and try-catch-finally
blocks. It is not appropriate for all situations but can simplify some
application code. Libraries and external APIs should continue to conform to
the Go standard of returning error values.

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
created and where it was rethrown.

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
propogating exceptions with `Unwind` or retrieving the error/exception with
`Error` and `Exception` functions.

One Gotcha! The `Try()` function creates a `*Block` struct. To execute the
block you must either call: `Unwind`, `Error`, or `Exception`. `Unwind`
executes the block, if there is an exception coming out of the block it
continues to cause the program stack unwind. `Error` and `Exception` excute
the block, but return the exception as a value to deal with in the usual Go
way.

#### Finally Blocks

Finally blocks are a great feature of exceptions. They allow you to have a block
of code run unconditionally after a try and catch block even if there was an
unhandled exception or re-raised exception. In this example I use a finally
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

Now go read the docs:

<a href="https://godoc.org/github.com/timtadh/data-structures/exc"><img src="https://godoc.org/github.com/timtadh/data-structures/exc?status.svg" alt="GoDoc"></a>



Title: First Rust Macro
Author: Tim Henderson
Date: 2014-09-20
Category: Blog


I started learning [Rust](http://www.rust-lang.org/) yesterday. Today as I was
writing input handling code I wanted to print to the standard err. The way to do
that seems to be:

```rust
(writeln![io::stderr(), "{}", err]).ok().expect("write to stderr failed");
```

That seems a bit verbose to me versus printing to the standard out, which is:

```rust
println!("{}", err)
```

So I decided to fix that with the following macro:

```rust
macro_rules! log(($fmt:expr$(, $msg:expr)*) => {
    (writeln![io::stderr(), $fmt $(, $msg)*]).ok().expect("log failed")
})
```

Which you can use like so:

```rust
log!("{}", err)
```

Or

```rust
log!("expected {} got {}", expected, actual)
```

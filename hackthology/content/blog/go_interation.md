Title: Functional Iteration in Go
Author: Tim Henderson
Date: 2013-12-13
Category: Blog


Go provides a built in way to iterate easily over built-in collection types:
`maps`, `slices` and `chans`. Iterating with these types is much like iterating
using for-each type loops in languages like Python, Ruby and Java.

    ::go

    for key, value := range map {
        // key, value
    }

    for index, item := range slice {
        // index, item
    }

    for item := range channel {
        // item
    }

Unfortunately, Go does not provide a way to iterate over user defined
collections using range. I have been experimenting with how to solve this
problem since the initial public release of Go and I have finally settled on a
solution I like. This new solution uses a functional programming style.

## Functional Iterators

    ::go

    type Iterator func()(item interface{}, next Iterator)

This iterator is a function. Calling the function yields the next item in the
collection and a continuation function pointer. When the continuation function
pointer becomes nil, there are no more items left in the collection. Here's an
example of how to use a functional iterator from a test case in my
[data-structures repository](
https://github.com/timtadh/data-structures/blob/ab3c41d91c7b569caa0e989c7787de16cca7d10b/tree/avltree_test.go#L206):


    ::go

    var data []int = []int{
        1, 5, 7, 9, 12, 13, 17, 18, 19, 20,
    }

    j := 0
    for k, v, next := tree.Iterate()(); next != nil; k, v, next = next() {
        if !k.Equals(types.Int(data[j])) {
            t.Error("Wrong key")
        }
        if v.(int) != j {
            t.Error("Wrong value")
        }
        j += 1
    }

The functional approach allows the user to have a nice "linked-list" style
interface while avoiding the problems with using channels to implement
iteration. Using channels make iterators quite easy to write, consider this
post-order traversal:

    ::go

    package main

    import "fmt"

    type Node struct {
        label int
        children []Node
    }

    func (self *Node) String() string {
        return fmt.Sprintf("<%v %v>", self.label, self.children)
    }

    func (self *Node) PostOrder() (<-chan int) {
        ch := make(chan int)
        go func(yield chan<- int) {
            var iter func(node *Node)
            iter = func(node *Node) {
                if node == nil {
                    return
                }
                for _, child := range node.children {
                    iter(&child)
                }
                yield<-node.label
            }
            iter(self)
            close(yield)
        }(ch)
        return ch
    }

    func main() {
        root := &Node{5, []Node{Node{3, []Node{Node{1, nil}, Node{4, nil}}}, Node{7, []Node{Node{6, nil}, Node{10, []Node{Node{8, nil}, Node{12, nil}}}}}}}
        fmt.Println(root)
        for i := range root.PostOrder() {
            fmt.Println(i)
        }
    }

(try it on the playground <http://play.golang.org/p/kUGDQvWhkb>)

However, what happens if the consumer of the iterator needs to bail out early?
Like so:

    ::go

    for i := range root.PostOrder() {
        fmt.Println(i)
        if i % 2 == 0 {
            break
        }
    }

In this case the go-routine `PostOrder` is running in will leak. Since, it will
be blocked on sending to the consumer who will never consume the item. The fix
for this is to make the API more complicated by adding two way communication
such that the consuming thread can indicate to the producing thread it no longer
wants any more items. This can be a significant complication as it would be in
the cute little post-order traversal presented above.

## Functional Iteration to the Rescue (almost)

Functional iteration solves several of the problems with iterating using
channels while maintaining an easy to use interface. Because all the code runs
on the same go-routine no go-routines can leak. If a consumer stops using an
iterator the garbage collector can clean it up. In the `PostOrder` traversal
above the channel can leak because the producing go-routine maintains a
reference. However, functional iterators are a bit tricky to write. Let's look
at a few from the [data-structures
repository](https://github.com/timtadh/data-structures).

### Hash Table Iteration.

    ::go

    func (self *Hash) Iterate() KVIterator {
        table := self.table
        i := -1
        var e *entry
        var kv_iterator KVIterator
        kv_iterator = func()(key Equatable, val interface{}, next KVIterator) {
            for e == nil {
                i++
                if i >= len(table) {
                    return nil, nil, nil
                }
                e = table[i]
            }
            key = e.key
            val = e.value
            e = e.next
            return key, val, kv_iterator
        }
        return kv_iterator
    }

How does the function work? The first thing to notice is the `Iterate` function
returns a function `kv_iterator` which closes over some state: `table`, `i` and
`e`. The `table` variable is the array backing the hash table. The `i` variable
refers to which bucket is currently being examined. Finally, the `e` variable
refers to which entry in the bucket is next to be returned to the consumer.

When the consumer calls the `kv_iterator` function for the first time `e` will
be `nil` and the top loop will run until and entry is found or it has run
through the entire table. When and entry is found, the key and value are stored
and `e` is set to `e.next`. This assignment modifies the closed state of
`kv_iterator` and will be preserved on the next call to `kv_iterator`. Finally,
`key`, `val` and `kv_iterator` are returned to the consumer.

The main thing to understand about the `kv_iterator` function and all iterators
of this style is they implement a tail-recursive approach to iteration. Thus,
just like writing a tail-recursive function in Scheme or Lisp one must write the
iterator such that no actions need to be taken after the data is returned to the
user. This sometimes gets tricky, for instance in post-order iteration.

### Post Order Iteration

    ::go

    package main

    import "fmt"

    type Node struct {
        label int
        children []Node
    }

    type IntIterator func()(label int, next IntIterator)

    func (self *Node) String() string {
        return fmt.Sprintf("<%v %v>", self.label, self.children)
    }

    func (self *Node) PostOrder() IntIterator {
        type entry struct {
            tn *Node
            i int
        }

        pop := func (stack []entry) ([]entry, *Node, int) {
            if len(stack) <= 0 {
                return stack, nil, 0
            } else {
                e := stack[len(stack)-1]
                return stack[0:len(stack)-1], e.tn, e.i
            }
        }

        stack := append(make([]entry, 0, 10), entry{self, 0})

        var iterator IntIterator
        iterator = func()(label int, next IntIterator) {
            var i int
            var tn *Node

            if len(stack) <= 0 {
                return 0, nil
            }

            stack, tn, i = pop(stack)
            if tn == nil {
                return 0, nil
            }
            for i < len(tn.children) {
                kid := &tn.children[i]
                stack = append(stack, entry{tn, i+1})
                tn = kid
                i = 0
            }
            return tn.label, iterator
        }
        return iterator

    }

    func main() {
        root := &Node{5, []Node{Node{3, []Node{Node{1, nil}, Node{4, nil}}}, Node{7, []Node{Node{6, nil}, Node{10, []Node{Node{8, nil}, Node{12, nil}}}}}}}
        fmt.Println(root)
        for i, next := root.PostOrder()(); next != nil; i, next = next() {
            fmt.Println(i)
        }
    }


(try it out yourself on the playground <http://play.golang.org/p/M4ivyGL7GM>)

This time, the iterator must keep a stack of items in order to function. The
top entry contains the next item to process and location in its child list next
to process. The function pops a node, `tn`, and child index, `i`, off of the
stack. If the node, `tn`, has unprocessed children it gets the next child, and
pushes `tn` back onto the stack (and increments `i`). The child then becomes
`tn`. It continues traversing down the left most side of the tree until it gets
to a leaf node. At that point, the function exits the loop and returns the final
value for `tn` and the `tn_iterator`.

The next time the function is called, it will pop the stack and find the parent
of the last node it returned to the consumer. If there are more children of
parent left to processed it will repeat the process described above. Otherwise,
the parent gets returned to the consumer and the stack shrinks.

## Conclusion

Functional iterators represent a flexible way to implement generic iterators in
Go. They are easy to use and do not leak resources. There only draw back in
comparison to other approaches is greater difficulty in constructing the
iterators. In order solve this libraries of data-structures and iterator
generators should be constructed.

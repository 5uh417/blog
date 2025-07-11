---
Title: Context Managers in Python
Date: 2020-10-06
Author: smirza
Slug: context-manager-python
Tags: python, notes
Keywords:
Summary: Context Managers is a simple protocol or interface that your object needs to follow in order to support the `with` statement. It makes properly acquiring and releasing resources a breeze. `with` statements abstracts away most of the resource handling logic.
Status: published
---

With Statements simplify some common resource management patterns by abstracting their functionality and allowing them to be factored out and reused.

An example of `with` statement:

```py
with open('hello.txt', 'w') as f:
	f.write('hello, world!')
```

Opening files with `with` statement is recommended because it ensure that open file descriptors are closed automatically after program execution leaves the context of the with statement.

BTS of `with` statement using `open`:

```py
f = open('hello.txt', 'w')
try:
	f.write('hello, world')
finally:
	f.close()
```

> Side Note

```
The `try` block lets you test a block of code for errors.
The `except` block lets you handle the error.
The `finally` block lets you execute code, regardless of the result of the try- and except blocks.
```

### Without using with statement:

```py
f = open('hello.txt', 'w')
f.write('hello, world')
f.close()
```

The above implementation will not guarantee that the file is closed if there is an exception during the f.write() call - and therefore our program might leak a file description.

## Supporting `with` in your own object

**Context Managers:** A simple protocol or interface that your object needs to follow in order to support the `with` statement.
It makes properly acquiring and releasing resources a breeze. Context Managers or `with` statements abstracts away most of the resource handling logic.

### Class Based Context Managers

Basically all you need to do is add `__enter__` and `__exit__` methods to an object if you want to function as a context manager. Python will call these methods at the appropriate times in the resource management cycle.

```py
class ManagedFile:
	def __init__(self, name):
		self.name = name
	def __enter__(self):
		self.file = open(self.name, 'w')
		return self.file
	def __exit__(self, exc_type, ecx_val, ecx_tb):
		if self.file:
			self.file.close()
```

```py
>>> with ManagedFile('hello.txt') as f:
...     f.write('hello, world!')
...     f.write('bye now')
>>>
```

Python calls `__enter__` when execution enters the context of the with statement and it’s time to acquire the resource. When execution leaves the context again, python calls `__exit__` to free up the resources.

### Context Manager using contextlib

Writing a class based context manager isn’t the only way to support the with statement.

The `contextlib` utility module in the standard library provides a few more abstractions built on top of the basic context manager protocol.

You can use the `contextlib.contextmanager` decorator to define a generator-based factory function for a resource that will then automatically support the with statement.

```py
from contextlib import contextmanager

@contextmanager
def managed_file(name):
	try:
		f = open(name, 'w')
		yield f
	finally:
		f.close()
```

In this case, managed_file() is a generator that first acquires the resource. After that, it temporarily suspends its own execution and yields the resource so it can be used by the caller. When the caller leaver the context, the generator continues to execute so that any remaining clean -up steps can occur and the resource can get released back to the system.

## Nested With statements with another example.

```py
class Indenter:
	def __init__(self):
		self.level = 0
	def __enter__(self):
		self.level += 1
		return self
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.level -= 1
		return self
	def print(self, text):
		print('    ' * self.level + text)
```

```py
>>> with Indenter() as indent:
...     indent.print('Hi!')
...     with indent:
...             indent.print("hello there!")
...             with indent:
...                     indent.print('Boo!')
...     indent.print('side lined')
...
    Hi!
        hello there!
            Boo!
    side lined
>>>
```

## Key Takeaways

- The with statement simplifies exception handling by encapsulating standard uses of try/finally statements in so-called context managers.
- Most commonly it is used to manage the safe acquisition and release of system resources. Resources are acquired by the with statement and released automatically when execution leaves the with context.
- Using with effectively can help you avoid resource leaks and make your code easier to read.

---
Title: Whats with all the Underscores in Python 🤯
Date: 2020-10-07
Author: smirza
Slug: python-underscores
Tags: python, notes
Keywords: python, underscores
Summary: The various meanings and naming conventions around single and double underscores (“dunder”) in Python, how name mangling works and how it affects your own Python classes.
Status: published

---

The various meanings and naming conventions around single and double underscores (“dunder”) in Python, how name mangling works and how it affects your own Python classes.

## Various Types of Underscores seen in Python:

`_var` -> Single leading underscore

`var_` -> Single Trailing underscore

`__var` -> Double leading underscore

`__var__` -> Double leading and trailing underscore

`_` -> Single Underscore

## Single Leading Underscore “\_var”

A variable or a method starting with a single underscore is intended for internal use. Its Meaning is by convention only. (Defined in PEP 8). It is supposed to play the role of a warning sign which indicates that the variable or method is not supposed to be used outside of that class or object.

```py
class Test:
	def __init__(self):
		self.foo = 13
		self._bar = 23
```

```py
>>> i = Test()
>>> i.foo
13
>>> i._bar # can be called but its not a good practice to do so. Supposed to be for internal use only.
23
>>>
```

However, leading underscored do impact how names get imported from modules.

`cat my_module.py`

```py
def external_func():
	return 23

def _internal_func():
	return 42
```

If you use a wildcard import to import all methods, python will not import names with a leading underscore. Unless the module defines an `__all__` list that overrides the behaviour.

> **NOTE:** **all** affects the `from <module> import *` behaviour only. Members that are not mentioned in `__all__` are still accessible from outside the module and can be imported with from <module> import <member>.

```py
>>> from my_module import *
>>> external_func()
23
>>> _internal_func()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name '_internal_func' is not defined
>>>
```

Unlike wildcards imports, regular imports are not affected by the leading single underscore naming convention:

```py
>>> import my_module
>>> my_module.external_func()
23
>>> my_module._internal_func()
42
>>>
```

Single underscores are a Python naming convention that indicates a name is meant for internal use. It is generally not enforced by the Python interpreter and is only meant as a hint to the programmer.

## Single Trailing Underscore: “var\_”

Used by convention to avoid naming conflicts with python keywords.

```py
>>> def make_object(name, class):
SyntaxError: "invalid syntax"

>>> def make_object(name, class_):
...		pass
```

## Double Leading Underscore: “\_\_var”

This is called **name mangling**.

The interpreter changes the name of the variable in a way that makes it harder to create collisions when the class is extended later.

```py
>>> class Test:
...     def __init__(self):
...             self.foo = 11
...             self._bar = 23
...             self.__baz = 42 ## changed to _Test__baz
...

>>> t = Test()
>>> dir(t)
['_Test__baz', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_bar', 'foo']
>>>
```

`__baz` attribute gets changed to `_Test__baz`

Trying to override or use the `__var` will result in a no attribute error.

```py
>>> class ExtendedTest(Test):
...     def __init__(self):
...             super().__init__()
...             self.foo = 'override'
...             self._bar = 'override'
...             self.__baz = 'override'
...
>>> t2 = ExtendedTest()
>>> t2.foo
'override'
>>> t2._bar
'override'
>>> t2.__baz
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'ExtendedTest' object has no attribute '__baz'
>>>
```

```py
>>> dir(t2)
['_ExtendedTest__baz', '_Test__baz', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_bar', 'foo']
>>>
```

Extended class `t2` Doesn’t have a `__baz` attribute as well.

`__baz` got turned into `_ExtendedTest__baz` to prevent accidental modification. But original `_Test__baz` is also still around.

These variables can be access like:

```py
>>> t2._ExtendedTest__baz
'override'
>>> t2._Test__baz
42
>>>
```

Name mangling is fully transparent to the programmer. Look at the below:

```py

>>> class ManglingTest:
...     def __init__(self):
...             self.__mangled = 'hello'
...     def get_mangled(self):
...             return self.__mangled
...

>>> ManglingTest().get_mangled()
'hello'
>>> ManglingTest().__mangled
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'ManglingTest' object has no attribute '__mangled'
>>>
```

Mangling also applies to method names. Name mangling affects all names that start with two underscore characters in a class context.

```py
>>> class MangledMethod:
...     def __method(self):
...             return 43
...     def call_it(self):
...             return self.__method()
...

>>> MangledMethod().call_it()
43
>>> MangledMethod().__method()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'MangledMethod' object has no attribute '__method'
>>>

```

#### Now This!!!

```py
>>> _MangledGlobal__mangled = 23
>>> class MangledGlobal:
...     def test(self):
...         return __mangled
...
```

In this example, I declared `_MangledGlobal__mangled` as a global variable. Then I accessed the variable inside the context of a class named MangledGlobal. Because of name mangling, I was able to reference the `_MangledGlobal__mangled` global variable as just `__mangled` inside the `test()` method on the class.

The Python interpreter automatically expanded the name `__mangled` to `_MangledGlobal__mangled` because it begins with two underscore characters. This demonstrates that name mangling isn’t tied to class attributes specifically. It applies to any name starting with two underscore characters that is used in a class context.

## Double Leading and Trailing Underscore: “**var**”

Names that have both leading and trailing double underscores are reserved, for special use in the language. This rule covers things like `__init__` for object constructors, or `__call__` to make objects callable.

```py
class PrefixPostfixTest:
    def __init__(self):
        self.__bam__ = 42

>>> PrefixPostfixTest().__bam__
42
```

## Single Underscore: “\_”

Per convention, a single stand-alone underscore is sometimes used as a name to indicate that a variable is temporary or insignificant.

```py
>>> for _ in range(32):
...     print('Hello, World.')
```

## Key Takeaways

- Single Leading Underscore `_var`: Naming convention indicating a name is meant for internal use. Generally not enforced by the Python interpreter (except in wildcard imports) and meant as a hint to the programmer only.
- Single Trailing Underscore `var_`: Used by convention to avoid naming conflicts with Python keywords.
- Double Leading Underscore `__var`: Triggers name mangling when used in a class context. Enforced by the Python interpreter.
- Double Leading and Trailing Underscore `__var__`: Indicates special methods defined by the Python language. Avoid this naming scheme for your own attributes.
- Single Underscore `_`: Sometimes used as a name for temporary or insignificant variables (“don’t care”). Also, it represents the result of the last expression in a Python REPL session.

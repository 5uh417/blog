---
Title: Assert Statements in Python
Date: 2020-10-01
Author: smirza
Slug: python-assert
Tags: python, notes
Keywords:
Summary: The assert keyword in Python lets you test if a condition in your code returns True, if not, the program will raise an AssertionError.
Status: published
---

Python assertion statement helps detect errors in your Python programs automatically. This will make your programs more reliable and easier to debug.

At its core, Python’s assert statement is a debugging aid that tests a condition. If the assert condition is true, nothing happens, and your program continues to execute as normal. But if the condition evaluates to false, an AssertionError exception is raised with an optional error message.

Lets start of with an Example implementation;

You are building an online store were products for our store is represented as plain dictionaries.

```py
# sample product
>>> shoes = {'name': 'Nike Shoes', 'price': 149.00}
```

You are working to add discount functionality
to the system in place. You write the following `apply_discount` function:

```python
def apply_discount(product, discount):
    price = int(product['price'] * (1.0 - discount))
    assert 0 <= price <= product['price']
    return price
```

The `assert` statement will guarantee that, no matter what, discount prices calculated by this function cannot be lower than `0` and they cannot be higher than the original price of the product.

Applying a `25%` discount on the sample product - Nike Shoes

```py
>>> apply_discount(shoes, .25)
111
```

This is a normal scenarios were the discount function works well with the given rate of discount `25%`. The `assert` statement returns `True` and does not complaint.

Let us now try bringing some chaos into the system in place, by introducing an invalid discount of `200%`, which would lead the store owner to give money to the customer.

```py
>>> apply_discount(shoes, 2.0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in apply_discount
AssertionError
>>>
```

The function raises an `AssertionError` as it violates the assertion condition we have placed in the `apply_discount` function. The Traceback points to the line of code were the assertion failed (`File "<stdin>", line 3, in apply_discount`). This speeds up debugging efforts considerably.

## Why not use an if-statement along with regular exception

**The proper use of assertion is to inform developers about _unrecoverable_ errors in a program.**

Assertions are not intended to signal expected error conditions, like a File-Not-Found error, where a user can take corrective actions or just try again.

Assertions are meant to be internal _self-checks_ for your programs. They work by declaring some conditions as impossible in your code.

Python's assert statement is a debugging aid, not a mechanism for handling run-time errors. The goal of using assertions is to let developers find the likely root cause of a bug more quickly.

## BTS on Python's Assert

At execution time, the python interpreter transform each assert statement into roughly the following sequence of statements:

```py
if __debug__:
    if not expression1:
        raise AssetionError(expression2)
```

`expression1` is the condition we test, and the optional `expression2` is an error message that's displayed if the assertion fails.

Before the assert condition is checked, there's an additional check for the **debug** global variable. It’s a built-in boolean flag that’s true under normal circumstances and false if optimizations are requested.

Providing the optional `expression2` to our example.

```py
def apply_discount(product, discount):
    price = int(product['price'] * (1.0 - discount))
    assert 0 <= price <= product['price'], "custom error message"
    return price
```

```py
>>> apply_discount(shoes, 2.0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in apply_discount
AssertionError: custom error message
>>>

```

## Caveats of using Assert

### Caveat #1: Don't Use Asserts for Data Validation

The biggest caveat with using asserts in Python is that assertions can be globally disabled with the `-O` and `-OO` command line switches, as well as the `PYTHONOPTIMIZE` environment variable in CPython.

This turns any assert statement into a null-operations, which means none of the conditions will be executed.

```py
def delete_product(prod_id, user):
    assert user.is_admin(),
    assert store.has_product(prod_id),
    store.get_product(prod_id).delete()
```

The above code can backfire quickly and lead to bug or security holes if assertions are disabled.

1. Checking for admin privileges with an assert statement is dangerous. If assertions are disabled in the Python interpreter, this turns into a null-op. Therefore any user can now delete products. The privileges check doesn’t even run.

2. The has_product() check is skipped when assertions are disabled. This means get_product() can now be called with invalid product IDs—which could lead to more severe bugs, depending on how our program is written. In the worst case, this could be an avenue for someone to launch Denial of Service attacks against our store.

**How to avoid these problems**

_Never use assertions to do data validation._ Instead, we could do our validation with regular if-statements and raise validation exceptions if necessary, like so:

```py
def delete_product(product_id, user):
    if not user.is_admin():
        raise AuthError('Must be admin to delete')
    if not store.has_product(product_id):
        raise ValueError('Unknown product id')
    store.get_product(product_id).delete()
```

The above code has the benefit that instead of raising unspecific AssertionError exceptions, it now raises semantically correct exceptions like ValueError or AuthError (which we’d have to define ourselves.)

### Caveat #2: Asserts that Never Fail

When you pass a tuple as the first argument in an `assert` statement, the assertion always evaluates as true and therefore never fails.

For example, this assertion will never fail:

```py
assert(1 == 2, 'This should fail')
```

This has to do with non-empty tuples always being truthy in python. Python. If you pass a tuple to an assert statement, it leads to the assert condition always being true—which in turn leads to the above assert statement being useless because it can never fail and trigger an exception.

## Python Assertions — Summary

Despite these caveats I believe that Python’s assertions are a powerful debugging tool that’s frequently underused by Python developers.

## Key Takeaways

- Python’s assert statement is a debugging aid that tests a condition as an internal self-check in your program.
- Asserts should only be used to help developers identify bugs. They’re not a mechanism for handling run-time errors.
- Asserts can be globally disabled with an interpreter setting.

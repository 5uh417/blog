---
Title: An Introduction to Python Generators
Date: 2020-06-26
Author: smirza
Slug: python-generators
Tags: python
Keywords: python, generators
Summary: Generator functions are a special kind of function that return a lazy iterator. These are objects that you can loop over like a list. However, unlike lists, lazy iterators do not store their contents in memory. *(source - realpython.com)*
Status: published
---

In Python the Data Structures are stored in a memory which is a limited resource. Consider the list:

```python
short_list = [1, 2, 3]
```

`short_list` is an iteratable structure and once stored in the memory you can iterate over the list one by one.

```python
medium_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
```

`medium_list` is a slightly longer list and hence takes up more memory to store it compared to the `short_list` but this list is still manageable as the performance does not take a hit when iterated over.

```python
long_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75,
76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94,
95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140,
141, 142, 143, 144, 145, 146, 147, 148, 149]
```

In the case of an even longer list (`long_list`) even more memory is taken up.

```python
longer_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
... # epsilon denotes the missing number
488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499]
```

Eventually it reaches a point where the computer memory just can not handle the structure as it is too big. If you are working with big data or an application that works with infinite sequences, your computers memory is by definition limited and not infinite. So you need to approach this problem in a different way and that is where _generators_ help.

Generators allows to attack these very large problems one small manageable chunk at a time.

## Understanding Generators

The function below is called infinite sequence, the deal is to create and print an infinite sequence of numbers. We are going to assume that the while loop below will run forever and keep returning the numbers in sequence.

```python
def infinite_sequence():
    num = 0
    while True:
        return num
        num += 1
```

But the above code will not satisfy the ask as it return at line number 4 and exits the loop. Running the above code will only output `0`.

```python
>>> infinite_sequence()
0
>>>
```

The above function will never return another value after 0 as it exits. The use of a generator function would allow us to get around this problem. Lets rewrite the function as a generator function by making one simple and quick change.

We are changing the `return` key word to `yield`.

```python
def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1
```

Since it is a generator function we cannot run it as a normal function as we did in the previous case, we create a variable and store the above function to that variable

We can further check the type of the variable by issuing `type` on that variable as shown below, it should return `<class 'generator'>`.

```python
>>> infinite = infinite_sequence()
>>> type(infinite)
<class 'generator'>
```

In order for the generator functions to give us the values, we need to use `next` keyword on the generator function variable - (`infinite` in the above example!)

```python
>>> next(infinite)
0
>>> next(infinite)
1
>>> next(infinite)
2
```

Each time we run a next on the generator function, the function stops and returns at `yield` and saves it's status or state (it is called keeping state). When we run `next` again on the function it picks up from the saved status (and increments its value in our example). We could keep calling next on the generator function and yet the memory footprint is modest as we do not have to store an infinite sequence in memory.

Let us go ahead and add another yield statement to the generator function at line number 6 soon after incrementing the num variable by 1.

```python
def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1
        yield "This is the second yield statement!"
```

Calling `next` on the above generator function will first run the function till the first yield statement, pause and save the state and return the yielded value (in our case - num).

```python
>>> next(infinite)
0
>>>
```

Calling `next` again would mean that the generator function resumes from line number 5, increment the value of num. Encountering the second `yield` statement where it returns the yielded value and saves the state of the generator function.

```python
>>> next(infinite)
'This is the second yield statement!'
>>> next(infinite)
1
>>> next(infinite)
'This is the second yield statement!'
>>>
```

Every time a generator function is called it runs till the next yield statement and saves it's state. This is a special case behavior exhibited by a generator function when it has multiple `yield` statements.

Looks look at another special case when a generator doesn't have a next value to go to. Let us write a function with a finite sequence to replicate this behavior.

```python
def finite_sequence():
    nums = [1,2,3]
    for num in nums:
        yield num
```

Calling next on the function until the finite sequence exhausts, gives us a traceback with an error type `StopIteration`.

```python
>>> finite = finite_sequence()
>>> next(finite)
1
>>> next(finite)
2
>>> next(finite)
3
>>> next(finite)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
>>>
```

Whenever we are calling an `iterator` on python - (or any structure which has baked in `__iter__` method) this is what happens behind the scenes. `next` function is used to call the next value and when it reaches the end it raises `StopIteration`, you don't usually see them because this is taken care of by exception handling.

### Generator Expressions

We have already seen how to create a generator function using the yield keyword, basically writing a normal function and switching the `return` statement with the `yield` keyword. There is another way to create generator functions and that is with **Generator Expressions**.

```python
nums_squared_lc = [num**2 for num in range(5)]
```

Assuming that we already know about list comprehension, the above will return a list of squared numbers ranging from 0 - 4. (Output Below)

```python
>>> nums_squared_lc
[0, 1, 4, 9, 16]
```

There is also generator comprehension. (use normal brackets or parenthesis instead of square brackets as used in list comprehension.)

```python
nums_squared_gc = (num**2 for num in range(5))
```

The above returns a generator object type and saves it to the variable `nums_squared_gc`.

```python
>>> nums_squared_gc
<generator object <genexpr> at 0x10b8bbc78>
>>> type(nums_squared_gc)
<class 'generator'>
>>>
```

Let us know compare how list comprehension and generator comprehension performs considering aspects such as speed and space utilized in memory.

We import `sys` which lets us understand the space taken by different objects.

```python
>>> import sys
>>> nums_squared_lc = [num**2 for num in range(100000)]
>>> nums_squared_gc = (num**2 for num in range(100000))
>>> sys.getsizeof(nums_squared_lc)
824464
>>> sys.getsizeof(nums_squared_gc)
120
>>>
```

We can see that the generator comprehension has a much smaller memory footprint than the list comprehension.

Let us now see how these two structures compares when it comes to speed, we would import cProfile to measure the speed.

```python
>>> import cProfile
# For List Comprehension
>>> cProfile.run('sum([i*2 for i in range(1000000)])')
         5 function calls in 0.101 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.080    0.080    0.080    0.080 <string>:1(<listcomp>)
        1    0.011    0.011    0.101    0.101 <string>:1(<module>)
        1    0.000    0.000    0.101    0.101 {built-in method builtins.exec}
        1    0.010    0.010    0.010    0.010 {built-in method builtins.sum}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

# For Generator Comprehension
>>> cProfile.run('sum((i*2 for i in range(1000000)))')
         1000005 function calls in 0.169 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  1000001    0.095    0.000    0.095    0.000 <string>:1(<genexpr>)
        1    0.000    0.000    0.169    0.169 <string>:1(<module>)
        1    0.000    0.000    0.169    0.169 {built-in method builtins.exec}
        1    0.074    0.074    0.169    0.169 {built-in method builtins.sum}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

>>>
```

List comprehension takes 0.101 seconds while Generator comprehension takes 0.169 seconds, the latter takes significantly higher time to run compared to the former but still runs with a much smaller memory footprint.

## Using Advanced Generator Methods

There are three of these that you should be aware of:

- .send()
- .throw()
- .close()

Lets explore each one of them with a sample code.

### .send()

```python
# checks if number is palindrome
def is_palindrome(num):
    # skip single digit inputs
    if num // 10 == 0:
        return False

    temp = num
    reversed_num = 0
    while temp != 0:
        reversed_num = (reversed_num * 10) + (temp % 10)
        temp = temp // 10
    if num == reversed_num:
        return True
    else:
        return False

# Generator Function
def infinite_palindromes():
    num = 0
    while True:
        if is_palindrome(num):
            i = (yield num)
            if i is not None:
                num = i
        num += 1

pal_gen = infinite_palindromes()

for i in pal_gen:
    print(i)
    digits = len(str(i))
    pal_gen.send(10 ** (digits))

```

In the above code under `infinite_palindromes` if you see `yield` is to the right of an assignment operator, this works together with the code after the function, as in order to send a value to yield; a generator should be initialized. (as we see in the above code: `i = (yield num)`)

In the above code `pal_gen.send(10**(digits))` is sending the value to `i = (yield num)` in place of num under `infinite_palindromes`.

Yield in this case is playing a double role, on one hand it returns the value to us on the other it works as a place holder where we can slide in a new value to it. Hence the function will start considering the num from the new value passed by the generator method send.

Running the above code gives us, palindromes and each time it runs it gives us a new palindrome which is one digit more than the previous one.

```bash
$ python send.py
11
111
1111
10101
101101
1001001
10011001
100010001
1000110001
10000100001
100001100001
1000001000001
```

> The send method in a generator function allows you to slip a value into the last yield statement where you stopped.

### .throw()

`.throw()` allows us to throw an exception in a generator.

```python
# checks if number is palindrome
def is_palindrome(num):
    # skip single digit inputs
    if num // 10 == 0:
        return False

    temp = num
    reversed_num = 0
    while temp != 0:
        reversed_num = (reversed_num * 10) + (temp % 10)
        temp = temp // 10
    if num == reversed_num:
        return True
    else:
        return False

# Generator Function
def infinite_palindromes():
    num = 0
    while True:
        if is_palindrome(num):
            i = (yield num)
            if i is not None:
                num = i
        num += 1

pal_gen = infinite_palindromes()

for i in pal_gen:
    print(i)
    digits = len(str(i))
    if digits == 5:
        pal_gen.throw(ValueError("We don't like large palindromes"))
    pal_gen.send(10 ** (digits))

```

When the if statement under the main program is triggered `if digits ==5`; it would execute the throw method.

The throw method is causing the generator to throw an exception and also specifying the exception we want. We are calling a `ValueError` here.

Running the above code with `throw()` will result in :

```bash
$ python send.py
11
111
1111
10101
Traceback (most recent call last):
  File "send.py", line 33, in <module>
    pal_gen.throw(ValueError("We don't like large palindromes"))
  File "send.py", line 22, in infinite_palindromes
    i = (yield num)
ValueError: We don't like large palindromes
```

### .close()

`.close()` allows to close a generator. As we discussed generator functions saves its state each time they are being called and `.close()` causes the generator to loose it saved state and close the generator function with a `StopIteration` traceback as if it has exhausted its sequence.

```python
# checks if number is palindrome
def is_palindrome(num):
    # skip single digit inputs
    if num // 10 == 0:
        return False

    temp = num
    reversed_num = 0
    while temp != 0:
        reversed_num = (reversed_num * 10) + (temp % 10)
        temp = temp // 10
    if num == reversed_num:
        return True
    else:
        return False

# Generator Function
def infinite_palindromes():
    num = 0
    while True:
        if is_palindrome(num):
            i = (yield num)
            if i is not None:
                num = i
        num += 1

pal_gen = infinite_palindromes()

for i in pal_gen:
    print(i)
    digits = len(str(i))
    if digits == 5:
        pal_gen.close()
    pal_gen.send(10 ** (digits))

```

Running the code with .close() would result in:

```bash
python send.py
11
111
1111
10101
Traceback (most recent call last):
  File "send.py", line 34, in <module>
    pal_gen.send(10 ** (digits))
StopIteration
```

> Additional Resource: [How to Use Generators and yield in Python - realpython.com](https://realpython.com/introduction-to-python-generators/)

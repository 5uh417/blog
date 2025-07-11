---
Title: Analyzing Algorithms, n-Notation!
Date: 2020-04-18
Author: smirza
Slug: big-o
Summary: Big O time is the language and metric we use to describe the efficiency of algorithms. Not understanding it thoroughly can really hurt you in developing an algorithm. Not only might you be judged harshly for not really understanding big O, but you will also struggle to judge when your algorithm is getting faster or slower.
Tags: algorithms, interview-notes
Keywords: algorithms
Status: published
---

Algorithm analysis is an important part of a broader computational complexity theory, which provides theoretical estimates for the resources needed by any algorithm which solves a given computational problem. These estimates provide an insight into reasonable directions of search for efficient algorithms.

Big O time is the language and metric we use to describe the efficiency of algorithms.

## An Analogy

Imagine the following scenario: You've got a file on a hard drive and you need to send it to your friend who
lives across the country. You need to get the file to your friend as fast as possible. How should you send it?
Most people's first thought would be email, FTP, or some other means of electronic transfer. That thought is
reasonable, but only half correct.

If it's a small file, you're certainly right. It would take 5 - 10 hours to get to an airport, hop on a flight, and
then deliver it to your friend.

But what if the file were really, really large? Is it possible that it's faster to physically deliver it via plane?
Yes, actually it is. A one-terabyte (1 TB) file could take more than a day to transfer electronically. It would be
much faster to just fly it across the country. If your file is that urgent (and cost isn't an issue), you might just
want to do that.

What if there were no flights, and instead you had to drive across the country? Even then, for a really huge
file, it would be faster to drive.

## Math Refresher

### Introduction

Before we go further it is important to understand the basic math that goes behind analaysing an alogirthm. If you are already aware of Logarithmic Functions, Factorial Expressions and Algebraic Expressions and its concepts please feel free to skip the section.

### Why is it Important?

Computer science in its essence is applied mathematics. This means it has a strong foundation in many different types of math. Understanding the basics of some math functions will help to get a better picture of computer science as a whole.

**Notes:**

_Logarithmic Functions:_

Log (short for logarithmic) functions are commonly referred to in computer science. This is because they are the inverse of exponential functions. Where an exponential function grows more and more over time, a log function grows **less** and **less** over time.

Below you can see the difference between these functions. On the bottom you will see a log(n), and then it’s inverse, near the top, the 2^n. Note how the log has a little two with it, this means it is using base two. Remember in binary, base 2 uses only 1 and 0. This is important when using with an online calculator. Make sure the log is set to base 2. Notice how the log function becomes almost horizontal, while the exponential function becomes almost vertical.

![/static/img/posts/02_BigO/pic1.png](/static/img/posts/02_BigO/pic1.png)

Let’s say for example this is a graph of run times. So the bottom is how many pieces of data are inserted, and the left is how long it will take. You will notice with a log function, we can insert 100 pieces of data and have a run-time below 5. With an exponential function however, we only have to insert around 5 pieces of data before our run-time exceeds 100.

Here is a [good link](http://tutorial.math.lamar.edu/Classes/Alg/LogFunctions.aspx#ExpLog_Log_Ex1_a) that describes them in a slightly different way and has some practice examples. Logarithmic functions are efficient, and that they are the inverse of exponential functions.

_Factorial Expressions:_

Factorials are interesting expressions. The notation for them are n! . What this means is that we are going to multiply a series of numbers up until the variable n.

4! = 1 _ 2 _ 3 \* 4 = 24

5! = 1 _ 2 _ 3 _ 4 _ 5 = 120

8! = 1 _ 2 _ 3 _ 4 _ 5 _ 6 _ 7 \* 8 = 40,320

10! = 1 _ 2 _ 3 _ 4 _ 5 _ 6 _ 7 _ 8 _ 9 \* 10 = 3,628,800

As you can see, factorials grow at an astounding rate. If any of our functions ever reach this, they will most likely never finish. Almost, if not every algorithm in computer science can be accomplished in faster than n! time.

_Algebraic Expressions:_

We will encounter a few algebraic expressions throughout the course. They may look something like nlogn or 2nlog(n^2) etc. All this means is that we have a variable n that will be plugged in to the equation. Because we don’t actually know how many pieces of data will go in to the algorithm, we use this n placeholder. (More about this in the next lecture).

Once we know the n value however, we can plug it in, and calculate the answer. For example, if n=32, we will then have nlogn or 32 _ log(32). This would come out to 32 _ 5 = 160 units of time.

## n-Notation Notes

### Introduction

In computer science we need a way to be able to compare different algorithms with each other. We typically use the n-Notation for this.

### Why is it Important?

Run times of different programs are usually written in n-Notation. So if we want to look up how fast a certain algorithm is, we will need to know this notation to be able to understand it.

### Notes:

N-Notation is represented as a function of n. This simply means that the program is going to be related to the variable n in some way.

**N-notation is NOT an analysis of how long an algorithm will take to run, but an analysis of how the algorithm will scale with more and more input data.**

This method is based off looking at the input of the algorithm and analyzing how the algorithm works with this input. However, we don’t particularly know how many pieces of data will come in at any given moment. What we do is replace this input number with a variable, n.

For example, let’s say we have an algorithm which runs through the amount of Facebook friends you have. When we are writing the algorithm, we have no clue how many friends are going to be added as input. You could have 250, or 2,000, or 2. So instead of giving an actual number, we just say n pieces of data will be put into this algorithm.

(The n here is just a variable, it could be x, or w, or z, but we typically use n). It is usually a count of how many operations are being run by a program. This can be the amount of inputs, the calculations, or the outputs.

The reason we use n is because it will show us how our program might react differently to different amounts of data. We as computer scientists never know how many pieces of data our programs are going to handle. So instead, we look at how our program is going to grow with different amounts of inputs.

![/static/img/posts/02_BigO/pic1.png](/static/img/posts/02_BigO/pic1.png)

As you can see with this chart, the different values yield vastly different results. The difference between n and n^2 is substantial. If you brought this out to infinity, the difference would almost be a 90-degree angle. (As the difference between them would grow to nearly infinity)

We can use these different values to compare how our different algorithms might react to different amounts of data.

| N =   | N     | N^2       | Nlog\(n\) | 1   |
| ----- | ----- | --------- | --------- | --- |
| 1     | 1     | 1         | 1         | 1   |
| 10    | 10    | 100       | 33        | 1   |
| 100   | 100   | 10,000    | 664       | 1   |
| 1,000 | 1,000 | 1,000,000 | 9965      | 1   |

The above table represents the change. It inputs some different numbers as n and then displays what different n values would give. These numbers vary a lot with the given n-formulas.

For example, with only 1,000 pieces of data, the difference between n^2 and nlog(n) is from 1,000,000 to 9965. Even though they look decently close on the line-chart above, nlog(n) will only take 1% of the time as n^2. This difference will grow the larger our n becomes.

This is the key concept behind n-notation. Even though we don’t know the specific amount of data that is coming through our program, we can atleast compare it to another that accomplishes the same task. If one runs at n^2 while the other runs at n, we know the n will be faster in **every** case.

## Big O

We usually don't use n by itself however. Typically we tie it together with a Greek letter to give it some context. Rarely does our program operate at the same timing for every single step. So instead of having exact values for things, we want to look at them in boundaries, or cases in which they are greater, less than, or equal.

| Notation | Meaning            |
| -------- | ------------------ |
| o\(n\)   | Faster             |
| O\(n\)   | Faster or Equal    |
| Ɵ\(n\)   | Equal To           |
| Ω\(n\)   | Slower or Equal to |
| ω\(n\)   | Slower Than        |

For this notation, we just use one of the Greek symbols above, with our n notation inside of the parenthesis. So for example, O(nlogn) would mean that the program is faster or equal to nlogn.

The most important notation above is the Omicron, or "Big O". The reason for this is because it gives us a worse case scenario. That means we know the absolute worse case scenario of our program, meaning if we plan for this, we won't have any surprises or weird corner cases that come up.

We can then compare the worst case scenarios of programs to see which are faster. Since this is the absolute slowest the program can run, we know that one program will always run slower than another program!

For example let's say that we have two programs, program A which runs at Ω(n) and program B which runs at Ω(n^2). Which of these two programs is better? Well all we know is that program A is slower or equal to n and program B is slower or equal to n^2. However that doesn't guarantee anything. Program A could end up running around n^3 or n! and meet the requirements of Ω(n). B could do the exact same thing, so their speed is still arbitrary. So with these symbols, we don't learn too much about the two programs.

However, if we used O(n) for A and O(n^2) for B, we can now compare the two. We know without a doubt that A will not run slower than n while B can run up to n^2. Therefore the faster is Program A, because it can never get slower than B.

Let’s use some numbers to drive this point home a little more.

Let’s say we have a time scale to determine how fast our algorithm runs. In this scale the closer to 0 we go, the faster our algorithm. We can use to show why Big O is typically the most useful of these notations.

**ω(7)** - The algorithm will run slower, or > 7. How much greater? 1,000. 1,000,000? There is no way to know. This algorithm could take years to complete the simplest of tasks.

**Ω(7)** - The algorithm will run “slower or equal” to 7, or >=7. Still could run in to infinity or really large run times.

**Θ(7)** - The algorithm is equal to 7, or = 7. This would be great. If we can guarantee an algorithm will always run equal to something we would use this. However, this is highly unlikely in the real world, so it’s not used too often.

**O(7)** - The algorithm will run “faster or equal” to 7, or <=7. This is good. We have a limit on the algorithm. We know in all cases, 7 is the worst this algorithm can do. This can be used to plan with. No surprises will come up here.

**o(7)** - The algorithm will run faster than 7, or < 7. There is nothing inherently wrong with this, except that it’s just less accurate than O(7). How much faster will it run? 6? 2?. We don’t know the limit. Although we can still plan a worst case scenario with this, it’s less accurate than O(7) which is why it’s rarely used.

## Time Complexity

This is what the concept of asymptotic runtime, or big O time, means. We could describe the data transfer
"algorithm" runtime as (taking the same analogy that we initially discussed at the start of the article):

- Electronic Transfer: 0( s ), where s is the size of the file. This means that the time to transfer the file
  increases linearly with the size of the file. (Yes, this is a bit of a simplification, but that's okay for these
  purposes.)
- Airplane Transfer: 0( 1) with respect to the size of the file. As the size of the file increases, it won't take
  any longer to get the file to your friend. The time is constant.

No matter how big the constant is and how slow the linear increase is, linear will at some point surpass
constant.

There are many more runtimes than this. Some of the most common ones are O(log N), O(N log N),
O(N), O(N^2) and 0( 2^N). There's no fixed list of possible runtimes, though.

You can also have multiple variables in your runtime. For example, the time to paint a fence that's w meters
wide and h meters high could be described as O(wh). If you needed p layers of paint, then you could say
that the time is O(whp).

## Best Case, Worst Case, and Expected Case

We can actually describe our runtime for an algorithm in three different ways.

Let's look at this from the perspective of quick sort. Quick sort picks a random element as a "pivot" and then
swaps values in the array such that the elements less than pivot appear before elements greater than pivot.
This gives a "partial sort:'Then it recursively sorts the left and right sides using a similar process.

- **Best Case:** If all elements are equal, then quick sort will, on average, just traverse through the array once.
  This is O ( N). (This actually depends slightly on the implementation of quick sort. There are implementations, though, that will run very quickly on a sorted array.)
- **Worst Case:** What if we get really unlucky and the pivot is repeatedly the biggest element in the array?
  (Actually, this can easily happen. If the pivot is chosen to be the first element in the subarray and the
  array is sorted in reverse order, we'll have this situation.) In this case, our recursion doesn't divide the
  array in half and recurse on each half. It just shrinks the subarray by one element. This will degenerate
  to anO(N2) runtime.
- **Expected Case:** Usually, though, these wonderful or terrible situations won't happen. Sure, sometimes
  the pivot will be very low or very high, but it won't happen over and over again. We can expect a runtime
  ofO(N log N).

We rarely ever discuss best case time complexity, because it's not a very useful concept. After all, we could
take essentially any algorithm, special case some input, and then get an O ( 1) time in the best case.

For many-probably most-algorithms, the worst case and the expected case are the same. Sometimes
they're different, though, and we need to describe both of the runtimes.

_What is the relationship between best/worst/expected case and big 0/theta/omega?_

It's easy for candidates to muddle these concepts (probably because both have some concepts of"higher':
"lower" and "exactly right"), but there is no particular relationship between the concepts.

Best, worst, and expected cases describe the big O (or big theta) time for particular inputs or scenarios.

Big 0, big omega, and big theta describe the upper, lower, and tight bounds for the runtime.

There you have it, Big O notation. This is used all across computer science, and now you know how to read it!

### Additional Resources

- [Logarithm Functions](http://tutorial.math.lamar.edu/Classes/Alg/LogFunctions.aspx#ExpLog_Log_Ex1_a)
- [Factorial](https://www.mathsisfun.com/numbers/factorial.html)
- [Algebraic Functions](https://study.com/academy/lesson/algebraic-function-definition-examples.html)
- [What is a plain English explanation of “Big O” notation?](https://stackoverflow.com/questions/487258/what-is-a-plain-english-explanation-of-big-o-notation)
- [Big-O notation](https://www.khanacademy.org/computing/computer-science/algorithms/asymptotic-notation/a/big-o-notation)

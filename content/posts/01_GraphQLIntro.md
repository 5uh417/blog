---
Title: Introduction to GraphQL using Python
Date: 2020-04-10
Author: smirza
Slug: graphql-python-intro
Summary: GraphQL is a data query language developed internally by Facebook in 2012 before being publicly released in 2015. It provides an alternative to REST and ad-hoc web service architectures.
Tags: graphql, python
Status: published
---

[GraphQL](https://graphql.org/) is a data query language developed internally by Facebook in 2012 before being publicly released in 2015. It provides an alternative to REST and ad-hoc web service architectures.

## Graphene-Python

Graphene-Python is a library for building GraphQL APIs in Python easily, its main goal is to provide a simple but extendable API for making developers’ lives easier.

## When to use GraphQL?

If you are creating a data-driven application of at least moderate complexity, GraphQL should absolutely merit primary consideration.

## Why Use GraphQL?

- GraphQL APIs have a strongly typed schema
- Solves the problem of over-fetching and under-fetching
- GraphQL enables rapid product development
- Composing GraphQL APIs (Schema Stitching)
- Rich open-source ecosystem and an amazing community

## GraphQL Ecosystem

GraphQL Ecosystem has three main classes:
**Query** — way to fetch data in a read-only manner from your GraphQL API (analogy of GET request in REST API).
**Mutation** — way to change(create/update/delete) data on your server (analogy of POST request in REST API).
**Subscription** — way to get a real-time feed of data from your server (something like traditional Web Sockets)

## GraphQL Schema

It can be compared to a dictionary in Python or object in Javascript, if it is possible to say, where the key is the name of a field and value is a type of this field.

## Supported data types in GraphQL

Scalars(Int, Float, String, Boolean, ID) List, Enum, Non-null are few of the most commonly used data types in GraphQL.
You can find out more info about data types in GraphQL [here](https://graphql.org/learn/schema/).

## Your First GraphQL App! (with GraphQL and Python)

Create a project directory, navigate to the same and create a `schema.py` file.

```bash
$ mkdir python-graphene
$ cd python-graphene && touch schema.py
```

Configure the `pipenv` environment and install the graphene module.

```bash
$ pipenv shell
(python-graphene)$ pipenv install graphene
```

Let's write our first app now that we have the environment set up with the required module in place.

{{<  gist sm087 55e10d1dd01f909812c966bbfa90891b >}}

_Line Numbers 5–13_: The `Query` class is a special ObjectType that sub-classes from `graphene.ObjectType` which defines the fields that are the entry-point for your API which in the above example is `user` and `is_admin`.

_Line Number 6–9_: In the above snippet which is for the resolver function in graphene, this helps fetch the required data to be returned when querying for that parameter. These functions should be prepended with resolve and should follow **snake case** styling. In the above example, these functions are `resolve_user` and `resolve_is_admin`.

_Resolver functions, in general, is a collection of functions that generate a response for your GraphQL query. In simple terms, a resolver acts as a GraphQL query handler._

_Line Number 16_: The `schema` defines the types and relationships between Fields in your API. A Schema is created by supplying the root ObjectType of each operation, query (\*mandatory), mutation and subscription. In this case, we have just supplied the Query operation.

_Line Number 18:_: Finally, in order to call the schema that we have created in the above example, we have the query string which is within comments and is passed with `schema.execute` and the same is converted to a JSON and printed to the standard out.

Running the `schema.py` file within the environment that was created should result in the below output

```bash
$ python 1_schema.py
{
  "user": "Benjamin Button",
  "isAdmin": true
}
```

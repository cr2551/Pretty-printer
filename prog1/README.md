# Project 1: Scheme Pretty-Printer

CSC 4101, Fall 2026

## Group members

- Truong Nguyen
- Carlos Rodriguez Coronel


## Design

- `Tokens` defines token types and classes carrying integer, string, or
  identifier values.
- `Parse/Scanner.py` reads characters, skips whitespace and comments, and
  produces tokens. Identifiers are converted to lowercase.
- `Parse/Parser.py` uses recursive descent to build expression trees. It
  supports proper lists, dotted lists, and apostrophe shorthand for quote.
  It reads only the tokens needed for the current expression. List elements
  are collected iteratively to avoid recursion for each element of a long list.
- `Tree` represents expressions using the `Node` hierarchy. `Cons` stores a
  list's first element and remaining tail. The empty list and boolean literals
  use shared singleton objects.
- `Special` provides printing strategies selected by `Cons` from the first
  list element. Shared helpers handle list traversal, regular list formatting,
  indentation, and parentheses.

Regular lists, variable definitions, and `set!` assignments use single-line
formatting. Quotes use apostrophe notation and print their contents as data.
`begin`, `let`, and `cond` place their keyword on the first line and indent
subsequent elements by two spaces. `if`, `lambda`, and function definitions
keep their first two elements together before indenting the remaining elements.
Function-definition bodies retain nested special-form formatting, matching
the assignment's factorial example. Other block bodies use regular-list
formatting. These choices resolve cases where the assignment's rules overlap.


## Status and limitations

The required scanner, parser, tree representation, and printing strategies are
implemented. The factorial example retains its subtraction operator correctly.
Unexpected top-level dots and closing parentheses are reported and skipped;
the process returns a failure status after processing any remaining expressions.
Other invalid input produces an error message and stops without a traceback.

This is the project's Scheme subset, not a full Scheme implementation. Numeric
literals are unsigned decimal integers. Special-form arity and semantics are
not checked because lists must also be accepted as data. Extremely deep nesting
is limited by Python's recursion depth.

Exact output comparison against the Java reference on the class server remains
unverified. Passing the local regression suite does not establish a match with
every reference test.

# Special-folder handoff

Each strategy exposes `eval(tree, env)` through Special and implements `_eval`.
`tree` is the entire form, including its leading keyword or function expression.
Printing implementations are reused from this repository's working Project 1 Special folder.

Implemented: quote, lambda, begin, if, cond (including else and test-only clauses),
define (variable and function shorthand), ordinary let, set!, and function calls.
Named let and cond's `=>` extension are outside this project's listed subset.

Required teammate interfaces:

- `Cons.eval(env)` returns `self.form.eval(self, env)`.
- Literals evaluate to themselves; `Ident.eval(env)` uses `env.lookup(self)`.
- `Environment(parent)` makes a new frame linked to parent.
- `define(Ident, value)` changes the current frame; `assign(Ident, value)` searches enclosing frames.
- `Closure(complete_lambda_tree, captured_env)` stores the entire lambda form and the live environment.
- `Closure.apply(args)` and `BuiltIn.apply(args)` accept an already evaluated Cons/Nil argument list.
- Closure.apply must implement fixed, symbol-only rest, and dotted-rest parameters.
- `Cons` construction requires `Cons.setUtil(util)` in the local starter.
- Boolean false is `BoolLit.getInstance(False)`; all other Scheme values are true.

Forms with unspecified results currently return `Nil.getInstance()`, following
the starter's placeholder convention. If the team adds an Unspecific type,
coordinate this change across the interpreter. Invalid form shapes print
`Error: ...` to stderr and return Nil; errors from other evaluator components
are not caught or suppressed here.

Run isolated contract tests from prog2:

    python -m unittest discover -s tests -v

The 16 contract tests use adapters for environment/evaluation methods to test
Special independently. Eight integration tests use the actual parser, tree nodes,
environments, closures and arithmetic/list built-ins, with test setup registering
the needed primitives. They cover recursion, lexical closures, mutation, let,
cond, anonymous calls, quoted data and reused Project 1 printing. They do not
validate full startup, all built-ins or rest-argument application.

The supplied compiled parser and leaf printer require Python 3.14. Package exports
were restored in Parse and Print. The Special printers reuse Project 1 source.
Before submission, finish the remaining Tree/startup work and run the full course suite.
In particular, Closure.apply still needs rest-parameter and argument-count handling.
The main project README should describe this AI-assisted implementation and tests.

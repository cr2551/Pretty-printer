"""Exercise Special with the repository parser, environments, closures and built-ins."""
import contextlib
import io
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from Parse import Parser, Scanner
from Tree import Cons, Environment, Closure, BuiltIn, Ident, TreeBuilder
from Util import Util
from Special import Special


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        util = Util()
        Cons.setUtil(util)
        Closure.setUtil(util)
        BuiltIn.setUtil(util)
        Special.setUtil(util)
        self.env = Environment()
        for name in ("b+", "b-", "b*", "b=", "b<", "cons", "car", "cdr"):
            self.env.define(Ident(name), BuiltIn(Ident(name)))

    def parse(self, source):
        return Parser(Scanner(io.StringIO(source)), TreeBuilder())

    def run_scheme(self, source):
        parser = self.parse(source)
        result = None
        with contextlib.redirect_stderr(io.StringIO()) as errors:
            while (expression := parser.parseExp()) is not None:
                result = expression.eval(self.env)
        self.assertEqual(errors.getvalue(), "")
        return result

    def test_recursive_function(self):
        result = self.run_scheme("(define (fac n) (if (b= n 0) 1 (b* n (fac (b- n 1))))) (fac 5)")
        self.assertEqual(result.intVal, 120)

    def test_returned_closure_uses_lexical_scope(self):
        result = self.run_scheme("(define (make x) (lambda (y) (b+ x y))) (define add (make 10)) (let ((x 99)) (add 2))")
        self.assertEqual(result.intVal, 12)

    def test_let_parallel_bindings_and_set(self):
        result = self.run_scheme("(define x 10) (let ((x 20) (y x)) (set! x (b+ x y)) x)")
        self.assertEqual(result.intVal, 30)
        self.assertEqual(self.env.lookup(Ident("x")).intVal, 10)

    def test_begin_mutates_outer_scope(self):
        self.assertEqual(self.run_scheme("(define x 1) (let () (begin (set! x 7) x)) x").intVal, 7)

    def test_cond_selects_one_branch(self):
        self.assertEqual(self.run_scheme("(cond (#f undefined) ((b< 1 2) 3 4) (else undefined))").intVal, 4)

    def test_quoted_lists_remain_data(self):
        result = self.run_scheme("(car '(unbound 2))")
        self.assertEqual(result.getName(), "unbound")

    def test_anonymous_operator(self):
        self.assertEqual(self.run_scheme("((lambda (x) (b+ x 1)) 4)").intVal, 5)

    def test_project1_printing_preserved(self):
        cases = {
            "'(lambda (x) (if x 1 2))": "'(lambda (x) (if x 1 2))\n",
            "(lambda (x) (if x 1 2))": "(lambda (x)\n  (if x\n    1\n    2\n  )\n)\n",
            "(let ((x 2)) x)": "(let\n  ((x 2))\n  x\n)\n",
        }
        for source, expected in cases.items():
            with self.subTest(source=source), contextlib.redirect_stdout(io.StringIO()) as output:
                self.parse(source).parseExp().print(0)
            self.assertEqual(output.getvalue(), expected)


if __name__ == "__main__":
    unittest.main()

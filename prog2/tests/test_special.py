"""Special-folder contract tests, isolated from unfinished teammate code.

Run: python -m unittest discover -s tests -v
Uses the repository parser/printer and requires Python 3.14.
Environment and eval adapters below are test fixtures, not interpreter fixes.
"""
import contextlib
import io
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from Tree import Node, Cons, Nil, Ident, IntLit, BoolLit, Closure
import Special
from Util import Util
import importlib
let_module = importlib.import_module("Special.Let")
fixture_modules = {name: module for name, module in sys.modules.items()
                   if name.split(".")[0] in ("Tree", "Special", "Util", "Print", "Parse")}


class Frame:
    def __init__(self, parent=None):
        self.parent = parent
        self.bindings = {}

    def lookup(self, name):
        if name.getName() in self.bindings:
            return self.bindings[name.getName()]
        if self.parent is not None:
            return self.parent.lookup(name)
        raise LookupError(name.getName())

    def define(self, name, value):
        self.bindings[name.getName()] = value

    def assign(self, name, value):
        if name.getName() in self.bindings:
            self.define(name, value)
        elif self.parent is not None:
            self.parent.assign(name, value)
        else:
            raise LookupError(name.getName())


def seq(*values):
    result = Nil.getInstance()
    for value in reversed(values):
        result = Cons(value, result)
    return result


def form(name, *values):
    return seq(Ident(name), *values)


class Probe(Node):
    def __init__(self, value, log):
        self.value, self.log = value, log

    def print(self, n, p=False):
        pass

    def eval(self, env):
        self.log.append(self.value)
        return self.value


class Procedure(Probe):
    def isProcedure(self):
        return True

    def eval(self, env):
        return self

    def apply(self, args):
        self.log.append(args)
        return self.value


class SpecialTests(unittest.TestCase):
    def setUp(self):
        self.env = Frame()
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.dict(sys.modules, fixture_modules))
        self.stack.enter_context(patch.object(Cons, "util", Util()))
        self.stack.enter_context(patch.object(Cons, "eval", lambda t, e: t.form.eval(t, e)))
        self.stack.enter_context(patch.object(Ident, "eval", lambda t, e: e.lookup(t)))
        for cls in (IntLit, BoolLit, Nil):
            self.stack.enter_context(patch.object(cls, "eval", lambda t, e: t))
        self.stack.enter_context(patch.object(let_module, "Environment", Frame))

    def evaluate(self, expression):
        return expression.eval(self.env)

    def test_quote_preserves_identity_without_evaluation(self):
        data = seq(Ident("undefined"), IntLit(3))
        self.assertIs(self.evaluate(form("quote", data)), data)

    def test_begin_order_and_result(self):
        log = []
        a, b = IntLit(1), IntLit(2)
        self.assertIs(self.evaluate(form("begin", Probe(a, log), Probe(b, log))), b)
        self.assertEqual(log, [a, b])
        self.assertIs(self.evaluate(form("begin")), Nil.getInstance())

    def test_if_skips_unselected_branch(self):
        result = IntLit(7)
        self.assertIs(self.evaluate(form("if", BoolLit.getInstance(False),
                                        Ident("undefined"), result)), result)
        self.assertIs(self.evaluate(form("if", BoolLit.getInstance(True),
                                        result, Ident("undefined"))), result)

    def test_zero_and_empty_list_are_true(self):
        for value in (IntLit(0), Nil.getInstance()):
            self.assertEqual(self.evaluate(form("if", value, IntLit(1), IntLit(2))).intVal, 1)

    def test_if_without_alternative(self):
        self.assertIs(self.evaluate(form("if", BoolLit.getInstance(False), IntLit(1))),
                      Nil.getInstance())

    def test_lambda_captures_complete_expression_and_environment(self):
        for params in (seq(Ident("x")), Ident("args"), Cons(Ident("x"), Ident("rest"))):
            expression = form("lambda", params, IntLit(1))
            result = self.evaluate(expression)
            self.assertIsInstance(result, Closure)
            self.assertIs(result.getFun(), expression)
            self.assertIs(result.getEnv(), self.env)

    def test_define_variable_and_redefine(self):
        for value in (IntLit(3), IntLit(4)):
            self.evaluate(form("define", Ident("x"), value))
            self.assertIs(self.env.lookup(Ident("x")), value)

    def test_function_shorthand_and_live_recursive_binding(self):
        params = Cons(Ident("x"), Ident("rest"))
        body = Ident("x")
        self.evaluate(form("define", Cons(Ident("f"), params), body))
        closure = self.env.lookup(Ident("f"))
        self.assertIs(closure.getEnv().lookup(Ident("f")), closure)
        function = closure.getFun()
        self.assertEqual(function.getCar().getName(), "lambda")
        self.assertIs(function.getCdr().getCar(), params)
        self.assertIs(function.getCdr().getCdr().getCar(), body)

    def test_let_initializers_use_outer_scope(self):
        outer = IntLit(10)
        self.env.define(Ident("x"), outer)
        bindings = seq(seq(Ident("x"), IntLit(20)), seq(Ident("y"), Ident("x")))
        self.assertIs(self.evaluate(form("let", bindings, Ident("y"))), outer)
        self.assertIs(self.env.lookup(Ident("x")), outer)

    def test_let_local_definitions_and_multiple_body_expressions(self):
        expression = form("let", seq(), form("define", Ident("local"), IntLit(8)), Ident("local"))
        self.assertEqual(self.evaluate(expression).intVal, 8)
        with self.assertRaises(LookupError):
            self.env.lookup(Ident("local"))

    def test_set_updates_outer_binding(self):
        self.env.define(Ident("x"), IntLit(1))
        self.evaluate(form("let", seq(), form("set!", Ident("x"), IntLit(9))))
        self.assertEqual(self.env.lookup(Ident("x")).intVal, 9)

    def test_cond_else_and_short_circuit(self):
        result = IntLit(12)
        expression = form("cond", seq(BoolLit.getInstance(False), Ident("undefined")),
                          seq(Ident("else"), IntLit(0), result))
        self.assertIs(self.evaluate(expression), result)
        expression = form("cond", seq(BoolLit.getInstance(True), result),
                          seq(Ident("undefined"), Ident("undefined")))
        self.assertIs(self.evaluate(expression), result)

    def test_cond_test_only_evaluates_once(self):
        log, result = [], IntLit(4)
        self.assertIs(self.evaluate(form("cond", seq(Probe(result, log)))), result)
        self.assertEqual(log, [result])
        self.assertIs(self.evaluate(form("cond", seq(BoolLit.getInstance(False), IntLit(1)))),
                      Nil.getInstance())

    def test_regular_passes_values_in_order_without_reevaluation(self):
        log, calls = [], []
        # A symbol returned by an operand must be passed as data, not looked up.
        a, b, result = Ident("unbound-data"), IntLit(2), IntLit(99)
        procedure = Procedure(result, calls)
        self.assertIs(self.evaluate(seq(procedure, Probe(a, log), Probe(b, log))), result)
        self.assertEqual(log, [a, b])
        self.assertIs(calls[0].getCar(), a)
        self.assertIs(calls[0].getCdr().getCar(), b)
        self.assertTrue(calls[0].getCdr().getCdr().isNull())
        self.evaluate(seq(procedure))
        self.assertTrue(calls[1].isNull())

    def test_invalid_forms_report_errors(self):
        invalid = [form("quote"), form("quote", IntLit(1), IntLit(2)),
                   form("if", IntLit(1)), form("set!", IntLit(1), IntLit(2)),
                   form("define", Ident("x"), IntLit(1), IntLit(2)),
                   form("lambda", seq(Ident("x"), Ident("x")), IntLit(1)),
                   form("lambda", Cons(Ident("x"), Ident("x")), IntLit(1)),
                   form("lambda", IntLit(1), IntLit(2)),
                   form("cond", seq(Ident("else"), IntLit(1)), seq(IntLit(2))),
                   form("cond", seq()), form("cond", seq(Ident("else"))),
                   form("let", seq(seq(Ident("x"), IntLit(1)),
                                    seq(Ident("x"), IntLit(2))), IntLit(0)),
                   form("let", seq(seq(Ident("x"))), IntLit(0)),
                   seq(IntLit(1), IntLit(2)), Cons(Ident("quote"), IntLit(1))]
        for expression in invalid:
            with self.subTest(expression=expression), contextlib.redirect_stderr(io.StringIO()) as errors:
                self.assertIs(self.evaluate(expression), Nil.getInstance())
                self.assertIn("Error:", errors.getvalue())

    def test_cyclic_form_reports_error(self):
        expression = form("begin", IntLit(1))
        expression.getCdr().setCdr(expression.getCdr())
        with contextlib.redirect_stderr(io.StringIO()) as errors:
            self.assertIs(self.evaluate(expression), Nil.getInstance())
        self.assertIn("cyclic", errors.getvalue())


if __name__ == "__main__":
    unittest.main()

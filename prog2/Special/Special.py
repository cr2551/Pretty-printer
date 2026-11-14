# Special -- Parse tree node strategy for printing special forms

import sys
from contextlib import redirect_stdout
from io import StringIO
from abc import ABC, abstractmethod

# There are several different approaches for how to implement the Special
# hierarchy.  We'll discuss some of them in class.  The easiest solution
# is to not add any fields and to use empty constructors.

from Tree import Nil, Cons


class FormError(Exception):
    """Invalid special-form syntax."""


class Special(ABC):
    util = None
    @abstractmethod
    def print(self, t, n, p):
        pass

    @staticmethod
    def list_parts(t):
        """Return the elements and the final nil or dotted tail."""
        items = []
        while t.isPair():
            items.append(t.getCar())
            t = t.getCdr()
        return items, t

    @staticmethod
    def regular_text(t):
        """Format data without invoking special-form printing strategies."""
        if t.isPair():
            items, tail = Special.list_parts(t)
            text = " ".join(Special.regular_text(item) for item in items)
            if not tail.isNull():
                text += " . " + Special.regular_text(tail)
            return "(" + text + ")"

        # Existing leaf print methods append a newline. Capture their output
        # so list elements can share one line without changing the Tree files.
        output = StringIO()
        with redirect_stdout(output):
            t.print(0)
        return output.getvalue().removesuffix("\n")

    @staticmethod
    def application_text(t, n):
        """Format list elements through their strategies, preserving blocks."""
        items, tail = Special.list_parts(t)
        parts = []
        for item in items:
            output = StringIO()
            with redirect_stdout(output):
                item.print(n + 2)
            text = output.getvalue()[n + 2:].removesuffix("\n")
            # A block finishes its own line before the next list element.
            parts.append(text + "\n" if "\n" in text else text)
        text = " ".join(parts)
        if not tail.isNull():
            text += " . " + Special.regular_text(tail)
        return "(" + text + ")"

    @staticmethod
    def write_text(text, n, p=False):
        """Write one expression; p means its opening '(' is already printed."""
        if p and text.startswith("("):
            text = text[1:]
        sys.stdout.write(" " * n + text + "\n")

    @classmethod
    def setUtil(cls, u):
        cls.util = u

    def eval(self, t, env):
        """Evaluate a complete form; leave errors from called code untouched."""
        try:
            return self._eval(t, env)
        except FormError as exc:
            self._error(str(exc))
            return Nil.getInstance()

    def _eval(self, t, env):
        raise NotImplementedError("special form has no evaluator")

    @staticmethod
    def _require(condition, message):
        if not condition:
            raise FormError(message)

    @staticmethod
    def _items(value, context):
        """Read a proper list without looping on a mutated cyclic list."""
        result = []
        seen = set()
        while value.isPair():
            if id(value) in seen:
                raise FormError(context + ": cyclic list")
            seen.add(id(value))
            result.append(value.getCar())
            value = value.getCdr()
        if not value.isNull():
            raise FormError(context + ": expected a proper list")
        return result

    def _operands(self, t, name, minimum, maximum=None):
        operands = self._items(t.getCdr(), name)
        self._require(len(operands) >= minimum and
                      (maximum is None or len(operands) <= maximum),
                      name + ": wrong number of operands")
        return operands

    @staticmethod
    def _truth(value):
        from Tree import BoolLit
        return value is not BoolLit.getInstance(False)

    @staticmethod
    def _sequence(expressions, env):
        result = Nil.getInstance()
        for expression in expressions:
            result = expression.eval(env)
        return result

    @staticmethod
    def _list(values):
        result = Nil.getInstance()
        for value in reversed(values):
            result = Cons(value, result)
        return result

    def _parameters(self, params):
        """Accept fixed, dotted-rest, or symbol-only lambda parameters."""
        names = set()
        seen = set()
        while params.isPair():
            self._require(id(params) not in seen, "lambda: cyclic parameters")
            seen.add(id(params))
            parameter = params.getCar()
            self._require(parameter.isSymbol(), "lambda: parameter must be a symbol")
            name = parameter.getName()
            self._require(name not in names, "lambda: duplicate parameter " + name)
            names.add(name)
            params = params.getCdr()
        if not params.isNull():
            self._require(params.isSymbol(), "lambda: invalid rest parameter")
            self._require(params.getName() not in names,
                          "lambda: duplicate rest parameter " + params.getName())

    def _error(self, msg):
        sys.stderr.write("Error: " + msg + "\n")
        sys.stderr.flush()

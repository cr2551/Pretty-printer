# Define -- Parse tree node strategy for printing the special form define

from Special import Special
from Tree import Ident, Cons, Nil


class Define(Special):
    def print(self, t, n, p):
        items, tail = self.list_parts(t)
        if not tail.isNull() or len(items) < 2 or not items[1].isPair():
            # Variable definitions and malformed forms use regular notation.
            self.write_text(self.application_text(t, n), n, p)
            return

        # Keep define and the function signature together on the first line.
        header = "(" + self.regular_text(items[0]) + " " + self.regular_text(items[1])
        self.write_text(header, n, p)
        for item in items[2:]:
            # Preserve nested special formatting, as in the factorial example.
            item.print(n + 2)
        self.write_text(")", n)

    def _eval(self, t, env):
        from Tree import Closure
        operands = self._operands(t, "define", 2)
        target = operands[0]
        if target.isSymbol():
            self._require(len(operands) == 2, "define: expected one value expression")
            env.define(target, operands[1].eval(env))
        else:
            self._require(target.isPair(), "define: invalid definition target")
            name = target.getCar()
            self._require(name.isSymbol(), "define: function name must be a symbol")
            params = target.getCdr()
            self._parameters(params)
            function = Cons(Ident("lambda"), Cons(params, t.getCdr().getCdr()))
            # Capture the live environment so recursive definitions can find themselves.
            env.define(name, Closure(function, env))
        return Nil.getInstance()

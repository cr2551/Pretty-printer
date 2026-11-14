# Let -- Parse tree node strategy for printing the special form let

from Special import Special
from Tree import Environment


class Let(Special):
    def print(self, t, n, p):
        items, tail = self.list_parts(t)
        if not tail.isNull():
            # Preserve improper lists used as data without losing their tail.
            self.write_text(self.regular_text(t), n, p)
            return

        self.write_text("(" + self.regular_text(items[0]), n, p)
        for item in items[1:]:
            item.print(n + 2)
        self.write_text(")", n)

    def _eval(self, t, env):
        operands = self._operands(t, "let", 2)
        bindings = self._items(operands[0], "let bindings")
        checked = []
        names = set()
        for binding in bindings:
            pair = self._items(binding, "let binding")
            self._require(len(pair) == 2, "let: binding needs a name and value")
            name, expression = pair
            self._require(name.isSymbol(), "let: binding name must be a symbol")
            self._require(name.getName() not in names, "let: duplicate binding")
            names.add(name.getName())
            checked.append((name, expression))
        # Ordinary let initializers all run in the outer environment, not the new frame.
        values = [(name, expression.eval(env)) for name, expression in checked]
        local = Environment(env)
        for name, value in values:
            local.define(name, value)
        return self._sequence(operands[1:], local)

# Cond -- Parse tree node strategy for printing the special form cond

from Special import Special
from Tree import Nil


class Cond(Special):
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
        clauses = self._operands(t, "cond", 0)
        checked = []
        for index, clause in enumerate(clauses):
            parts = self._items(clause, "cond clause")
            self._require(bool(parts), "cond: empty clause")
            test = parts[0]
            is_else = test.isSymbol() and test.getName() == "else"
            if is_else:
                self._require(index == len(clauses) - 1, "cond: else must be last")
                self._require(len(parts) > 1, "cond: else needs a body")
            checked.append((parts, is_else))
        for parts, is_else in checked:
            if is_else:
                return self._sequence(parts[1:], env)
            value = parts[0].eval(env)
            if self._truth(value):
                # A clause with just a test returns the test's value.
                return self._sequence(parts[1:], env) if len(parts) > 1 else value
        return Nil.getInstance()

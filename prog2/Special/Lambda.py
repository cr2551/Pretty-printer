# Lambda -- Parse tree node strategy for printing the special form lambda

from Special import Special
from Tree import Closure


class Lambda(Special):
    def print(self, t, n, p):
        items, tail = self.list_parts(t)
        if not tail.isNull() or len(items) < 2:
            # Preserve incomplete or improper forms when they occur as data.
            self.write_text(self.regular_text(t), n, p)
            return

        # Keep lambda and its parameters (a list or identifier) together.
        header = "(" + self.regular_text(items[0]) + " " + self.regular_text(items[1])
        self.write_text(header, n, p)
        for item in items[2:]:
            item.print(n + 2)
        self.write_text(")", n)

    def _eval(self, t, env):
        operands = self._operands(t, "lambda", 2)
        self._parameters(operands[0])
        # Store the entire lambda expression, as Closure.getFun expects.
        return Closure(t, env)

# If -- Parse tree node strategy for printing the special form if

from Special import Special
from Tree import Nil


class If(Special):
    def print(self, t, n, p):
        items, tail = self.list_parts(t)
        if not tail.isNull() or len(items) < 2:
            # Preserve incomplete or improper forms when they occur as data.
            self.write_text(self.regular_text(t), n, p)
            return

        # Keep the keyword and test expression together on the first line.
        header = "(" + self.regular_text(items[0]) + " " + self.regular_text(items[1])
        self.write_text(header, n, p)
        for item in items[2:]:
            item.print(n + 2)
        self.write_text(")", n)

    def _eval(self, t, env):
        operands = self._operands(t, "if", 2, 3)
        if self._truth(operands[0].eval(env)):
            return operands[1].eval(env)
        if len(operands) == 3:
            return operands[2].eval(env)
        return Nil.getInstance()

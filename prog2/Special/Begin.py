# Begin -- Parse tree node strategy for printing the special form begin

from Special import Special


class Begin(Special):
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
        return self._sequence(self._operands(t, "begin", 0), env)

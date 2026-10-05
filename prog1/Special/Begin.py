# Begin -- Parse tree node strategy for printing the special form begin

from Special import Special

class Begin(Special):
    def print(self, t, n, p):
        items, tail = self.list_parts(t)
        if not tail.isNull():
            # Preserve improper lists used as data without losing their tail.
            self.write_text(self.regular_text(t), n, p)
            return

        lines = ["(" + self.regular_text(items[0])]
        for item in items[1:]:
            # The assignment prints begin's subexpressions as regular lists.
            lines.append(" " * (n + 2) + self.regular_text(item))
        lines.append(" " * n + ")")
        self.write_text("\n".join(lines), n, p)

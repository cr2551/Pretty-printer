# Lambda -- Parse tree node strategy for printing the special form lambda

from Special import Special

class Lambda(Special):
    def print(self, t, n, p):
        items, tail = self.list_parts(t)
        if not tail.isNull() or len(items) < 2:
            # Preserve incomplete or improper forms when they occur as data.
            self.write_text(self.regular_text(t), n, p)
            return

        # Keep lambda and its parameters (a list or identifier) together.
        lines = ["(" + self.regular_text(items[0]) + " " +
                 self.regular_text(items[1])]
        for item in items[2:]:
            lines.append(" " * (n + 2) + self.regular_text(item))
        lines.append(" " * n + ")")
        self.write_text("\n".join(lines), n, p)

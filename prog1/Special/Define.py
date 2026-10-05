# Define -- Parse tree node strategy for printing the special form define

from Special import Special

class Define(Special):
    def print(self, t, n, p):
        items, tail = self.list_parts(t)
        if not tail.isNull() or len(items) < 2 or not items[1].isPair():
            # Variable definitions and malformed forms use regular notation.
            self.write_text(self.regular_text(t), n, p)
            return

        # Keep define and the function signature together on the first line.
        header = "(" + self.regular_text(items[0]) + " " + self.regular_text(items[1])
        self.write_text(header, n, p)
        for item in items[2:]:
            # Preserve nested special formatting, as in the factorial example.
            item.print(n + 2)
        self.write_text(")", n)

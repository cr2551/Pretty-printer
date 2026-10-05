# Set -- Parse tree node strategy for printing the special form set!

from Special import Special

class Set(Special):
    def print(self, t, n, p):
        # Assignments use the same single-line layout as regular lists.
        self.write_text(self.regular_text(t), n, p)


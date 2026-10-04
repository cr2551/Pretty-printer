# Regular -- Parse tree node strategy for printing regular lists

from Special import Special

class Regular(Special):
    def print(self, t, n, p):
        # Print all elements on one line, including nested and dotted lists.
        self.write_text(self.regular_text(t), n, p)

# Quote -- Parse tree node strategy for printing the special form quote

from Special import Special

class Quote(Special):
    def print(self, t, n, p):
        items, tail = self.list_parts(t)
        if not p and tail.isNull() and len(items) == 2:
            # Quoted special forms are data, so suppress special formatting.
            text = "'" + self.regular_text(items[1])
        else:
            # Preserve malformed quote lists and close any existing '('.
            text = self.regular_text(t)
        self.write_text(text, n, p)

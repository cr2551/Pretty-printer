# Special -- Parse tree node strategy for printing special forms

import sys
from contextlib import redirect_stdout
from io import StringIO
from abc import ABC, abstractmethod

# There are several different approaches for how to implement the Special
# hierarchy.  We'll discuss some of them in class.  The easiest solution
# is to not add any fields and to use empty constructors.

class Special(ABC):
    @abstractmethod
    def print(self, t, n, p):
        pass

    @staticmethod
    def list_parts(t):
        """Return the elements and the final nil or dotted tail."""
        items = []
        while t.isPair():
            items.append(t.getCar())
            t = t.getCdr()
        return items, t

    @staticmethod
    def regular_text(t):
        """Format data without invoking special-form printing strategies."""
        if t.isPair():
            items, tail = Special.list_parts(t)
            text = " ".join(Special.regular_text(item) for item in items)
            if not tail.isNull():
                text += " . " + Special.regular_text(tail)
            return "(" + text + ")"

        # Existing leaf print methods append a newline. Capture their output
        # so list elements can share one line without changing the Tree files.
        output = StringIO()
        with redirect_stdout(output):
            t.print(0)
        return output.getvalue().removesuffix("\n")

    @staticmethod
    def write_text(text, n, p=False):
        """Write one expression; p means its opening '(' is already printed."""
        if p and text.startswith("("):
            text = text[1:]
        sys.stdout.write(" " * n + text + "\n")

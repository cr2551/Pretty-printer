# Cons -- Parse tree node class for representing a Cons node

from Tree import Node
from Tree import Ident

from Tokens import TokenType
from Special import *
class Cons(Node):
    def __init__(self, a, d):
        self.car = a
        self.cdr = d
        self.parseList()

    # parseList() `parses' special forms, constructs an appropriate
    # object of a subclass of Special, and stores a pointer to that
    # object in variable form.  It would be possible to fully parse
    # special forms at this point.  Since this causes complications
    # when using (incorrect) programs as data, it is easiest to let
    # parseList only look at the car for selecting the appropriate
    # object from the Special hierarchy and to leave the rest of
    # parsing up to the interpreter.
    def parseList(self):
        # TODO: implement this function and any helper functions
        # you might need
        self.form = self.choose_form(self.car)

    def print(self, n, p=False):
        self.form.print(self, n, p)

    def choose_form(self, a):
        if a.get_type() == TokenType.IDENT:
            if a.getName() == "set":
                return Set()
            elif a.getName() == "define":
                return Define()
            elif a.getName() == "if":
                return If()
            elif a.getName() == "lambda":
                return Lambda()
            elif a.getName() == "begin":
                return Begin()
            elif a.getName() == "cond":
                return Cond()
            elif a.getName() == "let":
                return Let()
            elif a.getName() == "quote":
                return Quote()
            
        return Regular()

if __name__ == "__main__":
    c = Cons(Ident("Hello"), Ident("World"))
    c.print(0)

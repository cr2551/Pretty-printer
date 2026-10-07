# Cons -- Parse tree node class for representing a Cons node

from Tree import Node
from Tree.Ident import Ident

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
        self.form = self.choose_form()

    def print(self, n, p=False):
        self.form.print(self, n, p)

    def choose_form(self):

        car = self.getCar()
        if car.isSymbol():
            if car.name == "set!":
                return Set()
            elif car.name == "define":
                return Define()
            elif car.name == "if":
                return If()
            elif car.name == "lambda":
                return Lambda()
            elif car.name == "begin":
                return Begin()
            elif car.name == "cond":
                return Cond()
            elif car.name == "let":
                return Let()
            elif car.name == "quote":
                return Quote()
                
        return Regular()

    def getCar(self):
        return self.car


    def getCdr(self):
        return self.cdr

    def setCar(self, a):
        self.car = a
        self.parseList()

    def setCdr(self, d):
        self.cdr = d

    def isPair(self):
        return True


if __name__ == "__main__":
    c = Cons(Ident("Hello"), Ident("World"))
    c.print(0)

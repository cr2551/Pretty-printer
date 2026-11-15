# Closure -- the data structure for function closures

# Class Closure is used to represent the value of lambda expressions.
# It consists of the lambda expression itself, together with the
# environment in which the lambda expression was evaluated.

# The method apply() takes the environment out of the closure,
# adds a new frame for the function call, defines bindings for the
# parameters with the argument values in the new frame, and evaluates
# the function body.

import sys
from Tree import Node
from Tree import Environment
from Tree import StrLit
from Tree import Nil

class Closure(Node):
    util = None

    @classmethod
    def setUtil(cls, u):
        cls.util = u

    def __init__(self, f, e):
        self.fun = f                    # a lambda expression
        self.env = e                    # the environment in which
                                        # the function was defined

    def getFun(self):
        return self.fun

    def getEnv(self):
        return self.env

    def isProcedure(self):
        return True

    def print(self, n, p=False):
        for _ in range(n):
            sys.stdout.write(' ')
        sys.stdout.write("#{Procedure")
        if self.fun != None:
            self.fun.print(abs(n) + 4)
        for _ in range(abs(n)):
            sys.stdout.write(' ')
        sys.stdout.write(" }\n")
        sys.stdout.flush()

    def eval(self, env):
        return self

    # Done: The method apply() should be defined in class Node
    # to report an error.  It should be overridden only in classes
    # BuiltIn and Closure.
    # needs more work
    def apply(self, args):
        # return StrLit("Error: Closure.apply not yet implemented")
        enclosing_scope = self.getEnv()
        func = self.getFun()
        inner_scope = Environment(enclosing_scope) # add a new frame for the function call
        params = func.getCdr().getCar() # get parameters of the lambda expression
        body = func.getCdr().getCdr() # get the body of the lambda

        # bind each parameter to the corresponding argument in the new frame
        # walk list of parameters and arguments to bind them in the new environment
        while params.isPair() and args.isPair():
            inner_scope.define(params.getCar(), args.getCar())
            params = params.getCdr()
            args = args.getCdr()

        if params.isSymbol():
            inner_scope.define(params, args)
        # if there are remaining parameters but no arguments, it's an error
        elif params.isPair():
            self._error("wrong number of arguments")
        # if there are still arguments but no parameters, it's an error
        elif params.isNull() and args.isPair():
            self._error("wrong number of arguments")
            

        # evaluate the function
        result = Nil.getInstance() 
        while body.isPair():
            expr = body.getCar()
            result = expr.eval(inner_scope)
            body = body.getCdr()
        return result
        

        


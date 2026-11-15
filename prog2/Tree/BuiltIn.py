# BuiltIn -- the data structure for built-in functions

# Class BuiltIn is used for representing the value of built-in functions
# such as +.  Populate the initial environment with
# (name, BuiltIn(name)) pairs.

# The object-oriented style for implementing built-in functions would be
# to include the Python methods for implementing a Scheme built-in in the
# BuiltIn object.  This could be done by writing one subclass of class
# BuiltIn for each built-in function and implementing the method apply
# appropriately.  This requires a large number of classes, though.
# Another alternative is to program BuiltIn.apply() in a functional
# style by writing a large if-then-else chain that tests the name of
# the function symbol.

import math
import sys
from Parse import *
from Tree import Node
from Tree import BoolLit
from Tree import IntLit
from Tree import StrLit
from Tree import Ident
from Tree import Nil
from Tree import Cons
from Tree import TreeBuilder
from Tree import Unspecific
from Parse import Scanner, Parser

class BuiltIn(Node):
    env = None
    util = None

    @classmethod
    def setEnv(cls, e):
        cls.env = e

    @classmethod
    def setUtil(cls, u):
        cls.util = u


    def __init__(self, s):
        self.symbol = s    # the Ident for the built-in function

    def getSymbol(self):
        return self.symbol

    def isProcedure(self):
        return True

    def print(self, n, p=False):
        for _ in range(n):
            sys.stdout.write(' ')
        sys.stdout.write("#{Built-In Procedure ")
        if self.symbol != None:
            self.symbol.print(-abs(n) - 1)
        sys.stdout.write('}')
        if n >= 0:
            sys.stdout.write('\n')
            sys.stdout.flush()

    def eval(self, env):
        return self

    # DONE: The method apply() should be defined in class Node
    # to report an error.  It should be overridden only in classes
    # BuiltIn and Closure.
    def apply(self, args):
        ## The easiest way to implement BuiltIn.apply is as an
        ## if-then-else chain testing for the different names of
        ## the built-in functions.  E.g., here's how load could
        ## be implemented:
        name = self.getSymbol().getName()
        arg1 = None
        rest = Nil.getInstance()
        if args.isPair():
            arg1 = args.getCar()
            rest = args.getCdr()
        arg2 = None
        if rest is not None and rest.isPair():
            arg2 = rest.getCar()
    
        
    
        if name == "load":
            if arg1 is None:
                self._error("wrong number of arguments")
                return Nil.getInstance()
            if not arg1.isString():
                self._error("wrong type of argument")
                return Nil.getInstance()
            filename = arg1.strVal
            try:
                scanner = Scanner(open(filename))
                builder = TreeBuilder()
                parser = Parser(scanner, builder)

                root = parser.parseExp()
                while root != None:
                    root.eval(BuiltIn.env)
                    root = parser.parseExp()
            except IOError:
                self._error("could not find file " + filename)
            return Nil.getInstance()  # or Unspecific.getInstance()


        # elif name == "b+":
        #     if arg1 is None and arg2 is None:
        #         self._error("b+ expects two arguments")
        #         return Nil.getInstance()
        #     if arg1.isNumber() and arg2.isNumber():
        #         return IntLit(arg1.intVal + arg2.intVal)
        #     self.__error("b+ expects two numbers")
        #     return Nil.getInstance()
        
        # elif name == "b-":
        #     pass
        # elif name == "b*":
        #     pass
        # elif name == "b/":
        #     pass
        # elif name == "b=":
        #     pass
        # elif name == "b<":
        #     pass

        elif name in ("b+", "b-", "b*", "b/", "b=", "b<"):
            if arg1 is None or arg2 is None or not arg1.isNumber() or not arg2.isNumber():
                self._error("expects 2 numbers")
                return Nil.getInstance()
            op = name[1]
            if op == "=":
                val = eval(f"{arg1.intVal} {op*2} {arg2.intVal}")
                return BoolLit.getInstance(val)
            elif op == "/":
                if arg2.intVal == 0:
                    self._error("division by zero")
                    return Nil.getInstance()
                val = eval(f"{arg1.intVal} {op} {arg2.intVal}")
            elif op == "<":
                val = eval(f"{arg1.intVal} {op} {arg2.intVal}")
                return BoolLit.getInstance(val)
            else:
                val = eval(f"{arg1.intVal} {op} {arg2.intVal}")
            return IntLit(val)

        # Built-in type checks
        elif name == "number?":
            if arg1 is not None:
                return BoolLit.getInstance(arg1.isNumber())
            self._error("number expects an argument")
            return Nil.getInstance()
        elif name == "symbol?":
            if arg1 is not None:
                return BoolLit.getInstance(arg1.isSymbol())
            self._error("symbol? expects an argument")
            return Nil.getInstance()
        elif name == "pair?":
            if arg1 is not None:
                return BoolLit.getInstance(arg1.isPair())
            self._error("pair? expects an argument")
            return Nil.getInstance()
        # list operations
        elif name == "car":
            if arg1 is not None and arg1.isPair():
                return arg1.car
            self._error("car expects a pair")
            return Nil.getInstance()
        elif name == "cdr":
            if arg1 is not None and arg1.isPair():
                return arg1.cdr
            self._error("cdr expects a pair")
            return Nil.getInstance()
        elif name == "cons":
            if arg1 is not None and arg2 is not None:
                return Cons(arg1, arg2)
            self._error("cons expects 2 arguments")
            return Nil.getInstance()
        #  set-car!, set-cdr!, null?, pair?, eq?
        elif name == "set-car!":
            if arg1 is not None and arg1.isPair() and arg2 is not None:
                arg1.setCar(arg2)
                return Nil.getInstance()
            self._error("set-car! expects a pair and a value")
            return Nil.getInstance()
        elif name == "set-cdr!":
            if arg1 is not None and arg1.isPair() and arg2 is not None:
                arg1.setCdr(arg2)
                return Nil.getInstance()
            self._error("set-cdr! expects a pair and a value")
            return Nil.getInstance()
        elif name == "null?":
            if arg1 is not None:
                return BoolLit.getInstance(arg1.isNull())
            self._error("wrong number of arguments to procedure (null?)")
            return Nil.getInstance()

        elif name == "eq?":
            if arg1 is not None and arg2 is not None:
                if arg1.isSymbol() and arg2.isSymbol():
                    return BoolLit.getInstance(arg1.getName() == arg2.getName())
                return BoolLit.getInstance(arg1 is arg2)
            self._error("eq? expects 2 arguments")
            return Nil.getInstance()
        
        elif name == "procedure?":
            if arg1 is not None:
                return BoolLit.getInstance(arg1.isProcedure())
            self._error("procedure? expects an argument")
            return Nil.getInstance()

        # I/O:  read, write, display, newline
        elif name == "read": # parse one s-expression from stdin
            parser = Parser(Scanner(sys.stdin), TreeBuilder())
            root = parser.parseExp()
            return root if root is not None else Ident("end-of-file")
        elif name == "write": # write takes an optional second argument (port)
            # which we ignore
            if arg1 is None:
                self._error("write expects an argument")
                return Unspecific.getInstance()
            arg1.print(-1)
            sys.stdout.flush()
            return Unspecific.getInstance()
        elif name == "display":
            if arg1 is None:
                self._error("display expects an argument")
                return Unspecific.getInstance()
            arg1.print(-1)
            return Unspecific.getInstance()
        elif name == "newline":
            sys.stdout.write("\n")
            return Unspecific.getInstance()
        
        # Implement eval, apply and interaction-environment
        # (eval expression environment-specifier)
        elif name == "eval":
            if arg1 is None:
                self._error("eval expects an expression")
                return Nil.getInstance()
            if arg2 is not None and arg2.isEnvironment():
                env = arg2
            else:
                env = BuiltIn.env
            return arg1.eval(env)
        # the 'apply' procedure calls a function by unpacking a list
        # of values so that they are passed as individual arguments to the function
        # (apply procedure [arg1] [arg2]...argument-list)
        elif name == "apply":
        
            if arg1 is not None and arg1.isProcedure():
                proc = arg1
            else:
                self._error("apply expects a procedure")
                return Nil.getInstance()
            if arg2 is None or not (arg2.isPair() or arg2.isNull()):
                self._error("apply expects an argument list")
                return Nil.getInstance()
            return proc.apply(arg2) # right now it it only accepts the following syntax
            # (apply procedure argument-list)


        elif name == "interaction-environment":
            return BuiltIn.env
        else:
            self._error("unknown built-in function: " + name)
            return Nil.getInstance()

        

        







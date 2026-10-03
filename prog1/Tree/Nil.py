# Nil -- Parse tree node class for representing the empty list

import sys
from Tree import Node

class Nil(Node):
    __instance = None

    @staticmethod
    def getInstance():
        if Nil.__instance == None:
            Nil()
        return Nil.__instance

    def __init__(self):
        if Nil.__instance != None:
            raise Exception("Class Nil is a singleton")
        else:
            Nil.__instance = self

    def print(self, n, p=False):
        # There got to be a more efficient way to print n spaces.
        for _ in range(n):
            sys.stdout.write(' ')
        if p:
            sys.stdout.write(")\n")
        else:
            sys.stdout.write("()\n")

if __name__ == "__main__":
    n = Nil.getInstance()
    n.print(0)

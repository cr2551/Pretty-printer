# IntLit -- Parse tree node class for representing integer literals

import sys
from Tree import Node

class IntLit(Node):
    def __init__(self, i):
        self.intVal = i

    def print(self, n, p=False):
        # There got to be a more efficient way to print n spaces.
        for _ in range(n):
            sys.stdout.write(' ')
        sys.stdout.write(str(self.intVal) + '\n')

if __name__ == "__main__":
    id = IntLit(42)
    id.print(0)

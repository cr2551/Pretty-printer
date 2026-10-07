# StLit -- Parse tree node class for representing string literals

import sys
from Tree import Node

class StrLit(Node):
    def __init__(self, s):
        self.strVal = s

    def print(self, n, p=False):
        escaped = self.strVal.replace("\\", "\\\\").replace('"', '\\"')
        sys.stdout.write(" " * n + '"' + escaped + '"\n')

    def isString(self):
        return True

if __name__ == "__main__":
    id = StrLit("foo")
    id.print(0)

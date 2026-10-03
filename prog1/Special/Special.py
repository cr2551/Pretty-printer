# Special -- Parse tree node strategy for printing special forms

from abc import ABC, abstractmethod

# There are several different approaches for how to implement the Special
# hierarchy.  We'll discuss some of them in class.  The easiest solution
# is to not add any fields and to use empty constructors.

class Special(ABC):
    @abstractmethod
    def print(self, t, n, p):
        pass

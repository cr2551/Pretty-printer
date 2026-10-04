# Regular -- Parse tree node strategy for printing regular lists

from Special import Special

class Regular(Special):
    # TODO: Add fields and modify the constructor as needed.
    def __init__(self):
        ...

    def print(self, t, n, p):
        # TODO: Implement this function.
        if p == False:
            print('(', end='')

        t.car.print(n, p)
        

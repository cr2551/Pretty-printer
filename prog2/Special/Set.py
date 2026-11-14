# Set -- Parse tree node strategy for printing the special form set!

from Special import Special
from Tree import Nil


class Set(Special):
    def print(self, t, n, p):
        # Assignments use regular-list layout, preserving nested special forms.
        self.write_text(self.application_text(t, n), n, p)

    def _eval(self, t, env):
        target, expression = self._operands(t, "set!", 2, 2)
        self._require(target.isSymbol(), "set!: target must be a symbol")
        env.assign(target, expression.eval(env))
        return Nil.getInstance()

# Regular -- Parse tree node strategy for printing regular lists

from Special import Special


class Regular(Special):
    def print(self, t, n, p):
        # Keep ordinary elements inline while preserving nested special forms.
        self.write_text(self.application_text(t, n), n, p)

    def _eval(self, t, env):
        expressions = self._items(t, "function call")
        self._require(bool(expressions), "function call: missing operator")
        procedure = expressions[0].eval(env)
        self._require(procedure.isProcedure(), "function call: operator is not a procedure")
        values = [expression.eval(env) for expression in expressions[1:]]
        return procedure.apply(self._list(values))

# Parser -- recursive descent over expressions and proper/dotted lists.

import sys
from Tokens import TokenType
from Tree import Cons, Ident, IntLit, StrLit, BoolLit, Nil


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.had_error = False

    def parseExp(self):
        # Consume only this expression, not the next expression's first token.
        tok = self.scanner.getNextToken()
        while tok is not None and tok.getType() in (TokenType.DOT, TokenType.RPAREN):
            self.had_error = True
            sys.stderr.write("Parse error: unexpected " + tok.getType().name + "\n")
            tok = self.scanner.getNextToken()
        if tok is None:
            return None
        return self.parseExpHelper(tok)

    def parseExpHelper(self, tok):
        if tok is None:
            raise SyntaxError("Expected expression before EOF")
        tt = tok.getType()
        if tt == TokenType.LPAREN:
            return self.parseRest()
        if tt == TokenType.QUOTE:
            value = self.parseExpHelper(self.scanner.getNextToken())
            return Cons(Ident("quote"), Cons(value, Nil.getInstance()))
        if tt == TokenType.TRUE:
            return BoolLit.getInstance(True)
        if tt == TokenType.FALSE:
            return BoolLit.getInstance(False)
        if tt == TokenType.INT:
            return IntLit(tok.getIntVal())
        if tt == TokenType.STR:
            return StrLit(tok.getStrVal())
        if tt == TokenType.IDENT:
            return Ident(tok.getName())
        raise SyntaxError("Expected expression, found " + tt.name)

    def parseRest(self):
        return self.parseRestHelper(self.scanner.getNextToken())

    def parseRestHelper(self, tok):
        # Iterate over siblings to support long lists without deep recursion.
        items = []
        while True:
            if tok is None:
                raise SyntaxError("Expected ')' before EOF")
            tt = tok.getType()
            if tt == TokenType.RPAREN:
                tail = Nil.getInstance()
                break
            if tt == TokenType.DOT:
                if not items:
                    raise SyntaxError("Dot must follow a list element")
                tail = self.parseExpHelper(self.scanner.getNextToken())
                closing = self.scanner.getNextToken()
                if closing is None or closing.getType() != TokenType.RPAREN:
                    raise SyntaxError("Expected ')' after dotted tail")
                break
            items.append(self.parseExpHelper(tok))
            tok = self.scanner.getNextToken()
        for item in reversed(items):
            tail = Cons(item, tail)
        return tail

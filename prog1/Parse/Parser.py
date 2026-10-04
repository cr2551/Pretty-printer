# Parser -- the parser for the Scheme printer and interpreter
#
# Defines
#
#   class Parser
#
# Parses the language
#
#   exp  ->  ( rest
#         |  #f
#         |  #t
#         |  ' exp
#         |  integer_constant
#         |  string_constant
#         |  identifier
#    rest -> )
#         |  exp+ [. exp] )
#
# and builds a parse tree.  Lists of the form (rest) are further
# `parsed' into regular lists and special forms in the constructor
# for the parse tree node class Cons.  See Cons.parseList() for
# more information.
#
# The parser is implemented as an LL(0) recursive descent parser.
# I.e., parseExp() expects that the first token of an exp has not
# been read yet.  If parseRest() reads the first token of an exp
# before calling parseExp(), that token must be put back so that
# it can be re-read by parseExp() or an alternative version of
# parseExp() must be called.
#
# If EOF is reached (i.e., if the scanner returns None instead of a token),
# the parser returns None instead of a tree.  In case of a parse error, the
# parser discards the offending token (which probably was a DOT
# or an RPAREN) and attempts to continue parsing with the next token.

import sys
from Tokens import TokenType

from Tree import * # added

class Parser:
    def __init__(self, s):
        self.scanner = s

    def parseExp(self):
        tok = None
        return self.parseExpHelper(tok)

    def parseExpHelper(self, tok):
        # TODO: write code for parsing an exp
        if tok == None:
            tok = self.scanner.getNextToken()
            if tok is None:
                return None
        tt = tok.getType()

        if tt == TokenType.LPAREN:
            return self.parseRest()
        elif tt == TokenType.TRUE:
            return BoolLit.getInstance(True)
        elif tt == TokenType.FALSE:
            return BoolLit.getInstance(False)
        elif tt == TokenType.QUOTE:
            cons = Cons(Ident("quote"), Cons(self.parseExp(), Nil.getInstance()))
            return cons
        elif tt == TokenType.INT:
            return IntLit(tok.getIntVal())
        elif tt == TokenType.STR:
            return StrLit(tok.getStrVal())
        elif tt == TokenType.IDENT:
            return Ident(tok.getName())
        return None

    def parseRest(self):
        tok = None
        return self.parseRestHelper(tok)


    def parseRestHelper(self, tok):
        # TODO: write code for parsing a rest
        if tok == None:
            tok = self.scanner.getNextToken()
            if tok is None:
                return None

        tt = tok.getType()
        if tt == TokenType.RPAREN:
            return Nil.getInstance()
        
        else:
            exp = self.parseExpHelper(tok)
            tok = self.scanner.getNextToken()
            if tok.getType() == TokenType.DOT:
                cons =  Cons(exp, self.parseExp())
                next = self.scanner.getNextToken()
                if next is None or next.getType() is not TokenType.RPAREN:
                    self.__error("Expected ')' after '. exp'")
                    
            rest = self.parseRestHelper(tok)
            cons = Cons(exp, rest)
            return cons
        
    


    # TODO: Add any additional methods you might need

    def __error(self, msg):
        sys.stderr.write("Parse error: " + msg + "\n")

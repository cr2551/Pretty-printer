# Scanner -- The lexical analyzer for the Scheme printer and interpreter

import sys
import io
from Tokens import *

class Scanner:
    def __init__(self, i):
        self.In = i
        self.buf = []
        self.ch_buf = None

    def read(self):
        if self.ch_buf == None:
            return self.In.read(1)
        else:
            ch = self.ch_buf
            self.ch_buf = None
            return ch
    
    def peek(self):
        if self.ch_buf == None:
            self.ch_buf = self.In.read(1)
            return self.ch_buf
        else:
            return self.ch_buf

    @staticmethod
    def isDigit(ch):
        return ch >= '0' and ch <= '9'

    @staticmethod
    def _isletter(ch):
        if (ch >= 'A' and ch <= 'Z'):
            return True
        elif (ch >= 'a' and ch <= 'z'):
            return True
        else:
            return False
    @staticmethod
    def _is_special_initial(ch):
        special_initals = ['!', '$', '%', '&', '*', '/', ':', '<', '=', '>', '?', '^', '_', '~']
        if ch in special_initals:
            return True
        else:
            return False
    @staticmethod
    def _is_special_subsequent(ch):
        special_subsequents = ['+', '-', '.', '@']
        if ch in special_subsequents:
            return True
        else:
            return False

    # not being used right now
    @staticmethod
    def _is_peculiar_identifier(ch):
        peculiars = ['+', '-', '...']
        if ch in peculiars:
            return True # MODIFY later
        else:
            return False
        


    def is_valid_initial_ident(self, ch):
        if self._isletter(ch) or self._is_special_initial(ch):
            return True

    def is_valid_subsequent(self, ch):
        if self.is_valid_initial_ident(ch) \
                or self.isDigit(ch) \
                or self._is_special_subsequent(ch):
            return True
        else:
            return False
        # return true if the character is as valid first char for an identifier
        


    def getNextToken(self):
        try:
            # It would be more efficient if we'd maintain our own
            # input buffer for a line and read characters out of that
            # buffer, but reading individual characters from the
            # input stream is easier.
            ch = self.read()

            # TODO: Skip white space and comments
            while ch in [' ', '\t', '\n']:
                ch = self.read()

            if ch == ';':
                while ch != '\n':
                    ch = self.read()
                ch = self.read() # skip the newline too
                

            # Return None on EOF
            if ch == "":
                return None
    
            # Special characters
            elif ch == '\'':
                return Token(TokenType.QUOTE)
            elif ch == '(':
                return Token(TokenType.LPAREN)
            elif ch == ')':
                return Token(TokenType.RPAREN)
            elif ch == '.':
                #  We ignore the special identifier `...'.
                return Token(TokenType.DOT)

            # Boolean constants
            elif ch == '#':
                ch = self.read()

                if ch == 't':
                    return Token(TokenType.TRUE)
                elif ch == 'f':
                    return Token(TokenType.FALSE)
                elif ch == "":
                    sys.stderr.write("Unexpected EOF following #\n")
                    return None
                else:
                    sys.stderr.write("Illegal character '" +
                                     chr(ch) + "' following #\n")
                    return self.getNextToken()

            # String constants
            elif ch == '"':
                self.buf = []
                # TODO: scan a string into the buffer variable buf
                ch = self.read()
                while ch != '"':
                    self.buf.append(ch)
                    ch = self.read()

                return StrToken("".join(self.buf))

            # Integer constants
            elif self.isDigit(ch):
                i = ord(ch) - ord('0')
                # TODO: scan the number and convert it to an integer
                # only for integers > 0
                num = str(i)
                next = self.peek()
                while self.isDigit(next):
                    ch = self.read()
                    num += ch
                    next = self.peek()

                i = int(num)
                
                # make sure that the character following the integer
                # is not removed from the input stream
                return IntToken(i)
    
            # Identifiers
            elif (ch >= 'A' and ch <= 'Z') or self.is_valid_initial_ident(ch):
                # or ch is some other vaid first character
                # for an identifier
                self.buf = []
                self.buf.append(ch)
                # TODO: scan an identifier into the buffer variable buf
                next = self.peek()
                while self.is_valid_subsequent(next):
                    ch = self.read()
                    self.buf.append(ch)
                    next = self.peek()
                name = "".join(self.buf).lower()
                # make sure that the character following the identifier
                # is not removed from the input stream
                return IdentToken(name)

            # Illegal character
            else:
                sys.stderr.write("Illegal input character '" + ch + "'\n")
                return self.getNextToken()

        except IOError:
            sys.stderr.write("IOError: error reading input file\n")
            return None


if __name__ == "__main__":
    scanner = Scanner(sys.stdin)
    tok = scanner.getNextToken()
    tt = tok.getType()
    print(tt)
    if tt == TokenType.INT:
        print(tok.getIntVal())
    elif tt == TokenType.STR:
        print(tok.getStrVal())
    elif tt == TokenType.IDENT:
        print(tok.getName())
    

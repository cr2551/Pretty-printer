# SPP -- The main program of the Scheme pretty printer

import sys
from Parse import *
from Tokens import TokenType

if __name__ == "__main__":
    # Create scanner that reads from standard input
    scanner = Scanner(sys.stdin)
    
    if (len(sys.argv) > 2 or
        (len(sys.argv) == 2 and sys.argv[1] != "-d")):
        sys.stderr.write("Usage: python3 SPP.py [-d]\n")
        sys.exit(2)
    
    # If command line option -d is provided, debug the scanner.
    if len(sys.argv) == 2 and sys.argv[1] == "-d":
        # sys.stdout.write("Scheme 4101> ")
        # sys.stdout.flush()
        tok = scanner.getNextToken()
        while tok != None:
            tt = tok.getType()

            sys.stdout.write(str(tt))
            if tt == TokenType.INT:
                sys.stdout.write(", intVal = " + str(tok.getIntVal()) + "\n")
            elif tt == TokenType.STR:
                sys.stdout.write(", strVal = " + tok.getStrVal() + "\n")
            elif tt == TokenType.IDENT:
                sys.stdout.write(", name = " + tok.getName() + "\n")
            else:
                sys.stdout.write("\n")

            # sys.stdout.write("Scheme 4101> ")
            # sys.stdout.flush()
            tok = scanner.getNextToken()
    else:
        # Create parser
        parser = Parser(scanner)

        # Parse and pretty-print each input expression
        root = parser.parseExp()
        while root != None:
            root.print(0)
            root = parser.parseExp()

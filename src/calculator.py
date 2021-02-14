INTEGER, PLUS, MINUS, MUL, DIV, POW, LPAREN, RPAREN, EOF = "INTEGER", "PLUS", "MINUS", "MUL", "DIV", "POW", "(", ")", "EOF"

###############################################################################
#                                                                             #
#  LEXICAL ANALYZER                                                           #
#                                                                             #
###############################################################################

# Converts String to Token Stream
class Token(object):

    """
    This object holds type and value of a token

    A token is to a command what a word is to a sentence
    """

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token({type}, {value})".format(
            type = repr(self.type),
            value = self.value
        )

    def __repr__(self):
        return self.__str__()

class Lexer(object):

    """
    The Lexical Analyzer turns a stream of Characters into a stream of Tokens by looking at the string and fitting it into a grammar
    """

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception(f"Invalid Character: {self.current_char}")

    def out_of_bounds(self):
        return self.pos >= len(self.text)

    def advance(self):
        """
        Advances Character pointer to next Token
        """
        self.pos += 1

        if self.out_of_bounds():
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """
        Is called if current character is a whitespace
        Calls advance until current character is no longer whitespace.
        """

        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_integer(self):
        """
        Is called when current character is a digit: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9).
        Advances and collects all digits of an integer and parses the intiger using native python functions
        """
        result = ""

        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return int(result)

    def get_operation(self):

        """
        Collects Operators (for consistency)
        """

        if self.current_char == "+":
            self.advance()
            return PLUS, "+"

        if self.current_char == "-":
            self.advance()
            return MINUS, "-"

        if self.current_char == "*":
            self.advance()

            if self.current_char == "*":
                self.advance()
                return POW, "**"
            else:
                return MUL, "*"

        if self.current_char == "/":
            self.advance()
            return DIV, "/"

    def get_next_token(self):
        """
        Continously generates next token.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.get_integer())

            if self.current_char in ("+", "-", "*", "/"):
                token_type, value = self.get_operation()
                return Token(token_type, value)

            if self.current_char == "(":
                self.advance()
                return Token(LPAREN, "(")

            if self.current_char == ")":
                self.advance()
                return Token(RPAREN, ")")

            self.error()

        return Token(EOF, None)

# Data Structure
# ==============================================================================


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

# Turns Token Stream into Tree Structure (Abstract Syntax Tree / AST)

class AST(object):
    pass

class UnaryOp(AST):

    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value #Memory waste


class Parser(object):

    def __init__(self, lexer):

        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Parser Failure: Invalid Syntax.")

    def eat(self, token_type):
        """
        Compares the type of the current token to the expected type and advances to the next token.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            print(self.current_token.type, token_type)
            self.error()

    def factor(self):
        """
        Handles Unary operations and parentheses.

        factor : PLUS factor
           | MINUS factor
           | INTEGER
           | LPAREN expr RPAREN
           | variable
        """
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            return UnaryOp(token, self.factor())

        elif token.type == MINUS:
            self.eat(MINUS)
            return UnaryOp(token, self.factor())

        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)

        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node


    def term(self):

        """
        Handles Multiplication and devision:

        term: factor ((MUL | DIV) factor)*
        """

        node = self.factor()

        while self.current_token.type in (MUL, DIV):

            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node


    def expr(self):

        """
        Handles Binary operations off addition and subtraction.

        expr: term ((PLUS | MINUS) term)*
        """

        # set current token to the first token taken from the input
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):

            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):
        return self.expr()


###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

# Traverses Abstract Syntax Tree and performs actions

class NodeVisitor(object):


    def visit(self, node):
        # Dynamically Call visit type
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit_exception) # Generates name and fetches function with that name
        return visitor(node)


    def generic_visit_exception(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):

    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):

        # For Negative Numbers
        #if node.left is None:
        #    node.left = Num(Token(INTEGER, 0))

        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == POW:
            return self.visit(node.left) ** self.visit(node.right)

    def visit_UnaryOp(self, node):

        op = node.op.type

        if op == PLUS:
            return self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        head = self.parser.parse()
        return self.visit(head)


def test_calc():
    tests = {
        "3 + 2 - 1": 4,
        "56 / 2 - 4": 24,
        "4 - 56 / 2": -24,
        "2 / 20 * 2": 0.2,
        "(2 + 3) / 2": 2.5,
        "(3 - (2 + 3)) * 2": -4,
        "(2*2) / (32 - 30) - 3": -1,
        "-1+3*(-5+2)": -10,
        "--3": 3,
        "(5--16)*10/2": 105
    }

    for test in tests:
        lexer = Lexer(test)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        print(f"Testing {test} = {tests[test]}")
        assert interpreter.interpret() == tests[test]

    print("ALL TESTS PASSED!")

def main():

    from sys import argv

    if argv[1] == "-t":
        test_calc()
        return

    for command in argv[1:]:
        print(f"{command} = ", end = "")
        lexer = Lexer(command)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()

        print(result)

if __name__ == '__main__':
    main()

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
    The Lexical Analyzer turns a stream of Tokens into an abstract Syntax tree by looking at the Token and fitting into a grammar
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

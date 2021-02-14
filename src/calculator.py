INTEGER, PLUS, MINUS, MUL, DIV, POW, LPAREN, RPAREN, EOF = "INTEGER", "PLUS", "MINUS", "MUL", "DIV", "POW", "(", ")", "EOF"

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

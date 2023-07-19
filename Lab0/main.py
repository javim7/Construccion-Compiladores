'''
Jose Hernandez: 20053
Javier Mombiela: 20067

Laboratorio 0: Generacion de Scanner y Parser
'''

#importando la libreria de antlr4 y el archivo de YAPLLexer y YAPLParser
from antlr4 import *
from YAPLLexer import YAPLLexer
from YAPLParser import YAPLParser

class Compiler():
    def __init__(self, input_file):
        self.input = input_file
        self.input_stream = FileStream(self.input)
        self.lexer = YAPLLexer(self.input_stream)
        self.token_stream = CommonTokenStream(self.lexer)
        self.parser = YAPLParser(self.token_stream)
        self.parser.removeErrorListeners()
        self.tree = self.parser.program()

    def get_tokens(self):
        # Define a dictionary to map token numbers to names
        token_dict = {
            1: "';'",
            2: "'{'",
            3: "'}'",
            4: "'('",
            5: "','",
            6: "')'",
            7: "':'",
            8: "'@'",
            9: "'.'",
            10: "'~'",
            11: "'*'",
            12: "'/'",
            13: "'+'",
            14: "'-'",
            15: "'<='",
            16: "'<'",
            17: "'='",
            18: "WHITESPACE",
            19: "BLOCK_COMMENT",
            20: "LINE_COMMENT",
            21: "CLASS",
            22: "ELSE",
            23: "FALSE",
            24: "FI",
            25: "IF",
            26: "IN",
            27: "INHERITS",
            28: "ISVOID",
            29: "LET",
            30: "LOOP",
            31: "POOL",
            32: "THEN",
            33: "WHILE",
            34: "CASE",
            35: "ESAC",
            36: "NEW",
            37: "OF",
            38: "NOT",
            39: "TRUE",
            40: "STRING",
            41: "INT",
            42: "TYPE",
            43: "ID",
            44: "'<-'",
            45: "'=>'",
            46: "ERROR"
        }

        # Tokenize the input
        self.lexer.reset()
        token = self.lexer.nextToken()

        # Iterate over all the tokens
        while token.type != Token.EOF:
            token_type = token.type
            token_name = token_dict.get(token_type, f"Unknown token ({token_type})")
            print(f"Token type: {token_name}, Token ingresado: {token.text}")
            token = self.lexer.nextToken()

def main():
    
    compilador = Compiler('ejemplo.yapl')
    compilador.get_tokens()
    
    
    # for token_type, lexeme, line in token_list:
    #     try:
    #         token_name = YAPLLexer.symbolicNames[token_type]
    #     except IndexError:
    #         token_name = "UNKNOWN"
    #     print(f"Token: {token_name} ; Lexema: {lexeme} ; Linea: {line}")

if __name__ == '__main__':
    main()
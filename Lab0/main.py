import os
from antlr4 import *
from YAPLLexer import YAPLLexer
from YAPLParser import YAPLParser

class YAPLListener(ParseTreeListener):
    def enterEveryRule(self, ctx):
        print("Enter", type(ctx).__name__)

    def exitEveryRule(self, ctx):
        print("Exit", type(ctx).__name__)

def main():
    # Cargar el archivo de YAPL
    input_file = "ejemplo.yapl"  # Reemplaza con tu propio archivo de YAPL
    input_stream = FileStream(input_file)

    # Crear el lexer
    lexer = YAPLLexer(input_stream)
    token_stream = CommonTokenStream(lexer)

    # Crear el parser
    parser = YAPLParser(token_stream)

    # Obtener el árbol de análisis sintáctico
    tree = parser.program()

    # Agregar un listener personalizado para mostrar los nodos del árbol de análisis sintáctico
    listener = YAPLListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

if __name__ == '__main__':
    main()
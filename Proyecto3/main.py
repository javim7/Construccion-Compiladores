'''
Jose Hernandez: 20053
Javier Mombiela: 20067

Proyecto3: Generacion de codigo ensamblador
'''

from Compiler import *
from Cuadrupla import *
from Assembler import *

def main():
    
    compilador = Compiler('Proyecto3/Ejemplos/ejemplo1.yapl')

    compilador.lexicalAnalysis()
    compilador.syntacticAnalysis()
    compilador.semanticAnalysis()
    
    if not compilador.semanticAnalyzer.errors:

        arbol = compilador.treeStruct
        intermedio = Intermediate(arbol)
        print(intermedio)
        print(intermedio.translate())

if __name__ == '__main__':
    main()
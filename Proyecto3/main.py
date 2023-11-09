'''
Jose Hernandez: 20053
Javier Mombiela: 20067

Proyecto3: Generacion de codigo ensamblador
'''

from Compiler import *
from Cuadrupla import *
from Assembler2 import *

def main():
    
    compilador = Compiler('Proyecto3/Ejemplos/ejemplo0.yapl')

    compilador.lexicalAnalysis()
    compilador.syntacticAnalysis()
    compilador.semanticAnalysis()
    
    if not compilador.semanticAnalyzer.errors:

        arbol = compilador.treeStruct
        intermedio = Intermediate(arbol)
        print(intermedio)
        print(intermedio.translate())

        ensamblador = Assembler2(intermedio.lista_cuadruplas)
        print(ensamblador.generar_codigo_mips())

if __name__ == '__main__':
    main()
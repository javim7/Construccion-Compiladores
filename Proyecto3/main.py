'''
Jose Hernandez: 20053
Javier Mombiela: 20067

Proyecto3: Generacion de codigo ensamblador
'''

from Compiler import *
from Cuadrupla import *
from Assembler2 import *

def main():
    
    compilador = Compiler('Proyecto3/Ejemplos/ejemplo1.yapl')

    compilador.lexicalAnalysis()
    compilador.syntacticAnalysis()
    compilador.semanticAnalysis()
    
    if not compilador.semanticAnalyzer.errors:

        arbol = compilador.treeStruct
        symbolTable = compilador.symbolTable
        intermedio = Intermediate(arbol, symbolTable)
        print(intermedio)
        # print(intermedio.translate())

        ensamblador = Assembler2(intermedio.lista_cuadruplas)
        print(ensamblador.generar_codigo_mips())
        # print(ensamblador.variables_cargadas)

if __name__ == '__main__':
    main()
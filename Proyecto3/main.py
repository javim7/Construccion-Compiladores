'''
Jose Hernandez: 20053
Javier Mombiela: 20067

Proyecto3: Generacion de codigo ensamblador
'''

from Compiler import *
from Cuadrupla import *
from Ensamblador import *

def main():
    
    # compilador = Compiler('Proyecto3/Ejemplos/ejemplo1.yapl')
    # compilador = Compiler('Proyecto3/Ejemplos/ejemplo4_if.yapl')
    # compilador = Compiler('Proyecto3/Ejemplos/ejemplo3.yapl')
    
    # compilador = Compiler('Proyecto3/Ejemplos/ejemplo5_while.yapl')
    # compilador = Compiler('Proyecto3/Ejemplos/ejemplo6_if_while.yapl')
    # compilador = Compiler('Proyecto3/Ejemplos/ejemplo7_metodos.yapl')

    compilador = Compiler('Proyecto3/EjemplosPresentacion/pruebas.yapl')

    # compilador = Compiler('Proyecto3/EjemplosPresentacion/ejemplo_0.yapl')

    # compilador = Compiler('Proyecto3/EjemplosPresentacion/ejemplo_1.yapl')

    # compilador = Compiler('Proyecto3/EjemplosPresentacion/ejemplo_2.yapl')

    compilador.lexicalAnalysis()
    compilador.syntacticAnalysis()
    compilador.semanticAnalysis()
    
    if not compilador.semanticAnalyzer.errors and not compilador.lexicalErrors and not compilador.error_listener.errors:

        arbol = compilador.treeStruct
        symbolTable = compilador.symbolTable
        intermedio = Intermediate(arbol, symbolTable)
        print(intermedio)
        # print(intermedio.translate())

        ensamblador = Assembler(intermedio.lista_cuadruplas)
        print(ensamblador.data_section + ensamblador.text_section)
        # print(ensamblador.variables_cargadas)

if __name__ == '__main__':
    main()
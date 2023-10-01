'''
Jose Hernandez: 20053
Javier Mombiela: 20067

Proyecto2: Codigo Intermedio
'''

#importando el compilador
from Compiler import *
from Cuadrupla import *

def main():
    
    compilador = Compiler('Proyecto2/Ejemplos/ejemplo1.yapl')

    compilador.lexicalAnalysis()
    compilador.syntacticAnalysis()
    compilador.semanticAnalysis()
    
    if not compilador.semanticAnalyzer.errors:

        arbol = compilador.treeStruct

        intermedio = Intermediate(arbol)

        print(intermedio)

if __name__ == '__main__':
    main()
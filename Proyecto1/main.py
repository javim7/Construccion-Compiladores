'''
Jose Hernandez: 20053
Javier Mombiela: 20067

Lab: Generacion de Scanner y Parser
'''

#importando el compilador
from Compiler import *

def main():
    
    compilador = Compiler('Proyecto1/Ejemplos/ejemplo.yapl')

    compilador.lexicalAnalysis()
    compilador.syntacticAnalysis()
    compilador.semanticAnalysis()

    # arbol = compilador.treeStruct
    # postorder(arbol.root)


if __name__ == '__main__':
    main()
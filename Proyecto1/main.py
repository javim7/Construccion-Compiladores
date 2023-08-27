'''
Jose Hernandez: 20053
Javier Mombiela: 20067

Lab: Generacion de Scanner y Parser
'''

#importando el compilador
from Compiler import *

def postorder(node):
    if node.children:
        for child in node.children:
            postorder(child)
    print(node.val)


def main():
    
    compilador = Compiler('Proyecto1/Ejemplos/ejemplo.yapl')

    compilador.lexicalAnalysis()
    compilador.syntacticAnalysis()

    # arbol = compilador.treeStruct
    # postorder(arbol.root)


if __name__ == '__main__':
    main()
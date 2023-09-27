'''
Jose Hernandez: 20053
Javier Mombiela: 20067

Lab: Generacion de Scanner y Parser
'''

#importando el compilador
from Compiler import *
from Cuadrupla import *

def main():
    
    compilador = Compiler('Ejemplos/ejemplo1.yapl')

    compilador.lexicalAnalysis()
    compilador.syntacticAnalysis()
    compilador.semanticAnalysis()

    arbol = compilador.treeStruct

    intermedio = Intermediate(arbol)

    print(intermedio)

if __name__ == '__main__':
    main()
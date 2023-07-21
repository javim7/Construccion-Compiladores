'''
Jose Hernandez: 20053
Javier Mombiela: 20067

Laboratorio 0: Generacion de Scanner y Parser
'''

#importando el compilador
from Compiler import *
    
def main():
    
    compilador = Compiler('Ejemplos/ejemplo.yapl')

    compilador.lexicalAnalysis()
    compilador.syntacticAnalysis()

if __name__ == '__main__':
    main()
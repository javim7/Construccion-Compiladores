class Cuadrupla:
    def __init__(self, operador, operando1, operando2, resultado):
        self.operador = operador
        self.operando1 = operando1
        self.operando2 = operando2
        self.resultado = resultado

lista_cuadruplas = []

# Añadir una cuádrupla a la tabla
cuadrupla = Cuadrupla("+", "a", "b", "t1")
lista_cuadruplas.append(cuadrupla)


# lista_cuadruplas = [] # representa la tabla de cuádruplas
# tabla_simbolos = []  # representa la tabla de símbolos

# def recorrer_arbol(nodo):
#     if nodo es una operación:
#         operador = nodo.operador
#         resultado = nodo.resultado
#         operando1 = recorrer_arbol(nodo.hijo_izquierdo)
#         operando2 = recorrer_arbol(nodo.hijo_derecho)
        
#         instruccion = Cuadrupla(operador, resultado, operando1, operando2)
#         lista_cuadruplas.append(instruccion)
        
#         return resultado

#     else:  # nodo es una variable o un valor literal
#         # Utiliza la tabla de símbolos para obtener información sobre la variable
#         info_variable = tabla_simbolos[nodo.valor]
        
#         return info_variable

# recorrer_arbol(raiz_del_arbol)
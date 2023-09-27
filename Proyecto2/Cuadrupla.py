class Cuadrupla:
    def __init__(self, operador, operando1, operando2, resultado):
        self.operador = operador
        self.operando1 = operando1
        self.operando2 = operando2
        self.resultado = resultado

    def __str__(self):
        return f"Cuadrupla: {self.operador}, {self.operando1}, {self.operando2}, {self.resultado}"

class Intermediate():
    
    def __init__(self, arbol):
        self.lista_cuadruplas = []
        self.arbol = arbol
        self.temp_counter = 1
        self.label_counter = 1

        self.recorrer_arbol(arbol.root)

    def create_new_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def create_new_label(self):
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def recorrer_arbol(self, node=None):

        if node is not None:
            
            self.generar_codigo_tres_direcciones(node)

            for child in node.children:

                self.recorrer_arbol(child)

    def generar_codigo_tres_direcciones(self, node=None):

        if node.val == "expr":

            # Esto es una operacion aritmetica

            if len(node.children) == 3 and node.children[1].val in ["+", "-", "*", "/"]:

                self.aritmetica(node)

        pass

    # Agarramos los hijos de un nodo expr
    def getExprChildren(self, node, child_values=None):
        if child_values is None:
            child_values = []  # Initialize the list only in the initial call
        
        for child in node.children:
            if child.val == "expr":
                self.getExprChildren(child, child_values)  # Pass the existing list to the recursive call
            else:
                child_values.append(child.val)
        
        return child_values

    def aritmetica(self, node=None):

        print(self.getExprChildren(node))

        # operador = node.children[1].val
        # operando1 = node.children[0].val
        # operando2 = node.children[2].val
        # resultado = self.create_new_temp()

        # cuadrupla = Cuadrupla(operador, operando1, operando2, resultado)

        # self.lista_cuadruplas.append(cuadrupla)

        # node.val = resultado
    
    def __str__(self):

        for cuadrupla in self.lista_cuadruplas:
            print(cuadrupla)
        
        return 

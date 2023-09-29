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
        self.dic_cuadruplas = {}
        self.processed_nodes = set()
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
        rule = node.val

        if rule == "expr":
            if len(node.children) == 3: # es operacion aritmetica
                self.aritmethicQuad(node)
            if node.children[0].val == "return": # es un return
                self.returnQuad(node)

        elif rule == "property": # es una asignacion de variable
            self.propertyQuad(node)

        elif rule == "varDeclaration": # es una declaracion de variable
            self.varDeclarationQuad(node)

        elif rule == "method":
            self.methodQuad(node)

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
    
    def propertyQuad(self, node=None):
        #if para ver si es asignacion o solo declaracion
        if len(node.children) > 1: # es una asignacion
            formal = node.children[0]
            expr = node.children[2]
            cuadrupla = Cuadrupla("<-", expr.children[0].val, None, formal.children[0].val)
            self.lista_cuadruplas.append(cuadrupla)

    def returnQuad(self, node=None):
        # Si el nodo tiene hijos
        if len(node.children) > 1:
            # Obtenemos los hijos del nodo VarDeclaration
            child_values = []
            for child in node.children:
                if child.val == "expr":
                    # Si el hijo es un nodo expr, llamamos recursivamente a aritmethicQuad(node)
                    child_values.append(self.aritmethicQuad(child))
                else:
                    # Si el hijo no es un nodo expr, simplemente agregamos su valor a la lista
                    child_values.append(child.val)
            
            # Creamos la cuadrupla con la operación de asignación y los operandos
            cuadrupla = Cuadrupla("return", child_values[2], None, None)
            
            # Agregamos la cuadrupla a la lista de cuadruplas
            self.lista_cuadruplas.append(cuadrupla)
        else:
            # Si el nodo no tiene hijos o solo tiene uno, entonces es una variable o un número, y simplemente lo retornamos
            return node.val if len(node.children) == 0 else self.aritmethicQuad(node.children[0])

    def varDeclarationQuad(self, node=None):
        # Si el nodo tiene hijos
        if len(node.children) > 1:
            # Obtenemos los hijos del nodo VarDeclaration
            child_values = []
            for child in node.children:
                if child.val == "expr":
                    # Si el hijo es un nodo expr, llamamos recursivamente a aritmethicQuad(node)
                    child_values.append(self.aritmethicQuad(child))
                else:
                    # Si el hijo no es un nodo expr, simplemente agregamos su valor a la lista
                    child_values.append(child.val)
            
            # Creamos la cuadrupla con la operación de asignación y los operandos
            cuadrupla = Cuadrupla("<-", child_values[2], None, child_values[0])
            
            # Agregamos la cuadrupla a la lista de cuadruplas
            self.lista_cuadruplas.append(cuadrupla)

    def aritmethicQuad(self, node=None):
        # Si el nodo ya ha sido procesado, simplemente retornamos su valor
        if node in self.processed_nodes:
            return node.val

        # Si el nodo tiene hijos
        if len(node.children) > 1:
            # Obtenemos los hijos del nodo expr
            child_values = []
            for child in node.children:
                if child.val == "expr":
                    # Si el hijo es un nodo expr, llamamos recursivamente a aritmethicQuad(node)
                    child_values.append(self.aritmethicQuad(child))
                else:
                    # Si el hijo no es un nodo expr, simplemente agregamos su valor a la lista
                    child_values.append(child.val)
            
            # Creamos un nuevo temporal para almacenar el resultado de la operación
            temp = self.create_new_temp()
            
            # Creamos la cuadrupla con la operación y los operandos
            cuadrupla = Cuadrupla(child_values[1], child_values[0], child_values[2], temp)
            
            # Agregamos la cuadrupla a la lista de cuadruplas
            self.lista_cuadruplas.append(cuadrupla)
            
            # Agregamos el nodo a la lista de nodos procesados
            self.processed_nodes.add(node)

            # Retornamos el temporal que almacena el resultado de la operación
            return temp
        else:
            # Si el nodo no tiene hijos o solo tiene uno, entonces es una variable o un número, y simplemente lo retornamos
            return node.val if len(node.children) == 0 else self.aritmethicQuad(node.children[0])

    def methodQuad(self, node=None):
        pass

    def __str__(self):
        result = "\nCODIGO INTERMEDIO:\n"
        for cuadrupla in self.lista_cuadruplas:
            result += str(cuadrupla) + "\n"
        return result
    
    # def aritmethicQuad(self, node=None):
    #     # Si el nodo ya ha sido procesado, simplemente retornamos su valor
    #     if node in self.processed_nodes:
    #         return node.val

    #     # Si el nodo tiene hijos
    #     if len(node.children) > 1:
    #         # Obtenemos los hijos del nodo expr
    #         child_values = []
    #         for child in node.children:
    #             if child.val == "expr":
    #                 # Si el hijo es un nodo expr, llamamos recursivamente a aritmethicQuad(node)
    #                 child_values.append(self.aritmethicQuad(child))
    #             else:
    #                 # Si el hijo no es un nodo expr, simplemente agregamos su valor a la lista
    #                 child_values.append(child.val)
            
    #         # Buscamos en la lista de cuadruplas existentes para ver si ya hay una cuadrupla con los mismos operandos y operación
    #         for cuadrupla in self.lista_cuadruplas:
    #             if cuadrupla.operador == child_values[1] and cuadrupla.operando1 == child_values[0] and cuadrupla.operando2 == child_values[2]:
    #                 # Si encontramos una cuadrupla existente, simplemente retornamos su resultado
    #                 return cuadrupla.resultado
            
    #         # Si no encontramos una cuadrupla existente, creamos un nuevo temporal para almacenar el resultado de la operación
    #         temp = self.create_new_temp()
            
    #         # Creamos la cuadrupla con la operación y los operandos
    #         cuadrupla = Cuadrupla(child_values[1], child_values[0], child_values[2], temp)
            
    #         # Agregamos la cuadrupla a la lista de cuadruplas
    #         self.lista_cuadruplas.append(cuadrupla)
            
    #         # Agregamos el nodo a la lista de nodos procesados y al diccionario con su temporal correspondiente
    #         self.processed_nodes.add(node)
    #         self.dic_cuadruplas[node] = temp

    #         # Retornamos el temporal que almacena el resultado de la operación
    #         return temp
    #     else:
    #         # Si el nodo no tiene hijos o solo tiene uno, entonces es una variable o un número, y simplemente lo retornamos
    #         return node.val if len(node.children) == 0 else self.aritmethicQuad(node.children[0])

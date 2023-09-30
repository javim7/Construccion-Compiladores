from prettytable import PrettyTable

class Cuadrupla:

    def __init__(self, operador, operando1, operando2, resultado):

        # Asigna el operador pasado como argumento a la variable de instancia self.operador
        
        self.operador = operador
        
        # Asigna el primer operando pasado como argumento a la variable de instancia self.operando1
        
        self.operando1 = operando1
        
        # Asigna el segundo operando pasado como argumento a la variable de instancia self.operando2
        
        self.operando2 = operando2
        
        # Asigna el resultado pasado como argumento a la variable de instancia self.resultado
        
        self.resultado = resultado

    def __str__(self):

        # Retorna una representación en cadena de la cuádrupla en un formato específico
        
        return f"Cuadrupla: {self.operador}, {self.operando1}, {self.operando2}, {self.resultado}"


class Intermediate():
    
    def __init__(self, arbol):

        # Inicializa una lista vacía para almacenar cuádruplas
        
        self.lista_cuadruplas = []
        
        # Inicializa un diccionario vacío para almacenar cuádruplas
        
        self.dic_cuadruplas = {}
        
        # Inicializa un conjunto vacío para almacenar nodos procesados
        
        self.processed_nodes = set()
        
        # Almacena el árbol pasado como argumento en la variable de instancia self.arbol
        
        self.arbol = arbol
        
        # Inicializa un contador de temporales
        
        self.temp_counter = 1
        
        # Inicializa un contador de etiquetas
        
        self.label_counter = 1
        
        # Inicializa un índice a 0
        
        self.index = 0
        
        # Llama al método recorrer_arbol con la raíz del árbol como argumento
        
        self.recorrer_arbol(arbol.root)


    def create_new_temp(self):

        # Crea una nueva variable temporal usando el contador de temporales (temp_counter)
        
        temp = f"t{self.temp_counter}"
        
        # Incrementa el contador de temporales para el próximo uso
        
        self.temp_counter += 1
        
        # Retorna la nueva variable temporal creada
        
        return temp


    def create_new_label(self):

        # Crea una nueva etiqueta usando el contador de etiquetas (label_counter)
        
        label = f"L{self.label_counter}"
        
        # Incrementa el contador de etiquetas para el próximo uso
        
        self.label_counter += 1
        
        # Retorna la nueva etiqueta creada
        
        return label


    def recorrer_arbol(self, node=None):

        # Verifica si el nodo proporcionado no es None
        
        if node is not None:
            
            # Llama al método generar_codigo_tres_direcciones para el nodo actual
            
            self.generar_codigo_tres_direcciones(node)
            
            # Itera sobre todos los hijos del nodo actual y llama recursivamente al método recorrer_arbol para cada hijo
            
            for child in node.children:

                self.recorrer_arbol(child)


    def generar_codigo_tres_direcciones(self, node=None):

        # Asigna el valor del nodo a la variable rule
        
        rule = node.val
        
        # Obtiene la cantidad de hijos del nodo y la almacena en la variable children_len
        
        children_len = len(node.children)
        
        if rule == "expr":
            
            # Comprueba si es un método sin parámetros
            
            if children_len == 3 and node.children[1].val == "(" and node.children[2].val == ")":
                
                self.methodCallQuad(node)
                
            # Comprueba si es un método con parámetros
            
            elif children_len > 3 and node.children[1].val == "(" and node.children[-1].val == ")":
                
                self.methodCallParamsQuad(node)
                
            # Comprueba si es operación aritmética
            
            elif children_len == 3 and node.children[1].val in ["+", "/", "-", "*"]:
                
                self.arithmeticQuad(node)
                
            # Comprueba si es un if
            
            elif children_len == 7 and node.children[0].val == "if" and node.children[-1].val == "fi":
                
                self.ifQuad(node)
                
            # Comprueba si es un return
            
            if node.children[0].val == "return":
                
                self.returnQuad(node)

        elif rule == "property":
            
            # Es una asignación de variable
            
            self.propertyQuad(node)
            
        elif rule == "varDeclaration":
            
            # Es una declaración de variable
            
            self.varDeclarationQuad(node)
            
        elif rule == "method":
            
            # Es un método
            
            self.methodQuad(node)
            
        elif rule == "classDefine":
            
            # Es una clase
            
            self.classQuad(node)



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
    
    # funcion para crear la cuadrupla de methodCall sin parametros
    def methodCallQuad(self, node):
        cuadrupla = Cuadrupla("METHOD_CALL", node.children[0].val, 0, None)
        self.lista_cuadruplas.append(cuadrupla)

        # Agregamos el nodo a la lista de nodos procesados
        self.processed_nodes.add(node)

    # funcion para crear la cuadrupla de methodCall con parametros
    def methodCallParamsQuad(self, node):

        #saltarnos si es un return
        if node.children[0].val == "return":
            return

        children = node.children
        # ver los formals
        contador = 0
        for child in children:
            if child.val == "expr":
                self.lista_cuadruplas.append(Cuadrupla("PRE_PARAM", child.children[0].val, None, None))
                contador += 1
        
        # creamos el temporal
        temp = self.create_new_temp()
        # creamos la cuadrupla
        cuadrupla = Cuadrupla("METHOD_CALL", node.children[0].val, contador, temp)
        self.lista_cuadruplas.append(cuadrupla)

    def createIfLabels(self, node=None):
        # Initialize a list to store labels
        labels = []

        # Check if node has children
        if node and hasattr(node, 'children'):
            # Loop through each child
            for child in node.children:
                # If child value is 'if', create a new label and add it to the list
                if child.val == "if":
                    label = self.create_new_label()
                    labels.append(label)

                # Recursively call function on child and extend the label list with returned labels
                labels.extend(self.createIfLabels(child))

        return labels

    # funcion para crear la cuadrupla de if
    def ifQuad(self, node=None):

        if node in self.processed_nodes:
            return node.val
        
        #creamos las etiquetasq
        labels = self.createIfLabels(node)
        labels.append(self.create_new_label())
        print(labels)

        #creamos la cuadrupla de la condicion
        condicion = self.getExprChildren(node.children[1])
        temp = self.create_new_temp()
        cuadrupla = Cuadrupla(condicion[1], condicion[0], condicion[2], temp)
        self.lista_cuadruplas.append(cuadrupla)

        #ccreamos la cuadrupla del gotof
        cuadrupla = Cuadrupla("GOTOF", temp, None, labels[0])
        self.lista_cuadruplas.append(cuadrupla)

        #agregamos la cuadrupla deel cuerpo del if
        self.recorrer_arbol(node.children[3])
        #goto al label final
        cuadrupla = Cuadrupla("GOTO", None, None, labels[-1])

        #create la cuadrupla del label1
        cuadrupla = Cuadrupla("LABEL", None, None, labels[0])
        # else if

        #agregamos el nodo a nodos procesados
        self.processed_nodes.add(node)

    #if para ver si es asignacion o solo declaracion
    def propertyQuad(self, node=None):
        if len(node.children) > 1: # es una asignacion
            formal = node.children[0]
            expr = node.children[2]
            cuadrupla = Cuadrupla("<-", expr.children[0].val, None, formal.children[0].val)
            self.lista_cuadruplas.append(cuadrupla)

    # funcion para crear la cuadrupla de returns
    def returnQuad(self, node=None):
        # Si el nodo tiene hijos
        if len(node.children) > 1:
            # Obtenemos los hijos del nodo VarDeclaration
            child_values = []
            for child in node.children:
                if child.val == "expr":
                    # Si el hijo es un nodo expr, llamamos recursivamente a arithmeticQuad(node)
                    child_values.append(self.arithmeticQuad(child))
                else:
                    # Si el hijo no es un nodo expr, simplemente agregamos su valor a la lista
                    child_values.append(child.val)
            
            # Creamos la cuadrupla con la operación de asignación y los operandos
            cuadrupla = Cuadrupla("RETURN", child_values[2], None, None)
            
            # Agregamos la cuadrupla a la lista de cuadruplas
            self.lista_cuadruplas.append(cuadrupla)
        else:
            # Si el nodo no tiene hijos o solo tiene uno, entonces es una variable o un número, y simplemente lo retornamos
            return node.val if len(node.children) == 0 else self.arithmeticQuad(node.children[0])

    # funcion para crear la cuadrupla de variables asignadas
    def varDeclarationQuad(self, node=None):
        if node in self.processed_nodes:
            return node.val

        # Si el nodo tiene hijos
        if len(node.children) > 1:
            # Obtenemos los hijos del nodo VarDeclaration
            child_values = []
            for child in node.children:
                if child.val == "expr":
                    # Si el hijo es un nodo expr, llamamos recursivamente a arithmeticQuad(node)
                    child_values.append(self.arithmeticQuad(child))
                else:
                    # Si el hijo no es un nodo expr, simplemente agregamos su valor a la lista
                    child_values.append(child.val)
            
            # Creamos la cuadrupla con la operación de asignación y los operandos
            cuadrupla = Cuadrupla("<-", child_values[2], None, child_values[0])
            
            # Agregamos la cuadrupla a la lista de cuadruplas
            self.lista_cuadruplas.append(cuadrupla)

    # funcion para crear la cuadrupla de operaciones aritmeticas
    def arithmeticQuad(self, node=None):
        # Si el nodo ya ha sido procesado, simplemente retornamos su valor
        if node in self.processed_nodes:
            return node.val

        # Si el nodo tiene hijos
        if len(node.children) > 1:
            # Obtenemos los hijos del nodo expr
            child_values = []
            for child in node.children:
                if child.val == "expr":
                    # Si el hijo es un nodo expr, llamamos recursivamente a arithmeticQuad(node)
                    child_values.append(self.arithmeticQuad(child))
                elif child.val in ["(", ")"]:
                    # Si el hijo es un paréntesis, lo ignoramos
                    continue
                else:
                    # Si el hijo no es un nodo expr ni un paréntesis, simplemente agregamos su valor a la lista
                    child_values.append(child.val)
            
            # Si hay suficientes valores en child_values para formar una cuadrupla
            if len(child_values) >= 3:
                # Creamos un nuevo temporal para almacenar el resultado de la operación
                temp = self.create_new_temp()
                
                # Creamos la cuadrupla con la operación y los operandos
                cuadrupla = Cuadrupla(child_values[1], child_values[0], child_values[2], temp)
                # print(cuadrupla)
                
                # Agregamos la cuadrupla a la lista de cuadruplas
                self.lista_cuadruplas.append(cuadrupla)
                
                # Agregamos el nodo a la lista de nodos procesados
                self.processed_nodes.add(node)

                # Retornamos el temporal que almacena el resultado de la operación
                return temp
            else:
                # Si no hay suficientes valores en child_values, simplemente retornamos el primer valor
                return child_values[0] if child_values else None
        else:
            # Si el nodo no tiene hijos o solo tiene uno, entonces es una variable o un número, y simplemente lo retornamos
            return node.val if len(node.children) == 0 else self.arithmeticQuad(node.children[0])

    # funcion para crear la cuadrupla de metodo
    def methodQuad(self, node=None):

        children = node.children
        
        # creamos la cuadrupla
        cuadrupla = Cuadrupla("METHOD_START", node.children[0].val, node.children[-4].val, None)
        self.lista_cuadruplas.append(cuadrupla)

        for child in children:
            if child.val == "formal":
                self.paramQuad(child)
    
    # funcion para crear la cuadrupla de clase
    def classQuad(self, node=None):

        # Revisamos si la clase incluye herencia

        if node.children[2].val == "inherits":

            cuadrupla = Cuadrupla("CLASS", node.children[1].val, node.children[3].val, None)

            self.lista_cuadruplas.append(cuadrupla)
        
        # La clase no incluye herencia

        else:

            cuadrupla = Cuadrupla("CLASS", node.children[1].val, None, None)

            self.lista_cuadruplas.append(cuadrupla)

    # funcion para crear la cuadrupla de los parametros de un metodo
    def paramQuad(self, node=None):
            
        # creamos la cuadrupla
        cuadrupla = Cuadrupla("PARAM", node.children[0].val, node.children[2].val, None)
        self.lista_cuadruplas.append(cuadrupla)

    def __str__(self):
        # Crear una tabla con las columnas adecuadas
        table = PrettyTable()
        table.field_names = ["Indice","Operador", "Operando 1", "Operando 2", "Resultado"]

        # Agregar las cuadruplas a la tabla
        for cuadrupla in self.lista_cuadruplas:
            table.add_row([self.lista_cuadruplas.index(cuadrupla), cuadrupla.operador, cuadrupla.operando1, cuadrupla.operando2, cuadrupla.resultado])

        # Retornar la representación de la tabla como cadena
        return f"\n-----------CODIGO INTERMEDIO-----------\n{table}\n"

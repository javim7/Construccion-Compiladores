from prettytable import PrettyTable

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
        self.index = 0

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
            # print(node)
            if len(node.children) == 3 and node.children[1].val == "(" and node.children[2].val == ")": # es un metodo sin parametros
                self.methodCallQuad(node)
            elif len(node.children) > 3 and node.children[1].val == "(" and node.children[-1].val == ")": # es un metodo con parametros
                self.methodCallParamsQuad(node)
            elif len(node.children) == 3 and node.children[1].val in ["+", "/", "-", "*"]: # es operacion aritmetica
                self.arithmeticQuad(node)
            elif len(node.children) == 7 and node.children[0].val == "if" and node.children[-1].val == "fi": # es un if
                self.ifQuad(node)
            if node.children[0].val == "return": # es un return
                self.returnQuad(node)

        elif rule == "property": # es una asignacion de variable
            self.propertyQuad(node)

        elif rule == "varDeclaration": # es una declaracion de variable
            self.varDeclarationQuad(node)

        elif rule == "method": # es un metodo
            self.methodQuad(node)

        elif rule == "classDefine": # es una clase
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

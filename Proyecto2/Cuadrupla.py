from prettytable import PrettyTable
from termcolor import colored

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

        # Conjunto para almacenar etiquetas ya creadas

        self.created_labels = set()
        
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
                
                self.ifQuadEnhanced(node)
                
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
    def ifQuad(self, node=None, exit_label=None):

        # Obtenemos la condición, el bloque then y el bloque else de los hijos del nodo

        # Una estrucuta if se ve de la siguiente manera: Children: ['if', 'expr', 'then', 'expr', 'else', 'expr', 'fi']

        cond_node, then_node, else_node = node.children[1], node.children[3], node.children[5]

        # Generamos cuádruplas para la condición

        cond_quad = self.getExprChildren(cond_node)

        # Suponiendo que 'tn' es el resultado de la condición EJEMPLO: tn_temp = t6 y false_label = L1

        tn_temp = self.create_new_temp()

        false_label = self.create_new_label()

        self.lista_cuadruplas.append(Cuadrupla(cond_quad[1], cond_quad[0], cond_quad[2], tn_temp))

        self.lista_cuadruplas.append(Cuadrupla('JUMP_IF_FALSE', tn_temp, '_', false_label))

        # Generamos cuádruplas para el bloque then

        # TODO En este caso then_quad es un NODO del arbol de tipo "VarDeclaration" pero tenemos que revisar despues si siempre sera esto

        self.varDeclarationQuad(then_node)

        # Solo crea una nueva etiqueta de salida si no se proporcionó una

        if exit_label is None:

            exit_label = self.create_new_label()

        # Generamos una etiqueta para el bloque else

        self.lista_cuadruplas.append(Cuadrupla('LABEL', '_', '_', false_label))

        # Instrucción para saltar al final del bloque if-else

        self.lista_cuadruplas.append(Cuadrupla('JUMP', '_', '_', exit_label))

        # Chequea si el bloque else es otro if

        if else_node.children[0].val == 'if':

            self.ifQuad(else_node, exit_label)

        else:

            # TODO En este caso then_quad es un NODO del arbol de tipo "VarDeclaration" pero tenemos que revisar despues si siempre sera esto

            self.varDeclarationQuad(else_node)
        
        # Generamos una etiqueta para el bloque exit final del if-else

        # Verifica si la etiqueta ya ha sido creada antes de agregar una nueva etiqueta

        if exit_label not in self.created_labels:

            self.lista_cuadruplas.append(Cuadrupla('LABEL', '_', '_', exit_label))

            # Agrega la etiqueta al conjunto de etiquetas creadas

            self.created_labels.add(exit_label) 

    def ifQuadEnhanced(self, node=None, exit_label=None, start_label=None, primera_vez=True):

        if start_label is not None:

            self.lista_cuadruplas.append(Cuadrupla("LABEL", None, None, start_label))

        # Este metodo esta creado para ser una version mejorada del ifQuad.

        # Un condicional if se ve de la siguiente manera: ['if', 'expr', 'then', 'expr', 'else', 'expr', 'fi']

        # Obtenemos la condición, el bloque then y el bloque else de los hijos del nodo

        cond_node, then_node, else_node = node.children[1], node.children[3], node.children[5]

        # Realizamos la cuadrupla de la condicion

        cond_quad = self.getExprChildren(cond_node)

        # Generamos una variable t para almacenar el resultado de la condicion

        t_condicion = self.create_new_temp()

        # Generamos la cuadrupla de la condicion

        self.lista_cuadruplas.append(Cuadrupla(cond_quad[1], cond_quad[0], cond_quad[2], t_condicion))

        # Una vez que tenemos el resultado de la condicion, creamos una etiqueta para el bloque then

        l_condicion = self.create_new_label()

        # Creamos la cuadrupla de la etiqueta en caso de que la condicion sea falsa

        self.lista_cuadruplas.append(Cuadrupla("JUMP_IF_FALSE", t_condicion, None, l_condicion))

        # Creamos el cuerpo de la condicion then en caso de que la condicion sea verdadera

        # En el caso de que la condicion sea verdadera:
        print("Creando cuerpo del then:")
        cuad_tempr = self.varDeclarationQuad(then_node.children[0])
        print(cuad_tempr) 
        print("Cuerpo del then creado.")

        # En este punto ya evaluamos el cuerpo del then, por lo que creamos una etiqueta para la salida del if

        if exit_label is None:

            exit_label = self.create_new_label()
        
        # Creamos la cuadrupla de salto para salir del if

        self.lista_cuadruplas.append(Cuadrupla("JUMP", None, None, exit_label))

        # Revismos si el cuerpo del else es otro if

        if else_node.children[0].val == "if":

            self.ifQuadEnhanced(else_node, exit_label, l_condicion, primera_vez=False)
        
        # Si el cuerpo del else no es otro if, entonces es un bloque de codigo normal

        else:

            self.lista_cuadruplas.append(Cuadrupla("LABEL", None, None, l_condicion))

            self.varDeclarationQuad(else_node.children[0])

            self.lista_cuadruplas.append(Cuadrupla("JUMP", None, None, exit_label))
        

        # Creamos la cuadrupla para la exit label del if

        if primera_vez:

            self.lista_cuadruplas.append(Cuadrupla("LABEL", None, None, exit_label))

        # Cuadrupla comodin para ifelse:
        self.lista_cuadruplas.append(Cuadrupla("❌","❌","❌","❌"))
        pass 



    def ifQuadGenerate(self, node):

        # Esta implementacion del ifQuad es para generar el codigo intermedio de un if utilizando una aproximacion distinta a la del ifQuadEnhanced

        # Primero, generaramos todas las etiquetas que necesitamos para el if

        # Creamos una etiqueta para el inicio del if

        l_inicio = self.create_new_label()

        # Creamos una etiqueta por cada posible else if que pueda tener el if

        cond_node, then_node, else_node = node.children[1], node.children[3], node.children[5]

        cantidad_labels_elseif = 0

        if else_node.children[0].val == "if":

            cantidad_labels_elseif = self.obtenerLabelIf(node)
        
        print("La cantidad de elseif es: ", cantidad_labels_elseif)

        

        
    def obtenerLabelIf(self, node):

        try:

            cond_node, then_node, else_node = node.children[1], node.children[3], node.children[5]

            if else_node.children[0].val == "if":

                return 1 + self.obtenerLabelIf(node.children[0])
            
            else:

                return 0
        
        except:

            return 0



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
            return cuadrupla

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

        # Definir un diccionario de colores para cada operador
        operator_colors = {
            'JUMP_IF_FALSE': 'red',
            'METHOD_START': 'green',
            '<-': 'cyan',
            'LABEL': 'yellow',
            'JUMP': 'magenta',
            '<': 'green',
        }

        # grey
        # red
        # green
        # yellow
        # blue
        # magenta
        # cyan
        # white

        # Agregar las cuadruplas a la tabla
        for cuadrupla in self.lista_cuadruplas:
            operator_color = operator_colors.get(cuadrupla.operador, 'white')  # Default a blanco si el operador no está en el diccionario
            colored_row = [colored(item, operator_color) for item in [
                self.lista_cuadruplas.index(cuadrupla), 
                cuadrupla.operador, 
                cuadrupla.operando1, 
                cuadrupla.operando2, 
                cuadrupla.resultado
            ]]
            table.add_row(colored_row)

        # Retornar la representación de la tabla como cadena
        return f"\n-----------CODIGO INTERMEDIO-----------\n{table}\n"


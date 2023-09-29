class SemanticVisitor:
    def __init__(self, symbol_table, tokenDict):
        self.symbol_table = symbol_table
        self.tokenDict = tokenDict
        self.names, self.ids, self.dataTypes, self.values, self.inheritsFroms, self.scopes, self.lines = self.symbol_table.allInfo()

    # Verificar que exista clase main
    def visit_program_node(self, node):
        MainClass = False
        for children in node.children:
            if children.val == "classDefine":
                if children.children[1].val == "Main":
                    MainClass = True
        
        if not MainClass:
            return f"El programa debe tener una clase 'Main'"
        return None

    # Verificar si alguna clase hereda a main o viceversa
    def visit_classdefine_node(self, node):
        class_name = node.children[1].val
        method_names = [symbol.name for symbol in self.symbol_table.symbols if symbol.id_type == "Method" and symbol.scope.startswith(class_name)]
        
        #ver si hace falta la clase main
        if class_name == "Main" and "main" not in method_names:
            return f"La clase 'Main' debe tener un metodo 'main'"
        #ver si alguna clase hereda a Main
        if node.children[2].val == "inherits" and node.children[3].val == "Main":
            return f"La clase 'Main' no puede ser heredar por ninguna otra clase"
        
        elif node.children[2].val == "inherits" and node.children[3].val == "String":
            return f"La clase 'String' no puede ser heredar por ninguna otra clase"
        
        elif node.children[2].val == "inherits" and node.children[3].val == "Int":
            return f"La clase 'Int' no puede ser heredar por ninguna otra clase"
        
        elif node.children[2].val == "inherits" and node.children[3].val == "Bool":
            return f"La clase 'Bool' no puede ser heredar por ninguna otra clase"
        
        if node.children[2].val == "inherits" and class_name == "Main":
            return f"La clase 'Main' no puede heredar de ninguna otra clase"

        if node.children[2].val == "inherits" and node.children[3].val == class_name:
            return f"La clase '{class_name}' no puede heredar de si misma (herencia recursiva)"
        
        return None


    # Verifica que los metodos heredados sigan la firma del origina y que exista el metodo main
    def visit_method_node(self, node):
        methodName = node.children[0].val
        nodeScope = node.parent.parent.children[1].val
        
        if methodName == "main" and node.children[2].val == "formal":
            return f"El metodo 'main' no puede tener parametros formales"
        
        #ver que los metodos heredadeos sigan la firma del original
        symbolToUse = self.symbol_table.lookup_by_scope(methodName, nodeScope)
        # print(symbolToUse)
        if symbolToUse.inheritsFrom:
            # print(symbolToUse)
            inheritedFrom = symbolToUse.inheritsFrom
            symbolToMatch = self.symbol_table.lookup_by_scope(methodName, inheritedFrom)
            # print(symbolToMatch)
            if symbolToMatch.data_type != symbolToUse.data_type:
                return f"El metodo '{methodName}' en el scope '{nodeScope}' debe tener el mismo tipo de retorno que el metodo original en el scope '{inheritedFrom}'"


    def visit_vardeclaration_node(self, node):
        #revisar si la variable ya fue definida
        var_name = node.children[0].val
        for symbol in self.symbol_table.symbols:
            if symbol.name == var_name and symbol.id_type == "Variable" and symbol.data_type == "Void":
                return f"La variable '{var_name}' no ha sido definida"

        #revisar que las asignaciones esten en el mismo scope
        varScope = self.symbol_table.lookup_all(var_name).scope
        children = self.getExprChildren(node.children[2])
        for child in children:
            if child in self.names:
                childScope = self.symbol_table.lookup_all(child).scope
                if childScope.split(".")[0] != varScope.split(".")[0]:
                    return f"El atributo '{child}' no ha sido definida en el scope '{varScope}'"
        #revisar que los tipos sean los correctos

        #obtener el tipo de la variable
        var_type = None
        for symbol in self.symbol_table.symbols:
            if symbol.name == var_name:
                var_type = symbol.data_type

        # print("var_name: ", var_name, "var_type: ", var_type)
        #revisar por asignaciones correctas
        expr_node = node.children[2]

        if len(expr_node.children) == 1:
            value_node = expr_node.children[0]
            
            # Verifica que las variables se aignen con el mismo tipo
            if value_node.val in self.names:
                symbol = self.symbol_table.lookup(value_node.val)
                if symbol.data_type != var_type:
                    if var_type.lower() == "int" and symbol.data_type.lower() == "bool":
                        if symbol.value:
                            self.symbol_table.update_symbol_value(var_name, 1)
                        else:
                            self.symbol_table.update_symbol_value(var_name, 0)
                        self.symbol_table.display()
                    elif var_type.lower() == "bool" and symbol.data_type.lower() == "int":
                        if symbol.value == "0":

                            self.symbol_table.update_symbol_value(var_name, False)
                        else:

                            self.symbol_table.update_symbol_value(var_name, True)
                        self.symbol_table.display()
                    else:
                        return f"La variable '{var_name}' debe ser de tipo '{var_type}' no '{symbol.data_type}'"
            
            # Verifica que los tokens se asignen con el mismo tipo
            elif value_node.val in self.tokenDict:
                valueType = self.tokenDict[value_node.val]
                
                if valueType.lower() != var_type.lower():
                    if var_type.lower() == "int" and valueType.lower() == "bool":
                        print(var_name)
                    elif var_type.lower() == "bool" and valueType.lower() == "int":
                        pass
                    else:
                        if symbol.data_type.lower() == "id" or symbol.data_type.lower() == "void": #este no
                            return f"El atributo '{value_node.val}' no ha sido definido en el scope '{varScope}'"
                        else:
                            return f"La variable '{var_name}' debe ser de tipo '{var_type}' no '{symbol.data_type}'"

        
        else:
            child_values = self.getExprChildren(expr_node)
            operators = []
            alphanum = []
            variables = {}

            stringOperators = ["+", ","]
            intOperators = ["+", "-", "*", "/", "%", "(", ")","~"]

           
            #Verifica que hayan operadores dentro de la asignacion x <- 1 + 2
            for child in child_values:
                if child.isalnum():
                    # print(child)
                    if child in self.names:
                        symbol = self.symbol_table.lookup(child)
                        variables[child] = symbol.data_type
                        alphanum.append(child)
                    else:
                        variables[child] = self.tokenDict[child]  
                        alphanum.append(child)
                elif '"' in child:
                    variables[child] = "String"
                    alphanum.append(child)
                else:
                    operators.append(child)

            # print("alphanum: ", alphanum)
            # print("variables: ", variables)
            # Verifica y asigna el return de un metodo
            if "(" in operators and ")" in operators:
                symbol_type = self.symbol_table.lookup_by_scope(alphanum[0], varScope)
                symbol_type_2 = symbol_type.data_type
                if symbol_type_2.lower() != var_type.lower():
                    return f"La variable '{alphanum[0]}' debe ser de tipo '{var_type}' no '{symbol_type_2}'"
                return None

            # print(operators)

            # Verifica que las variables se aignen con el mismo tipo
            firstVal = next(iter(variables.values())).lower()
            if all(value.lower() == firstVal for value in variables.values()):
                if firstVal.lower() != var_type.lower():
                    return f"Las variables '{alphanum}' deben ser de tipo '{var_type}' no '{firstVal}'"

                elif firstVal.lower() == var_type.lower() and firstVal.lower() == "string":
                    for operator in operators:
                        if operator not in stringOperators:
                            return f"La operacion '{operator}' no es valida para variables de tipo '{firstVal}'"
              
                elif firstVal.lower() == var_type.lower() and firstVal.lower() == "int":
                    for operator in operators:
                        if operator not in intOperators:
                            return f"La operacion '{operator}' no es valida para variables de tipo '{firstVal}'"
            else:
                for var in alphanum:
                    if var not in self.names and self.tokenDict[var].lower() == "id":
                        return f"El atributo '{var}' no ha sido definido en el scope '{varScope}'"
                    if var.lower() == "not":
                        if var_type.lower() != "bool":
                            return f"La operacion '{var}' no es valida para variables de tipo '{var_type}'"
                        else:
                            return None

                return f"Las variables '{alphanum}' deben ser del mismo tipo '{var_type}'"

        return None

    def visit_expr_node(self, node):
        

        # Verifica while loops e ifs
        if node.children[0].val == "if" or node.children[0].val == "while":

            return self.check_comparisons(node)

        # methodcall sin parametros
        if len(node.children) == 3 and node.children[1].val == "(" and node.children[2].val == ")":
            methodName = node.children[0].val
            nodeScope = self.getClassDefineParent(node)
            for symbol in self.symbol_table.symbols:
                if symbol.name == methodName and symbol.id_type == "Method" and symbol.scope.startswith(nodeScope):
                    return None
            
            return f"El metodo '{methodName}' no ha sido definido en el scope '{nodeScope}'"
        
        # methodcall con parametros u operacion IO o return
        elif len(node.children) == 4 and node.children[1].val == "(" and node.children[3].val == ")":
            methodName = node.children[0].val
            nodeScope = self.getClassDefineParent(node)
            # print("mehtodName: ", methodName)
            IOmethods = ["out_int", "out_string", "in_int", "in_string", "out_bool", "in_bool"]

            if methodName == "return":

                # print("nodeScope: ", nodeScope)
                # print("methodName: ", methodName)

                node_value = self.getExprChildren(node.children[2])

                methodScope = self.getMethodParent(node)

                wholeScope = nodeScope + "." + methodScope

                # print("wholeScope: ", wholeScope)

                # print("node_value: ", node_value)

                methodType = None

                methodreturnType = None

                node_value_string =  " ".join(node_value)

                if "+" in node_value_string:
                    lista_temp = node_value_string.split("+")
                    # print("lista_temp: ", lista_temp)
                    lista_tipos = []
                    for item in lista_temp:
                        
                        item = item.strip(" ")

                        if item in self.names:
                            symbolIo2 = self.symbol_table.lookup(item)
                            lista_tipos.append(symbolIo2.data_type)
                        else:
                            lista_tipos.append(self.tokenDict[item])
                        
                    if all(value.lower() == lista_tipos[0].lower() for value in lista_tipos):

                        symbolType = lista_tipos[0]

                        return None
                    
                    else:

                        return f"Los parametros de '{methodName}' deben ser del mismo tipo"

                for symbol_temp in self.symbol_table.symbols:

                    # print("symbol_temp.name: ", symbol_temp.name)
                    # print("symbol_temp.scope: ", symbol_temp.scope)
                    # print(symbol_temp.name == methodName)
                    # print(symbol_temp.scope == wholeScope)

                    if str(symbol_temp.name) == str(methodName) and str(symbol_temp.scope) == str(wholeScope):

                        methodType = symbol_temp.value
                    
                    if symbol_temp.name == methodScope and symbol_temp.scope == nodeScope and symbol_temp.id_type == "Method":

                        methodreturnType = symbol_temp.data_type



                # print("methodType: ", methodType)
                # print("methodreturnType: ", methodreturnType)

                method_type_2 = None
                if methodType in self.names:

                    method_type_2 = self.symbol_table.lookup_all(methodType).data_type

                    if method_type_2.lower() != methodreturnType.lower():

                        return f"El metodo {methodScope} debe retornar un '{methodreturnType}' no un '{method_type_2}'"

                else:

                    method_type_2 = self.tokenDict[methodType]

                    if methodType == "self":

                        if methodreturnType != "SELF_TYPE":

                            return f"El metodo {methodScope} debe retornar un '{methodreturnType}' no un '{methodType}'"

                    else:

                        if method_type_2.lower() != methodreturnType.lower():

                            return f"El metodo {methodScope} debe retornar un '{methodreturnType}' no un '{method_type_2}'"


                # print(method_type_2)   

                return None

            # Verifica que el metodo este definido en el scope
            for symbol in self.symbol_table.symbols:
               
                # Verifica que el metodo este definido en el scope actual

                if methodName not in IOmethods:
                    
                    if symbol.name == methodName and symbol.id_type == "Method" and symbol.scope.startswith(nodeScope):

                        # Queremos revisar que los parametros definidos sean los correctos

                        # Para este metodo

                        # test(x : Int) : Int {
                        #     out_int(2)
                        # };

                        # Estamos revisando que la llamada "test("1");" sea correcta
                        # 

                        # Guardamos los parametros del metodo en una lista

                        # print(">methodName: ", methodName)

                        parameters = []
                        for symbol in self.symbol_table.symbols:
                            if methodName in symbol.scope and symbol.id_type == "Parameter" and symbol.scope.startswith(nodeScope):
                                parameters.append(symbol.data_type)    

                        # print(">parameters: ", parameters)  

                        # Verifica que los parametros de la llamada sean los correctos

                        for symbol in self.symbol_table.symbols:

                            # Se verifica para un method call

                            if symbol.name == methodName and symbol.id_type == "MethodCall":
                                if symbol.value in self.names:
                                    symbol = self.symbol_table.lookup(symbol.value)
                                    symbolType = symbol.data_type
                                else:
                                    # print(symbol)
                                    symbolType = self.tokenDict[symbol.value]
                                if symbol.name in IOmethods:
                                    pass
                                else:
                                    # print(len(parameters)) 
                                    if len(parameters) == 1 and parameters[0].lower() == symbolType.lower():
                                        return None
                                    else:
                                        return f"El metodo '{methodName}' debe recibir {len(parameters)} parametro(s) de tipo '{', '.join(parameters)}'"

                            # Se verifica para un Procedure call

                            elif symbol.name == methodName and symbol.id_type == "Procedure":
                               
                                if symbol.value in self.names:
                                    symbol = self.symbol_table.lookup(symbol.value)
                                    symbolType = symbol.data_type
                                else:
                                    symbolType = self.tokenDict[symbol.value]
                                if symbol.name in IOmethods:
                                    pass
                                else:
                                    # print(len(parameters)) 
                                    if len(parameters) == 1 and parameters[0].lower() == symbolType.lower():
                                        return None
                                    else:
                                        return f"El metodo '{methodName}' debe recibir {len(parameters)} parametro(s) de tipo '{', '.join(parameters)}'"


                        return None
 




                # Si son parte del IO revisa que el parametro sea el correcto
                
                else:
                    for symbol3 in self.symbol_table.symbols:
                        if symbol3.name == methodName:

                            if symbol3.value in self.names:
                                symbolIo2 = self.symbol_table.lookup(symbol3.value)
                                symbolType = symbolIo2.data_type
                            else:
                                # print(symbol)
                                if "+" in symbol3.value:
                                    lista_temp = symbol3.value.split("+")
                                    lista_tipos = []
                                    for item in lista_temp:
                                        
                                        item = item.strip(" ")

                                        if item in self.names:
                                            symbolIo2 = self.symbol_table.lookup(item)
                                            lista_tipos.append(symbolIo2.data_type)
                                        else:
                                            lista_tipos.append(self.tokenDict[item])
                                        
                                    if all(value.lower() == lista_tipos[0].lower() for value in lista_tipos):

                                        symbolType = lista_tipos[0]
                                    
                                    else:

                                        return f"Los parametros de '{methodName}' deben ser del mismo tipo"

                                else:
                                    symbolType = self.tokenDict[symbol3.value]
                            
                            if symbol3.name == IOmethods[0] or symbol3.name == IOmethods[2]:
                                if symbolType.lower() != "int":
                                    return f"El metodo '{methodName}' debe recibir un parametro de tipo 'int'"

                            elif symbol3.name == IOmethods[1] or symbol3.name == IOmethods[3]:
                                if symbolType.lower() != "string":
                                    return f"El metodo '{methodName}' debe recibir un parametro de tipo 'string'"
                            
                            elif symbol3.name == IOmethods[4] or symbol3.name == IOmethods[5]:
                                if symbolType.lower() != "bool":
                                    return f"El metodo '{methodName}' debe recibir un parametro de tipo 'bool'"
                      
                    # symbol2 = self.symbol_table.lookup_all("Main")
                    try:
                        if symbol.name == "IO":
                            return None
                    except:
                        pass

            # Si termina el for sin retornar es porque no encontro el metodo (No esta definido en el scope)        
            if methodName == "String" or methodName == "Bool" or methodName == "Int":
                return f"No se permite el casteo explicito {methodName}"
            else:
                return f"El metodo '{methodName}' no ha sido definido en el scope '{nodeScope}'"
        
        # Methodcall con uno o mas varios parametros
        elif len(node.children) > 4 and node.children[1].val == "(" and node.children[-1].val == ")":
            methodName = node.children[0].val

            nodeScope = self.getClassDefineParent(node)

            #revisar que los parametros si sean los correctos
            parameters = []

            
            for symbol in self.symbol_table.symbols:
                if methodName in symbol.scope and symbol.id_type == "Parameter" and symbol.scope.startswith(nodeScope):
                    parameters.append(symbol.data_type)

            # No existe ese metodo en el scope
            if len(parameters) == 0:

                return f"El metodo '{methodName}' no ha sido definido en el scope '{nodeScope}'"

            for symbol in self.symbol_table.symbols:
                if symbol.name == methodName and symbol.id_type == "MethodCall":
                    separate_parameters = symbol.value.split(",")
                    typeParameters = []
                    if len(parameters) == len(separate_parameters):
                        # print(separate_parameters)

                        for param in separate_parameters:
                            if param in self.names:
                                symbol = self.symbol_table.lookup(param)
                                typeParameters.append(symbol.data_type)
                            else:
                                typeParameters.append(self.tokenDict[param])
                        
                        for i in range(len(parameters)):
                            if parameters[i].lower() != typeParameters[i].lower():
                                return f"El metodo '{methodName}' debe recibir {len(parameters)} parametro(s) de tipo '{', '.join(parameters)}'"
                    else:
                        return f"El metodo '{methodName}' debe recibir {len(parameters)} parametro(s) de tipo '{', '.join(parameters)}'"

    # HELPER METHODS

    # Agarramos el scope de la clase
    def getClassDefineParent(self, node):
        if node.val == "classDefine":
            return node.children[1].val
        
        return self.getClassDefineParent(node.parent)
    
    # Agarramos el scope del metodo
    def getMethodParent(self, node):
        if node.val == "method":
            return node.children[0].val
        return self.getMethodParent(node.parent)

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
    
    # Verifica que las comparaciones sean validas
    def check_comparisons(self, node):

        primera_comparacion = node.children[1]

        expresion = self.getExprChildren(primera_comparacion)

        variables_comparadas = [expresion[0], expresion[2]]

        tipos_datos_comparados = []

        for variable in variables_comparadas:

            # Si es una variable no declarada

            if variable in self.names:

                symbol_temporal = self.symbol_table.lookup(variable)

                tipos_datos_comparados.append(symbol_temporal.data_type)
            
            # Si es un token

            else:

                tipo_dato = self.tokenDict[variable]

                tipos_datos_comparados.append(tipo_dato)

        if tipos_datos_comparados[0].lower() != tipos_datos_comparados[1].lower():

            if tipos_datos_comparados[0].lower() in ["int","false","true"] and tipos_datos_comparados[1].lower() in ["int","false","true"]:

                return None

            return f"La comparacion '{tipos_datos_comparados[0].lower()} con {tipos_datos_comparados[1].lower()}' no es valida"


        return None

    # Revisa que no se declaren dos veces el mismo identificador
    def checkDoubleDeclarations(self):

        poissbleErrors = []

        lista_tuplas = []

        for symbol in self.symbol_table.symbols:

            if (symbol.name, symbol.scope) in lista_tuplas:

                if symbol.id_type == "MethodCall" or symbol.id_type == "Procedure":

                    pass
                
                else:

                    poissbleErrors.append(f"ERROR SEMANTICO: El identificador '{symbol.name}' ya ha sido declarado en el scope '{symbol.scope}': Linea {symbol.line}")
            
            else:

                lista_tuplas.append((symbol.name, symbol.scope))
        
        return poissbleErrors


class SemanticAnalyzer:
    def __init__(self, parse_tree, symbol_table, tokenDict):
        self.parse_tree = parse_tree
        self.symbol_table = symbol_table
        self.tokenDict = tokenDict
        self.visitor = SemanticVisitor(self.symbol_table, self.tokenDict)
        self.errors = []

    def analyze(self):
        self.traverse_tree(self.parse_tree.root)

        checkDoubleDeclarations_errors = self.visitor.checkDoubleDeclarations()

        if checkDoubleDeclarations_errors:
            for error in checkDoubleDeclarations_errors:
                self.errors.append(error)
        
        self.display_errors()



    def traverse_tree(self, node):
        if node is not None:
            method_name = "visit_" + node.val.lower() + "_node"
            if hasattr(self.visitor, method_name):
                visit_method = getattr(self.visitor, method_name)
                error_message = visit_method(node)
                if error_message:
                    line_number = node.line
                    self.report_error(error_message, line_number)
            for child in node.children:
                self.traverse_tree(child)

    def report_error(self, message, line_number):
        error = f"{message}: Linea {line_number}"
        self.errors.append("ERROR SEMANTICO: " +  error)

    def display_errors(self):
        if self.errors:
            print("\nERRORES SEMANTICOS DETECTADOS:")
            for error in self.errors:
                print(error)
        else:
            print("No se encontraron errores semanticos.")

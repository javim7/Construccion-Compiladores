class SemanticVisitor:
    def __init__(self, symbol_table, tokenDict):
        self.symbol_table = symbol_table
        self.tokenDict = tokenDict
        self.names, self.ids, self.dataTypes, self.values, self.inheritsFroms, self.scopes, self.lines = self.symbol_table.allInfo()

    def visit_program_node(self, node):
        MainClass = False
        for children in node.children:
            if children.val == "classDefine":
                if children.children[1].val == "Main":
                    MainClass = True
        
        if not MainClass:
            return f"El programa debe tener una clase 'Main'"
        return None

    def visit_classdefine_node(self, node):
        class_name = node.children[1].val
        method_names = [symbol.name for symbol in self.symbol_table.symbols if symbol.id_type == "Method" and symbol.scope.startswith(class_name)]
        
        #ver si hace falta la clase main
        if class_name == "Main" and "main" not in method_names:
            return f"La clase 'Main' debe tener un metodo 'main'"
        #ver si alguna clase hereda a Main
        if node.children[2].val == "inherits" and node.children[3].val == "Main":
            return f"La clase 'Main' no puede heredar de ninguna otra clase"
        
        return None


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
                        if int(symbol.value) == 0:
                            print("false")
                            self.symbol_table.update_symbol_value(var_name, False)
                        else:
                            print("true")
                            self.symbol_table.update_symbol_value(var_name, True)
                        self.symbol_table.display()
                    else:
                        return f"La variable '{var_name}' debe ser de tipo '{var_type}' no '{symbol.data_type}'"
            
            elif value_node.val in self.tokenDict:
                valueType = self.tokenDict[value_node.val]
                
                if valueType.lower() != var_type.lower():
                    if var_type.lower() == "int" and valueType.lower() == "bool":
                        print(var_name)
                    elif var_type.lower() == "bool" and valueType.lower() == "int":
                        pass
                    else:
                        return f"La variable '{var_name}' debe ser de tipo '{var_type}' no '{valueType}'"

        else:
            child_values = self.getExprChildren(expr_node)
            operators = []
            alphanum = []
            variables = {}

            stringOperators = ["+", ","]
            intOperators = ["+", "-", "*", "/", "%", "(", ")"]

            # print("child_values: ", child_values)
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
          
            firstVal = next(iter(variables.values()))
            if all(value == firstVal for value in variables.values()):
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
                return f"Las variables '{alphanum}' deben ser del mismo tipo '{var_type}'"

        return None

    def visit_expr_node(self, node):
        
        if len(node.children) == 3 and node.children[1].val == "(" and node.children[2].val == ")":
            methodName = node.children[0].val
            nodeScope = self.getClassDefineParent(node)
            for symbol in self.symbol_table.symbols:
                if symbol.name == methodName and symbol.id_type == "Method" and symbol.scope.startswith(nodeScope):
                    return None
            
            return f"El metodo '{methodName}' no ha sido definido en el scope '{nodeScope}'"
        
        elif len(node.children) == 4 and node.children[1].val == "(" and node.children[3].val == ")":
            methodName = node.children[0].val
            nodeScope = self.getClassDefineParent(node)
            # print("mehtodName: ", methodName)
            IOmethods = ["out_int", "out_string", "in_int", "in_string"]

            # ver que el metodo este definido
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

                        print(">methodName: ", methodName)

                        parameters = []
                        for symbol in self.symbol_table.symbols:
                            if methodName in symbol.scope and symbol.id_type == "Parameter" and symbol.scope.startswith(nodeScope):
                                parameters.append(symbol.data_type)    

                        print(">parameters: ", parameters)  

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
                                symbolType = self.tokenDict[symbol3.value]
                            
                            if symbol3.name == IOmethods[0] or symbol3.name == IOmethods[2]:
                                if symbolType.lower() != "int":
                                    return f"El metodo '{methodName}' debe recibir un parametro de tipo 'int'"

                            elif symbol3.name == IOmethods[1] or symbol3.name == IOmethods[3]:
                                if symbolType.lower() != "string":
                                    return f"El metodo '{methodName}' debe recibir un parametro de tipo 'string'"
                      
                    symbol2 = self.symbol_table.lookup_all("Main")
                    try:
                        if symbol2.inheritsFrom == "IO":
                            return None
                    except:
                        pass

            # Si termina el for sin retornar es porque no encontro el metodo (No esta definido en el scope)        

            return f"El metodo '{methodName}' no ha sido definido en el scope '{nodeScope}'"
        
        elif len(node.children) > 4 and node.children[1].val == "(" and node.children[-1].val == ")":
            methodName = node.children[0].val

            nodeScope = self.getClassDefineParent(node)

            #revisar que los parametros si sean los correctos
            parameters = []
            for symbol in self.symbol_table.symbols:
                if methodName in symbol.scope and symbol.id_type == "Parameter" and symbol.scope.startswith(nodeScope):
                    parameters.append(symbol.data_type)

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

    def getClassDefineParent(self, node):
        if node.val == "classDefine":
            return node.children[1].val
        
        return self.getClassDefineParent(node.parent)

    def getExprChildren(self, node, child_values=None):
        if child_values is None:
            child_values = []  # Initialize the list only in the initial call
        
        for child in node.children:
            if child.val == "expr":
                self.getExprChildren(child, child_values)  # Pass the existing list to the recursive call
            else:
                child_values.append(child.val)
        
        return child_values

class SemanticAnalyzer:
    def __init__(self, parse_tree, symbol_table, tokenDict):
        self.parse_tree = parse_tree
        self.symbol_table = symbol_table
        self.tokenDict = tokenDict
        self.visitor = SemanticVisitor(self.symbol_table, self.tokenDict)
        self.errors = []

    def analyze(self):
        self.traverse_tree(self.parse_tree.root)
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

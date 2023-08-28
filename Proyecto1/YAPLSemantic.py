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
        if class_name == "Main" and "main" not in method_names:
            return f"La clase 'Main' debe tener un metodo 'main'"
        return None

    def visit_method_node(self, node):
        if node.children[0].val == "main" and node.children[2].val == "formal":
            return f"El metodo 'main' no puede tener parametros formales"

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
                    return f"La variable '{var_name}' debe ser de tipo '{var_type}' no '{symbol.data_type}'"
            
            elif value_node.val in self.tokenDict:
                valueType = self.tokenDict[value_node.val]
                
                if valueType.lower() != var_type.lower():
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
        # print(node)
        if len(node.children) == 3 and node.children[1].val == "(" and node.children[2].val == ")":
            methodName = node.children[0].val
            for symbol in self.symbol_table.symbols:
                if symbol.name == methodName and symbol.id_type == "Method":
                    return None
            
            return f"El metodo '{methodName}' no ha sido definido"
        
        elif len(node.children) == 4 and node.children[1].val == "(" and node.children[3].val == ")":
            methodName = node.children[0].val
            # print("mehtodName: ", methodName)
            IOmethods = ["out_int", "out_string", "in_int", "in_string"]
            for symbol in self.symbol_table.symbols:
               
                if methodName not in IOmethods:
                    if symbol.name == methodName and symbol.id_type == "Method":
                        return None
                else:
                    symbol = self.symbol_table.lookup_all("Main")
                    try:
                        if symbol.inheritsFrom == "IO":
                            return None
                    except:
                        pass
                    
            return f"El metodo '{methodName}' no ha sido definido"

    def perform_semantic_analysis(self):
        # Implement your semantic analysis rules here
        pass

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
        self.errors.append(error)

    def display_errors(self):
        if self.errors:
            print("\nERRORES SEMANTICOS DETECTADOS:")
            for error in self.errors:
                print("ERROR: " + error)
        else:
            print("No se encontraron errores semanticos.")

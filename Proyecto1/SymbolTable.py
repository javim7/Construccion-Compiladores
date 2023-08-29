from prettytable import PrettyTable

class Symbol:
    def __init__(self, name, id_type, data_type, value, inheritsFrom, scope, line):
        self.name = name
        self.id_type = id_type
        self.data_type = data_type
        self.value = value
        self.inheritsFrom = inheritsFrom
        self.scope = scope
        self.line = line
    
    def update_value(self, new_value):
        # Verificar si el nuevo valor tiene el mismo tipo que el tipo original del símbolo
        # print("new_value: ", new_value)
        # print("old value: ", self.value)
        # if type(new_value) != type(self.value):
        #     raise ValueError(f"Invalid type for new value of symbol '{self.name}': {type(new_value)}")
        
        self.value = new_value

    def update_data_type(self, new_data_type):
        # Verificar si el nuevo tipo es un tipo válido 
        valid_data_types = ['int', 'float', 'string', 'bool']  # Lista de tipos válidos
        if new_data_type not in valid_data_types:
            raise ValueError(f"Invalid data type for symbol '{self.name}': {new_data_type}")

        # Verificar si el nuevo tipo es diferente al tipo original del símbolo
        if new_data_type != self.data_type:
            # Realizar cualquier acción adicional requerida cuando el tipo cambia 
            self.data_type = new_data_type

    def __str__(self):
        return f"Name: {self.name}\nVar Type: {self.id_type}\nData Type: {self.data_type}\nValue: {self.value}\nInherits From: {self.inheritsFrom}\nScope: {self.scope}\nLine: {self.line}\n"


class SymbolTable:
    def __init__(self):
        self.symbols = []

    def insert(self, symbolEntry):
        for symbol in self.symbols:
            if symbolEntry.name == symbol.name and symbolEntry.scope == symbol.scope:

                if symbol.id_type == "Procedure" or symbol.id_type == "MethodCall":
                    pass
                else:
                    # raise ValueError(f"Symbol '{symbolEntry.name}' already exists in the same scope: {symbolEntry.scope}.")
                    pass
            
        valid_data_types = ['int', 'float', 'string', 'bool', "class", "id", "block_comment", "type", "object", "self_type", "void", "list"]  # Lista de tipos válidos
        if symbolEntry.data_type.lower() not in valid_data_types:
            raise ValueError(f"Invalid data type for symbol '{symbolEntry.name}': {symbolEntry.data_type}")
        
        self.symbols.append(symbolEntry)

    def lookup(self, name):
        symbol = None
        for s in self.symbols:
            if s.name == name:
                symbol = s
                break
        if symbol is None:
            raise ValueError(f"Symbol '{name}' not found in the table.")
        
        return symbol
    
    def lookup_all(self, name):
        for s in self.symbols:
            if s.name == name:
                return s
        return None
    
    def detailed_lookup(self, name, value):
        for s in self.symbols:
            if s.name == name and s.value == value:
                return s
        return None
    
    def lookup_by_scope(self, name, scope):
        for s in self.symbols:
            if s.name == name and s.scope == scope:
                return s
        return None

    def allInfo(self):
        names = []
        ids = []
        dataTypes = []
        values = []
        inheritsFroms = []
        scopes = []
        lines = []

        for s in self.symbols:
            names.append(s.name)
            ids.append(s.id_type)
            dataTypes.append(s.data_type)
            values.append(s.value)
            inheritsFroms.append(s.inheritsFrom)
            scopes.append(s.scope)
            lines.append(s.line)

        return names, ids, dataTypes, values, inheritsFroms, scopes, lines

    def remove(self, name):
        symbol = None
        for s in self.symbols:
            if s.name == name:
                symbol = s
                break
        if symbol is None:
            raise ValueError(f"Symbol '{name}' not found in the table.")
        
        self.symbols.remove(symbol)
        print("Symbol removed successfully.")
    
    def update_symbol_value(self, symbol_name, new_value):
        symbol = self.lookup(symbol_name)
        # print("symbol: ", symbol)
        symbol.update_value(new_value)

    def update_symbol_data_type(self, symbol_name, new_data_type):
        symbol = self.lookup(symbol_name)
        symbol.update_data_type(new_data_type)

    def update_symbol_line(self, symbol_name, new_line):
        symbol = self.lookup(symbol_name)
        symbol.line = new_line

    # def display(self):
    #     for symbol in self.symbols.values():
    #         print(symbol)
    def display(self):
        table = PrettyTable()
        table.field_names = ["Name", "ID Type", "Data Type", "Value","Inherits","Scope", "Line"]

        for symbol in self.symbols:
            table.add_row([symbol.name, symbol.id_type, symbol.data_type, symbol.value,symbol.inheritsFrom, symbol.scope, symbol.line])

        print(table)
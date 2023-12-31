from prettytable import PrettyTable

class Symbol:
    def __init__(self, name, data_type, value):
        self.name = name
        self.data_type = data_type
        self.value = value
    
    def update_value(self, new_value):
        # Verificar si el nuevo valor tiene el mismo tipo que el tipo original del símbolo
        if type(new_value) != type(self.value):
            raise ValueError(f"Invalid type for new value of symbol '{self.name}': {type(new_value)}")
        
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
        return f"{self.name}: {self.data_type} = {self.value}"


class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def insert(self, symbol):
        if symbol.name in self.symbols:
            raise ValueError(f"Symbol '{symbol.name}' already exists in the table.")
        
        # Verificar tipo válido (opcional)
        valid_data_types = ['int', 'float', 'string', 'bool']  # Lista de tipos válidos
        if symbol.data_type not in valid_data_types:
            raise ValueError(f"Invalid data type for symbol '{symbol.name}': {symbol.data_type}")
        
        self.symbols[symbol.name] = symbol

    def lookup(self, name):
        symbol = self.symbols.get(name, None)
        if symbol is None:
            raise ValueError(f"Symbol '{name}' not found in the table.")
        return symbol

    def remove(self, name):
        if name not in self.symbols:
            raise ValueError(f"Symbol '{name}' not found in the table.")
        del self.symbols[name]
    
    def update_symbol_value(self, symbol_name, new_value):
        symbol = self.lookup(symbol_name)
        symbol.update_value(new_value)

    def update_symbol_data_type(self, symbol_name, new_data_type):
        symbol = self.lookup(symbol_name)
        symbol.update_data_type(new_data_type)

    # def display(self):
    #     for symbol in self.symbols.values():
    #         print(symbol)
    def display(self):
        table = PrettyTable()
        table.field_names = ["Name", "Data Type", "Value"]

        for symbol in self.symbols.values():
            table.add_row([symbol.name, symbol.data_type, symbol.value])

        print(table)


# Ejemplo de uso
if __name__ == "__main__":
    table = SymbolTable()

    symbol1 = Symbol("x", "int", 42)
    symbol2 = Symbol("y", "float", 3.14)

    try:
        table.insert(symbol1)
        table.insert(symbol2)
        table.insert(symbol1)  # Esto generará un error, ya que 'x' ya existe en la tabla.
    except ValueError as e:
        print(f"Error: {e}")

    try:
        table.lookup("z")  # Esto generará un error, ya que 'z' no existe en la tabla.
    except ValueError as e:
        print(f"Error: {e}")

    table.display()

    '''
    el output de este programa es:
    Error: Symbol 'x' already exists in the table.
    Error: Symbol 'z' not found in the table.
    +------+-----------+-------+
    | Name | Data Type | Value |
    +------+-----------+-------+
    |  x   |    int    |   42  |
    |  y   |   float   |  3.14 |
    +------+-----------+-------+
    '''
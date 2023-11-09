class Assembler2:
    def __init__(self, cuadruplas):
        self.cuadruplas = cuadruplas
        self.data_section = ".data\n"
        self.text_section = "\n.text\n.globl main\n"
        self.variables = set()
        self.variables_cargadas = {}
        self.temp_counter = 0

    def get_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def generar_codigo_mips(self):

        indentation = 0

        for cuadrupla in self.cuadruplas:

            # Agregar variables con sus valores originales a la sección de datos
            if cuadrupla.operador == '<-':
                if cuadrupla.resultado not in self.variables:
                    self.data_section += f"{cuadrupla.resultado}: .word {cuadrupla.operando1}\n"
                    self.variables.add(cuadrupla.resultado)
                else:
                    self.text_section += f"{'    ' * indentation}sw $t{self.temp_counter-1}, {cuadrupla.resultado}\n"

            # Metodos
            elif cuadrupla.operador == 'METHOD_START':
                indentation = 0
                self.text_section += f"\n{' ' * indentation} {cuadrupla.operando1}:\n"
                indentation += 1

            # Operaciones aritmeticas
            elif cuadrupla.operador in ['+', '-', '*', '/']:
                # cargar valores iniciales

                if cuadrupla.operando1 not in self.variables_cargadas:
                    temp1 = self.get_temp()
                    self.text_section += f"{'    ' * indentation}lw ${temp1}, {cuadrupla.operando1}\n"
                    self.variables_cargadas[cuadrupla.operando1] = temp1
                if cuadrupla.operando2 not in self.variables_cargadas:
                    temp2 = self.get_temp()
                    self.text_section += f"{'    ' * indentation}lw ${temp2}, {cuadrupla.operando2}\n"
                    self.variables_cargadas[cuadrupla.operando2] = temp2

                temp3 = self.get_temp()

                if cuadrupla.operador == '+':
                    self.text_section += f"\n{'    ' * indentation}add ${temp3}, ${self.variables_cargadas[cuadrupla.operando1]}, ${self.variables_cargadas[cuadrupla.operando2]}\n"
                elif cuadrupla.operador == '-':
                    self.text_section += f"\n{'    ' * indentation}sub ${temp3}, ${self.variables_cargadas[cuadrupla.operando1]}, ${self.variables_cargadas[cuadrupla.operando2]}\n"
                elif cuadrupla.operador == '*':
                    self.text_section += f"\n{'    ' * indentation}mul ${temp3}, ${self.variables_cargadas[cuadrupla.operando1]}, ${self.variables_cargadas[cuadrupla.operando2]}\n"
                elif cuadrupla.operador == '/':
                    self.text_section += f"\n{'    ' * indentation}div ${self.variables_cargadas[cuadrupla.operando1]}, ${self.variables_cargadas[cuadrupla.operando2]}\n"
                    self.text_section += f"{'    ' * indentation}mflo ${temp3}\n"
                    temp4 = self.get_temp()
                    self.text_section += f"{'    ' * indentation}mfhi ${temp4}\n"
                    self.temp_counter -= 1
                # self.text_section += f"{'    ' * indentation}sw ${temp3}, {cuadrupla.resultado}\n"


         # Finalizar el programa
        indentation = 0
        self.text_section += "\nli $v0, 10    # Código de salida\nsyscall       # Ejecutar syscall para terminar\n"

        return self.data_section + self.text_section
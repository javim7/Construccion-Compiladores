class Assembler2:
    def __init__(self, cuadruplas):
        self.cuadruplas = cuadruplas
        self.data_section = ".data\n"
        self.text_section = "\n.text\n.globl main\n"
        self.variables = set()
        self.methods = []
        self.variables_cargadas = {}
        self.temp_counter = 0
        self.a_counter = 0
        self.v_counter = 0

    def get_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def get_a(self):
        a = f"a{self.a_counter}"
        self.a_counter += 1
        return a
    
    def get_v(self):
        v = f"v{self.v_counter}"
        self.v_counter += 1
        return v
    
    def generar_codigo_mips(self):

        indentation = 0

        for cuadrupla in self.cuadruplas:

            # Variables
            if cuadrupla.operador == '<-':
                if cuadrupla.resultado not in self.variables: # agregar variables a la seccion de datos
                    if cuadrupla.operando2 == 'String':
                        self.data_section += f"{cuadrupla.resultado}: .asciiz {cuadrupla.operando1}\n"
                        self.variables.add(cuadrupla.resultado)
                    elif cuadrupla.operando2 == 'Int':
                        self.data_section += f"{cuadrupla.resultado}: .word {cuadrupla.operando1}\n"
                        self.variables.add(cuadrupla.resultado) 
                    elif cuadrupla.operando2 == 'Bool':
                        self.data_section += f"{cuadrupla.resultado}: .word {1 if cuadrupla.operando1 == 'true' else 0}\n"
                        self.variables.add(cuadrupla.resultado)

                else: # actualizar variables en las operaciones aritmeticas
                    self.text_section += f"{'    ' * indentation}sw $t{self.temp_counter-1}, {cuadrupla.resultado}\n"
                    self.variables_cargadas[cuadrupla.resultado] = f"t{self.temp_counter-1}"

            # Metodos
            elif cuadrupla.operador == 'METHOD_START':
                indentation = 0
                if len(self.methods) >= 1 and cuadrupla.operando1 not in self.methods and self.methods[-1] == 'main':
                    # Finalizar el programa
                    self.text_section += f"\n{'    '}li $v0, 10    # Código de salida\n{'    '}syscall       # Ejecutar syscall para terminar\n"

                self.text_section += f"\n{'    ' * indentation} {cuadrupla.operando1}:\n"
                self.methods.append(cuadrupla.operando1)
                indentation += 1

            # Operaciones aritmeticas
            elif cuadrupla.operador in ['+', '-', '*', '/']:
               
                # verificar si las variables ya estan cargadas en los registros
                if cuadrupla.operando1 not in self.variables_cargadas:
                    temp1 = self.get_temp()
                    self.text_section += f"\n{'    ' * indentation}lw ${temp1}, {cuadrupla.operando1}\n"
                    self.variables_cargadas[cuadrupla.operando1] = temp1
                if cuadrupla.operando2 not in self.variables_cargadas:
                    temp2 = self.get_temp()
                    self.text_section += f"{'    ' * indentation}lw ${temp2}, {cuadrupla.operando2}\n"
                    self.variables_cargadas[cuadrupla.operando2] = temp2

                # temporal para guardar el resultado
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

            # Prints
            elif cuadrupla.operador == 'PROCEDURE':

                # out_int
                if cuadrupla.operando1 == 'out_int':
                    self.text_section += f"\n{'    ' * indentation}li $v0, 1\n"
                    self.text_section += f"{'    ' * indentation}move $a0, ${self.variables_cargadas[cuadrupla.operando2]}\n"
                    self.text_section += f"{'    ' * indentation}syscall\n"
                
                # out_string
                elif cuadrupla.operando1 == 'out_string':
                    self.text_section += f"\n{'    ' * indentation}li $v0, 4\n"
                    self.text_section += f"{'    ' * indentation}move $a0, ${self.variables_cargadas[cuadrupla.operando2]}\n"
                    self.text_section += f"{'    ' * indentation}syscall\n"

        if len(self.methods) == 1:
            # Finalizar el programa
            self.text_section += f"\n{'    ' * indentation}li $v0, 10    # Código de salida\n{'    ' * indentation}syscall       # Ejecutar syscall para terminar\n"

        return self.data_section + self.text_section
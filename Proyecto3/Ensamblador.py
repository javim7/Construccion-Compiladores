class Assembler:
    def __init__(self, cuadruplas):

        self.cuadruplas_iniciales = cuadruplas
        self.data_section = ".data\n"
        self.text_section = "\n.text\n.globl main\n"
        self.variables = set()
        self.methods = []
        self.stack = []
        self.variables_cargadas = {}
        self.argumentos = {}
        self.resultados = {}
        self.temp_counter = 0
        self.a_counter = 0
        self.v_counter = 0
        self.indentation = 0

        self.cuadruplas_procesadas = set()

        self.recorrer_cuadruplas(self.cuadruplas_iniciales)



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
    
    def recorrer_cuadruplas(self,cuadruplas_actuales):

        for indice, cuadrupla in enumerate(cuadruplas_actuales):

            print("Procesando cuadrupla numero: ", indice, " con valor: ", cuadrupla)
            self.generar_codigo_mips(cuadrupla) 

    def generar_codigo_mips(self, cuadrupla_actual):

        # Revisamos si la cuadrupla ya fue procesada:

        if cuadrupla_actual in self.cuadruplas_procesadas:
            return
        
        self.cuadruplas_procesadas.add(cuadrupla_actual)

        # Variables

        if cuadrupla_actual.operador == '<-':
            self.mips_asignacion(cuadrupla_actual)
        
        # Metodos

        if cuadrupla_actual.operador == 'METHOD_START':
            self.mips_metodos(cuadrupla_actual)
    
        # Operaciones aritmeticas

        if cuadrupla_actual.operador in ['+', '-', '*', '/']:
            self.mips_aritmetica(cuadrupla_actual)

    def mips_aritmetica(self, cuadrupla):
        # verificar si las variables ya estan cargadas en los registros
        if cuadrupla.operando1 not in self.variables_cargadas:
            temp1 = self.get_temp()
            self.text_section += f"\n{'    ' * self.indentation}lw ${temp1}, {cuadrupla.operando1}\n"
            self.variables_cargadas[cuadrupla.operando1] = temp1
        if cuadrupla.operando2 not in self.variables_cargadas:
            temp2 = self.get_temp()
            self.text_section += f"{'    ' * self.indentation}lw ${temp2}, {cuadrupla.operando2}\n"
            self.variables_cargadas[cuadrupla.operando2] = temp2

        # temporal para guardar el resultado
        temp3 = self.get_temp()

        if cuadrupla.operador == '+':
            self.text_section += f"\n{'    ' * self.indentation}add ${temp3}, ${self.variables_cargadas[cuadrupla.operando1]}, ${self.variables_cargadas[cuadrupla.operando2]}\n"
        elif cuadrupla.operador == '-':
            self.text_section += f"\n{'    ' * self.indentation}sub ${temp3}, ${self.variables_cargadas[cuadrupla.operando1]}, ${self.variables_cargadas[cuadrupla.operando2]}\n"
        elif cuadrupla.operador == '*':
            self.text_section += f"\n{'    ' * self.indentation}mul ${temp3}, ${self.variables_cargadas[cuadrupla.operando1]}, ${self.variables_cargadas[cuadrupla.operando2]}\n"
        elif cuadrupla.operador == '/':
            self.text_section += f"\n{'    ' * self.indentation}div ${self.variables_cargadas[cuadrupla.operando1]}, ${self.variables_cargadas[cuadrupla.operando2]}\n"
            self.text_section += f"{'    ' * self.indentation}mflo ${temp3}\n"
            temp4 = self.get_temp()
            self.text_section += f"{'    ' * self.indentation}mfhi ${temp4}\n"
            self.temp_counter -= 1

    def mips_metodos(self, cuadrupla):
        
        self.indentation = 0
        if len(self.methods) >= 1 and cuadrupla.operando1 not in self.methods and self.methods[-1] == 'main':
            # Finalizar el programa
            self.text_section += f"\n{'    '}li $v0, 10    # Código de salida\n{'    '}syscall       # Ejecutar syscall para terminar\n"

        self.text_section += f"\n{cuadrupla.operando1}:\n"
        self.methods.append(cuadrupla.operando1)
        self.indentation += 1

    def mips_asignacion(self, cuadrupla):

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
        else:
            self.text_section += f"{'    ' * self.indentation}sw $t{self.temp_counter-1}, {cuadrupla.resultado}\n"
            self.variables_cargadas[cuadrupla.resultado] = f"t{self.temp_counter-1}"
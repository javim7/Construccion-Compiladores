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
    
    def recorrer_cuadruplas(self,cuadruplas_actuales, cuadrupla_exit_label = None):

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

        # Prints

        if cuadrupla_actual.operador == 'PROCEDURE':
            self.mips_procedure(cuadrupla_actual)
        
        # Ifs simples

        if cuadrupla_actual.operador == 'IFS':
            self.mips_ifs(cuadrupla_actual)
        
        # Jumps

        if cuadrupla_actual.operador == 'JUMP':
            self.mips_jump(cuadrupla_actual)

        # Whiles simples

        if cuadrupla_actual.operador == 'WHL':
            self.mips_while(cuadrupla_actual)
                
    def mips_jump(self, cuadrupla):
        self.text_section += f"\n{'    ' * self.indentation}j {cuadrupla.resultado}\n"

    def mips_while(self, cuadrupla):
        
        # La cuadrupla actual luce de la siguiente manera:

        # WHL      |    ---     |    ---     |    ---

        # La siguiente cuadrupla es la que contiene la label de inicio del while

        # LABEL    |    None    |    None    |     L1    |

        # Obtenemos la cuadrupla siguiente

        cuadrupla_siguiente = self.cuadruplas_iniciales[self.cuadruplas_iniciales.index(cuadrupla) + 1]

        print()
        print("Cuadrupla siguiente: ", cuadrupla_siguiente)
        print()

        # Obtenemos la cuadrupla de comparacion que se encuentra despues de la cuadrupla de la etiqueta de inicio del while

        cuadrupla_comparacion = self.cuadruplas_iniciales[self.cuadruplas_iniciales.index(cuadrupla_siguiente) + 1]

        print()
        print("Cuadrupla comparacion: ", cuadrupla_comparacion)
        print()

        instruccion_comparacion = ""

        # Obtenemos la cuadrupla JUMP_IF_FALSE que se encuentra despues de la cuadrupla de comparacion

        cuadrupla_jump_if_false = self.cuadruplas_iniciales[self.cuadruplas_iniciales.index(cuadrupla_comparacion) + 1]

        print()
        print("Cuadrupla jump if false: ", cuadrupla_jump_if_false)
        print()

        match cuadrupla_comparacion.operador:

            case '<':
                instruccion_comparacion = "blt"
            case '>':
                instruccion_comparacion = "bgt"
            case '<=':
                instruccion_comparacion = "ble"
            case '>=':
                instruccion_comparacion = "bge"
            case '==':
                instruccion_comparacion = "beq"
            case '!=':
                instruccion_comparacion = "bne"
        
        # Ahora tenemos que ver si los operandos son variables o constantes

        operando1 = ""

        if cuadrupla_comparacion.operando1 in self.variables_cargadas:
            operando1 = self.variables_cargadas[cuadrupla_comparacion.operando1]
        else:

            # Tambien tenemos que alocar el valor en un registro temporal
            self.text_section += f"\n{'    ' * self.indentation}li $t{self.temp_counter}, {cuadrupla_comparacion.operando1}\n"
            self.variables_cargadas[cuadrupla_comparacion.operando1] = f"t{self.temp_counter}"
            self.temp_counter += 1
            operando1 = self.variables_cargadas[cuadrupla_comparacion.operando1]
        
        operando2 = ""

        if cuadrupla_comparacion.operando2 in self.variables_cargadas:
            operando2 = self.variables_cargadas[cuadrupla_comparacion.operando2]
        else:
            # Tambien tenemos que alocar el valor en un registro temporal
            self.text_section += f"\n{'    ' * self.indentation}li $t{self.temp_counter}, {cuadrupla_comparacion.operando2}\n"
            self.variables_cargadas[cuadrupla_comparacion.operando2] = f"t{self.temp_counter}"
            self.temp_counter += 1
            operando2 = self.variables_cargadas[cuadrupla_comparacion.operando2]
        
        print()
        print("Operando 1: ", cuadrupla_comparacion.operando1 + " | " + operando1 )
        print("Operando 2: ", cuadrupla_comparacion.operando2 + " | " + operando2)
        print("Comparacion: ", instruccion_comparacion)
        print()

        # Creamos la subrutina que contiene la etiqueta de inicio del while

        self.text_section += f"\n{cuadrupla_siguiente.resultado}:\n"

        # Ahora tenemos que ver a donde tenemos que saltar si la comparacion es falsa

        cuadrupla_end_while = None

        for cuadrupla in self.cuadruplas_iniciales[self.cuadruplas_iniciales.index(cuadrupla_comparacion):]:
            if cuadrupla.operador == 'EXIT_LABEL':
                cuadrupla_end_while = cuadrupla
                break
        
        print()
        print("Cuadrupla end while: ", cuadrupla_end_while)
        print()

        # El salto se hace a la etiqueta que esta en el resultado de la cuadrupla cuadrupla_end_while

        etiqueta_salto_end_while = "while_end_" + cuadrupla_end_while.resultado # while_end_L1

        self.text_section += f"\n{'    ' * self.indentation}{instruccion_comparacion} ${operando1}, ${operando2}, {etiqueta_salto_end_while}\n"

        # Ahora obtenemos el cuerpo del bucle que es encapsulando todas las cuadruplas entre JUMP_IF_FALSE + 1 y EXIT_LABEL

        lista_cuadruplas_in_between = self.cuadruplas_iniciales[self.cuadruplas_iniciales.index(cuadrupla_jump_if_false) + 1: self.cuadruplas_iniciales.index(cuadrupla_end_while)]

        print("Lista de cuadruplas in between: ")

        for cuadrupla in lista_cuadruplas_in_between:
            print(cuadrupla)
        
        print()

        # Tenemos que procesar las cuadruplas en between generando su codigo mips

        self.recorrer_cuadruplas(lista_cuadruplas_in_between)

        # Ahora solo nos queda escribir el final del while que es la etiqueta de salida

        self.text_section += f"\nwhile_end_{cuadrupla_end_while.resultado}:\n"


    def mips_ifs(self, cuadrupla):
        
        # Actualmente estamos en la cuadrupla 
        # IFS      |    ---     |    ---     |    ---

        # La cuadrupla que tenemos que procesar es la siguiente i + 1
        # Para eso obtenemos el indice de la cuadrupla actual en la lista de cuadruplas

        indice_cuadrupla_actual = self.cuadruplas_iniciales.index(cuadrupla)

        # Obtenemos la cuadrupla siguiente

        cuadrupla_siguiente = self.cuadruplas_iniciales[indice_cuadrupla_actual + 1]

        # Con esto ya tenemos la siguiente cuadrupla que contiene la comparacion
        #    <       |     4      |     6      |     t4    |

        # Tenemos que ver que tipo de comparacion es para utilizar blt, bgt, ble, bge, beq, bne 

        instruccion_comparacion = ""

        match cuadrupla_siguiente.operador:

            case '<':
                instruccion_comparacion = "blt"
            case '>':
                instruccion_comparacion = "bgt"
            case '<=':
                instruccion_comparacion = "ble"
            case '>=':
                instruccion_comparacion = "bge"
            case '==':
                instruccion_comparacion = "beq"
            case '!=':
                instruccion_comparacion = "bne"
        
        # Ahora tenemos que ver si los operandos son variables o constantes

        operando1 = ""

        if cuadrupla_siguiente.operando1 in self.variables_cargadas:
            operando1 = self.variables_cargadas[cuadrupla_siguiente.operando1]
        else:

            # Tambien tenemos que alocar el valor en un registro temporal
            self.text_section += f"\n{'    ' * self.indentation}li $t{self.temp_counter}, {cuadrupla_siguiente.operando1}\n"
            self.variables_cargadas[cuadrupla_siguiente.operando1] = f"t{self.temp_counter}"
            self.temp_counter += 1
            operando1 = self.variables_cargadas[cuadrupla_siguiente.operando1]
        
        operando2 = ""

        if cuadrupla_siguiente.operando2 in self.variables_cargadas:
            operando2 = self.variables_cargadas[cuadrupla_siguiente.operando2]
        else:
            # Tambien tenemos que alocar el valor en un registro temporal
            self.text_section += f"\n{'    ' * self.indentation}li $t{self.temp_counter}, {cuadrupla_siguiente.operando2}\n"
            self.variables_cargadas[cuadrupla_siguiente.operando2] = f"t{self.temp_counter}"
            self.temp_counter += 1
            operando2 = self.variables_cargadas[cuadrupla_siguiente.operando2]

        # Ahora tenemos que ver a donde tenemos que saltar si la comparacion es falsa

        cuadrupla_jump_if_false = self.cuadruplas_iniciales[indice_cuadrupla_actual + 2]

        # |   18   | JUMP_IF_FALSE |     t4     |    None    |     L1    |

        # El salto se hace a la etiqueta que esta en el resultado de la cuadrupla cuadrupla_jump_if_false

        etiqueta_salto = "if_part_" + cuadrupla_jump_if_false.resultado # if_part_L1

        self.text_section += f"\n{'    ' * self.indentation}{instruccion_comparacion} ${operando1}, ${operando2}, {etiqueta_salto}\n"

        # Ahora tenemos que obtener la EXIT_LABEL para saber a donde tenemos que saltar luego

        cuadrupla_exit_label = None

        # Iteramos desde la cuadrupla actual hasta el final de la lista de cuadruplas si es necesario para encontrar la cuadrupla que contiene la etiqueta de salida

        for cuadrupla in self.cuadruplas_iniciales[indice_cuadrupla_actual:]:
            if cuadrupla.operador == 'EXIT_LABEL':
                cuadrupla_exit_label = cuadrupla
                break

        # EXIT_LABEL  |    None    |    None    |     L2    |

        # Para este punto ya tenemos lo siguiente:

        # .text
        # main:
        #       # Cargar los números en los registros
        #       lw $t0, num1     # Cargar num1 en $t0
        #       lw $t1, num2     # Cargar num2 en $t1

        #       # Comparar los números
        #       bgt $t0, $t1, if_part    # Si num1 > num2, salta a if_part

        # Y ahora tenemos que escribir la parte del else:

                # Else Part: num1 <= num2
                # sub $t2, $t0, $t1  # Restar num1 - num2
                # sw $t2, result     # Guardar el resultado
                # j end              # Saltar al final

        # Para eso tenemos que ubicar todas las cuadruplas que se encuentren entre LABEL y EXIT_LABEL

        Cuadrupla_LABEL = None
        cuadrupla_EXIT_LABEL = None

        etiqueta_salto_final = "else_part_" + cuadrupla_jump_if_false.resultado

        # Recorremos todas las cuadruplas hasta el final desde la cuadrupla actual

        for cuadrupla_iteradora in self.cuadruplas_iniciales[indice_cuadrupla_actual:]:

            if cuadrupla_iteradora.operador == "LABEL":
                Cuadrupla_LABEL = cuadrupla_iteradora
                break
        
        for cuadrupla_iteradora in self.cuadruplas_iniciales[indice_cuadrupla_actual:]:

            if cuadrupla_iteradora.operador == "EXIT_LABEL":
                cuadrupla_EXIT_LABEL = cuadrupla_iteradora
                break

        print()
        print("Cuadrupla LABEL: ", Cuadrupla_LABEL)
        print("Cuadrupla EXIT_LABEL: ", cuadrupla_EXIT_LABEL)
        print()

        # Ahora obtenemos todas las cuadruplas que estan entre la cuadrupla LABEL y la cuadrupla EXIT_LABEL

        lista_cuadruplas_in_between = self.cuadruplas_iniciales[self.cuadruplas_iniciales.index(Cuadrupla_LABEL) + 1: self.cuadruplas_iniciales.index(cuadrupla_EXIT_LABEL)]

        print("Lista de cuadruplas in between si se entro al else: ")

        for cuadrupla in lista_cuadruplas_in_between:
            print(cuadrupla)
        
        print()

        # Tenemos que procesar las cuadruplas en between generando su codigo mips

        self.recorrer_cuadruplas(lista_cuadruplas_in_between)

        # Para este punto ya tenemos el siguiente fragmento escrito:

        # Else Part: num1 <= num2
        # sub $t2, $t0, $t1  # Restar num1 - num2
        # sw $t2, result     # Guardar el resultado
        # j end              # Saltar al final

        # Ahora nos toca escribir la parte del if : "if_part_" + cuadrupla_jump_if_false.resultado

        # if_part:
        #     # If Part: num1 > num2
        #     add $t2, $t0, $t1  # Sumar num1 + num2
        #     sw $t2, result     # Guardar el resultado

        self.text_section += f"\n{etiqueta_salto}:\n"

        # Tenemos que procesar todas las cuadruplas que se encuentren entre JUMP_IF_FALSE + 1 y LABEL

        lista_cuadruplas_in_between = self.cuadruplas_iniciales[self.cuadruplas_iniciales.index(cuadrupla_jump_if_false) + 1: self.cuadruplas_iniciales.index(Cuadrupla_LABEL)]

        print("Lista de cuadruplas in between si se entro al if: ")

        for cuadrupla in lista_cuadruplas_in_between:
            print(cuadrupla)
        
        print()

        # Tenemos que procesar las cuadruplas en between generando su codigo mips

        self.recorrer_cuadruplas(lista_cuadruplas_in_between)

        # Ahora solo nos queda escribir el final del if que es la etiqueta de salida

        self.text_section += f"\n{cuadrupla_EXIT_LABEL.resultado}:\n"






        # # Ahora escribimos todo lo que tendria que suceder si la comparacion es verdadera tomando desde la actual hasta la cuadrupla que contiene la etiqueta de salto
        
        # cuadrupla_salto_en_caso_de_verdadero = None

        # for cuadrupla in self.cuadruplas_iniciales[indice_cuadrupla_actual:]:
        #     if cuadrupla.operador == "JUMP":
        #         cuadrupla_salto_en_caso_de_verdadero = cuadrupla
        #         break
        
        # lista_cuadruplas_in_between = self.cuadruplas_iniciales[self.cuadruplas_iniciales.index(cuadrupla_jump_if_false) + 1: self.cuadruplas_iniciales.index(cuadrupla_salto_en_caso_de_verdadero)]

        # print("Cuadrupla salto en caso de verdadero: ", cuadrupla_salto_en_caso_de_verdadero)
        # print("Lista de cuadruplas en between si se entro al if: ")
        # for cuadrupla in lista_cuadruplas_in_between:
        #     print(cuadrupla)
        
        # # Tenemos que procesar las cuadruplas en between generando su codigo mips

        # self.recorrer_cuadruplas(lista_cuadruplas_in_between, cuadrupla_exit_label)

        # self.text_section += f"\n{'    ' * self.indentation}j SUBRUTINA_{cuadrupla_exit_label.resultado}\n"

        # # Creamos la Label de la SUBRUTINA que contiene la etiqueta de salto

        # self.text_section += f"\n{etiqueta_salto}:\n"

        # # Tenemos que procesar las cuadruplas que estan entre la etiqueta de salto y la etiqueta de salida

        # lista_cuadruplas_in_between = self.cuadruplas_iniciales[self.cuadruplas_iniciales.index(cuadrupla_salto_en_caso_de_verdadero) + 1: self.cuadruplas_iniciales.index(cuadrupla_exit_label)]

        # print("Lista de cuadruplas in between si se entro al else: ")

        # for cuadrupla in lista_cuadruplas_in_between:
        #     print(cuadrupla)

        # return cuadrupla_exit_label.resultado


        








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
    
    def mips_procedure(self, cuadrupla):
        
        if cuadrupla.operando2 in self.variables_cargadas:
            if cuadrupla.operando1 == 'out_int':
                        self.text_section += f"\n{'    ' * self.indentation}li $v0, 1\n"
                        self.text_section += f"{'    ' * self.indentation}move $a0, ${self.variables_cargadas[cuadrupla.operando2]}\n"
                        self.text_section += f"{'    ' * self.indentation}syscall\n"
                    
            # out_string
            elif cuadrupla.operando1 == 'out_string':
                self.text_section += f"\n{'    ' * self.indentation}li $v0, 4\n"
                self.text_section += f"{'    ' * self.indentation}move $a0, ${self.variables_cargadas[cuadrupla.operando2]}\n"
                self.text_section += f"{'    ' * self.indentation}syscall\n"
        else:
            if cuadrupla.operando1 == 'out_int':
                        self.text_section += f"\n{'    ' * self.indentation}li $v0, 1\n"
                        self.text_section += f"{'    ' * self.indentation}move $a0, ${cuadrupla.operando2}\n"
                        self.text_section += f"{'    ' * self.indentation}syscall\n"
                    
            # out_string
            elif cuadrupla.operando1 == 'out_string':
                self.text_section += f"\n{'    ' * self.indentation}li $v0, 4\n"
                self.text_section += f"{'    ' * self.indentation}move $a0, ${cuadrupla.operando2}\n"
                self.text_section += f"{'    ' * self.indentation}syscall\n"
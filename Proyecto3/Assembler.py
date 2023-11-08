class Cuadrupla:
    def __init__(self, operador, operando1, operando2, resultado):
        self.operador = operador
        self.operando1 = operando1
        self.operando2 = operando2
        self.resultado = resultado

class Assembler:
    def __init__(self, cuadruplas):
        self.cuadruplas = cuadruplas
        self.data_section = ".data\n"
        self.text_section = ".text\n.globl main\nmain:\n"
        self.variables_data = {}
        self.temp_reg_counter = 0
        self.variables_iniciales = ['num1', 'num2', 'resAdd', 'resSub', 'resMul', 'resDiv']

    def generar_codigo_mips(self):
        for cuad in self.cuadruplas:
            if cuad.operador == 'CLASS' or cuad.operador == 'METHOD_START':
                continue  # No se necesita en MIPS
            elif cuad.operador == '<-' and cuad.resultado in self.variables_iniciales:
                self.data_section += f"{cuad.resultado}: .word {cuad.operando1}\n"
                self.variables_data[cuad.resultado] = cuad.operando1
            elif cuad.operador in ['+', '-', '*', '/']:
                # Cargar valores iniciales
                self.text_section += f"    lw $t0, {cuad.operando1}\n"
                self.text_section += f"    lw $t1, {cuad.operando2}\n"

                # Realizar la operación
                if cuad.operador == '+':
                    self.text_section += "    add $t2, $t0, $t1\n    sw $t2, resAdd\n"
                elif cuad.operador == '-':
                    self.text_section += "    sub $t2, $t1, $t0\n    sw $t2, resSub\n"
                elif cuad.operador == '*':
                    self.text_section += "    mul $t2, $t0, $t1\n    sw $t2, resMul\n"
                elif cuad.operador == '/':
                    self.text_section += "    div $t0, $t1\n    mflo $t2\n    sw $t2, resDiv\n"

        # Finalizar el programa
        self.text_section += "    li $v0, 10    # Código de salida\n    syscall       # Ejecutar syscall para terminar\n"

        return self.data_section + self.text_section


# Lista de cuadruplas de ejemplo
cuadruplas_ejemplo = [
    Cuadrupla('CLASS', 'Main', None, None),
    Cuadrupla('<-', 3, None, 'num1'),
    Cuadrupla('<-', 9, None, 'num2'),
    Cuadrupla('<-', 0, None, 'resAdd'),
    Cuadrupla('<-', 0, None, 'resSub'),
    Cuadrupla('<-', 0, None, 'resMul'),
    Cuadrupla('<-', 0, None, 'resDiv'),
    Cuadrupla('METHOD_START', 'main', 'SELF_TYPE', None),
    Cuadrupla('+', 'num1', 'num2', 't1'),
    Cuadrupla('<-', 't1', None, 'resAdd'),
    Cuadrupla('-', 'num2', 'num1', 't2'),
    Cuadrupla('<-', 't2', None, 'resSub'),
    Cuadrupla('*', 'num1', 'num2', 't3'),
    Cuadrupla('<-', 't3', None, 'resMul'),
    Cuadrupla('/', 'num2', 'num1', 't4'),
    Cuadrupla('<-', 't4', None, 'resDiv'),
]

# Crear una instancia de la clase Assembler con las cuadruplas de ejemplo
ensamblador = Assembler(cuadruplas_ejemplo)

# Generar el código MIPS
codigo_mips = ensamblador.generar_codigo_mips()

print(codigo_mips)

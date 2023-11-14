import re
import os
import platform 
import tkinter as tk
from datetime import datetime
from tkinter import Text, ttk, Frame

import pyperclip

from Compiler import *
from Cuadrupla import *
from Ensamblador import *

keywords = {
    # Palabras clave
    "METHOD_START": ("yellow", None),
    "LABEL": ("blue", None),
    "RETURN": ("green", None),
    "CLASS": ("cyan", None),
    "PRE_PARAM": ("coral", None),
    "METHOD_CALL": ("pink", None),
    "IFS": ("steelblue", None),
    "JUMP_IF_FALSE": ("salmon", None),
    "JUMP": ("seagreen", None),
    "PARAM": ("skyblue", None),
    "WHL": ("gold", None), 
    "STACK_INIT": ("red", None),
    "EMPTY_STACK": ("red", None),

    # Operadores aritméticos
    "*": ("gray", None),
    "+": ("gray", None),
    "-": ("gray", None),
    "/": ("gray", None),

    # Otros operadores
    "<-": ("lavender", None),
    "<": ("lavender", None),
    "=": ("lavender", None)
}

# Ejemplo de código ensamblador MIPS
mips_code_example = """
.data
hello:     .asciiz "Hola mundo!\n"
    .text
main:      li $v0, 4           # syscall para print_string
    la $a0, hello        # carga la dirección de hello en $a0
    syscall             # llama al sistema operativo
    li $v0, 10          # syscall para exit
    syscall             # llama al sistema operativo
"""


def highlight_keywords(text_widget):
    for keyword, (fg, bg) in keywords.items():
        highlight_pattern(text_widget, keyword, fg, bg)

def highlight_pattern(text_widget, pattern, fg, bg=None):
    text_widget.tag_remove(pattern, '1.0', tk.END)
    start_idx = '1.0'
    while True:
        start_idx = text_widget.search(pattern, start_idx, nocase=True, stopindex=tk.END)
        if not start_idx: break
        end_idx = f"{start_idx} + {len(pattern)}c"
        text_widget.tag_add(pattern, start_idx, end_idx)
        if bg:
            text_widget.tag_config(pattern, foreground=fg, background=bg)
        else:
            text_widget.tag_config(pattern, foreground=fg)
        start_idx = end_idx

# Paso 1: Función para poblar el árbol de directorios
def populate_tree(tree, node):
    # Eliminar todos los nodos hijos existentes
    for child in tree.get_children(node):
        tree.delete(child)
    
    # Lista el contenido del directorio
    path = tree.set(node, "fullpath")
    for p in os.listdir(path):
        full_path = os.path.join(path, p)
        isdir = os.path.isdir(full_path)
        id = tree.insert(node, "end", text=p, values=[full_path])
        if isdir:
            tree.insert(id, "end")

# Paso 3: Función para cargar archivos en el editor
def load_file_into_editor(event):
    selected_item = file_tree.selection()[0]
    filepath = file_tree.item(selected_item, "values")[0]
    if os.path.isfile(filepath):
        with open(filepath, 'r') as file:
            content = file.read()
            code_area.delete(1.0, tk.END)
            code_area.insert(tk.END, content)

def extract_keywords_from_g4(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        
        # Extraer palabras reservadas
        reserved_words = re.findall(r'(\w+): \'\w+\' \| \'\w+\';', content)
        reserved_words.extend([word.lower() for word in reserved_words])
        
        # Extraer tipos de variables
        variable_types = re.findall(r'(TYPE|STRING|INT|BOOL|ID): [^;]+;', content)
        variable_types.extend([var_type.lower() for var_type in variable_types])
        variable_types.extend([var_type.lower().capitalize() for var_type in variable_types])
        
        return reserved_words, variable_types

reserved_words, variable_types = extract_keywords_from_g4('Proyecto3/YAPL.g4')
reserved_words.extend(['return'])
variable_types.extend(['Bool'])

def compile_code():
    content = code_area.get(1.0, "end-1c")
    
    # Crear el directorio 'compiled/' si no existe
    if not os.path.exists("compiled"):
        os.mkdir("compiled")
    
    # Obtener la fecha y hora actual y formatearla para el nombre del archivo
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"compiled/compiled_code.yapl"
    
    # Guardar el contenido en el archivo
    with open(file_name, 'w') as file:
        file.write(content)

    compilador = Compiler(file_name)

    compilador.lexicalAnalysis()
    compilador.syntacticAnalysis()
    compilador.semanticAnalysis()

    # Quitar el tag de todas las líneas para eliminar resaltados anteriores
    code_area.tag_remove("error", "1.0", tk.END)
    
    


    terminal_messages = [
           str(current_time) + " Errores léxicos:\n" + "\n".join(compilador.lexicalErrors) if len(compilador.lexicalErrors) > 0 else str(current_time) +" No hay errores léxicos",
           str(current_time) + " Errores sintácticos:\n" + "\n".join(compilador.error_listener.errors) if len(compilador.error_listener.errors) > 0 else str(current_time) + " No hay errores sintácticos",
    ]

    # Extraer números de línea de los mensajes de error
    error_messages = compilador.lexicalErrors + compilador.error_listener.errors 

    try:
        terminal_messages.append(
            str(current_time) + " Errores semánticos:\n" + "\n".join(compilador.semanticAnalyzer.errors) if len(compilador.semanticAnalyzer.errors) > 0 else str(current_time) + " No hay errores semánticos"
        )

        error_messages.extend(getattr(compilador.semanticAnalyzer, 'errors', []))
    except:
        pass

    error_lines = [int(re.search("Linea (\d+)", msg).group(1)) for msg in error_messages if re.search("Linea (\d+)", msg)]

    for line in error_lines:
        line_start = f"{line}.0"
        line_end = f"{line}.end"
        
        # Añadir el tag "error" a la línea completa
        code_area.tag_add("error", line_start, line_end)

    terminal_content = "\n".join(terminal_messages)
    
    terminal_area.config(state=tk.NORMAL)
    terminal_area.delete(1.0, tk.END)
    terminal_area.insert(tk.END, terminal_content)
    terminal_area.config(state=tk.DISABLED)


    if not compilador.semanticAnalyzer.errors and not compilador.lexicalErrors and not compilador.error_listener.errors:

        arbol = compilador.treeStruct

        intermedio = Intermediate(arbol, compilador.symbolTable)

        print("\n\n\n\n\n\n\n\n\n")
        print(intermedio)
        print("\n\n\n\n\n\n\n\n\n")
        print(intermedio.translate())
        print("\n\n\n\n\n\n\n\n\n")



        text_area.delete(1.0, tk.END)

        text_area.insert(tk.END, intermedio)

        highlight_keywords(text_area)

        # Actualizar la nueva área de texto con el código ensamblador MIPS
        mips_code_area.delete(1.0, tk.END)  # Borrar el contenido actual
        ensamblador = Assembler(intermedio.lista_cuadruplas)
        mips_code_area.insert(tk.END, str(ensamblador.data_section + ensamblador.text_section))  # Insertar el ejemplo MIPS

        pyperclip.copy(str(ensamblador.data_section + ensamblador.text_section))  # Copiar el código MIPS al portapapeles

    
    

def redraw():
    line_numbers_canvas.delete("all")
    i = code_area.index("@0,0")
    while True:
        dline = code_area.dlineinfo(i)
        if dline is None:
            break
        y = dline[1]
        linenum = str(i).split(".")[0]
        line_numbers_canvas.create_text(10, y+22, anchor="nw", text=linenum)
        i = code_area.index(f"{i}+1line")

    # Actualizar nuevamente después de 100 ms
    line_numbers_canvas.after(1, redraw)

def highlight_text():
    content = code_area.get(1.0, "end-1c")
    for word in reserved_words:
        start_index = "1.0"
        while start_index:
            # Buscar la palabra completa
            start_index = code_area.search(r'\m' + word + r'\M', start_index, stopindex=tk.END, regexp=True)
            if start_index:
                end_index = f"{start_index}+{len(word)}c"
                code_area.tag_add(word, start_index, end_index)
                start_index = end_index

    for vtype in variable_types:
        start_index = "1.0"
        while start_index:
            # Buscar el tipo de variable completo
            start_index = code_area.search(r'\m' + vtype + r'\M', start_index, stopindex=tk.END, regexp=True)
            if start_index:
                end_index = f"{start_index}+{len(vtype)}c"
                code_area.tag_add(vtype, start_index, end_index)
                start_index = end_index


def on_content_change(event):
    # Resaltar texto
    highlight_text()

    # Eliminar resaltado de errores
    code_area.tag_remove("error", "1.0", tk.END)
    
    # Restablecer el estado "modificado" para futuros eventos
    code_area.edit_modified(False)

# Configurar el resaltado
def configure_tags():
    for word in reserved_words:
        code_area.tag_configure(word, foreground="yellow")
    
    for vtype in variable_types:
        code_area.tag_configure(vtype, foreground="green")
    
    code_area.tag_configure("return", foreground="orange")

    code_area.tag_configure("error", background="red")



root = tk.Tk()
root.title("IDE Compiladores")
root.geometry("1400x1400")

# Frame superior que contendrá el editor y el árbol de archivos
upper_frame = tk.Frame(root)
upper_frame.pack(side="top", fill="both", expand=True)

# Frame para el editor de código y el código MIPS
editor_frame = tk.Frame(upper_frame)
editor_frame.pack(side="left", fill="both", expand=True)

# Canvas para números de línea
line_numbers_canvas = tk.Canvas(editor_frame, width=30)
line_numbers_canvas.pack(side="left", fill="y", padx=(5, 0))

# Área de código principal
code_area = Text(editor_frame, wrap="none", undo=True, spacing1=5)
code_area.pack(side="top", pady=20, padx=20, expand=True, fill="both")

# Área de código MIPS
mips_code_area = Text(editor_frame, height=30, wrap="none")
mips_code_area.pack(side="bottom", pady=(0, 20), padx=20, fill="both", expand=False)

# Obtener el directorio de trabajo actual
current_directory = os.getcwd()

# Ruta a la carpeta 'Ejemplos/' en el directorio de trabajo actual
ejemplos_path = os.path.join(current_directory, "Proyecto3")
# ejemplos_path = os.path.join(current_directory, "Proyecto1/Ejemplos")

# Frame para el árbol de archivos y el área de las cuádruplas
files_and_text_frame = Frame(upper_frame)
files_and_text_frame.pack(pady=20, padx=20, side="right", fill="both", expand=True)

# Árbol de directorios
file_tree = ttk.Treeview(files_and_text_frame, columns=("fullpath",), displaycolumns=(), height=12)
file_tree.pack(side="top", fill="both", expand=True)

root_node = file_tree.insert("", "end", text=ejemplos_path, values=(ejemplos_path,))
populate_tree(file_tree, root_node)

# Agregar un "+" para indicar que se puede expandir
file_tree.insert(root_node, "end")

# Configurar el evento para expandir el directorio
file_tree.bind("<<TreeviewOpen>>", lambda event: populate_tree(file_tree, file_tree.focus()))

# Configurar el evento para cargar archivos al hacer doble clic
file_tree.bind("<Double-1>", load_file_into_editor)

# Área de texto para las cuádruplas
text_area = Text(files_and_text_frame, height=12, wrap="none")
text_area.pack(side="top", fill="both", expand=True)

# Área de la "terminal"
terminal_area = Text(root, height=6, wrap="none", state=tk.DISABLED)
terminal_area.pack(pady=(0, 20), padx=20, fill="x")

# Botón para compilar
if platform.system() == "Windows":
    compile_button = tk.Button(root, text="▶ Compilar", bg="green", fg="white", command=compile_code)
else:
    # Estilo para el botón en otros sistemas operativos
    style = ttk.Style()
    style.configure('TButton', foreground='white')
    compile_button = ttk.Button(root, text="▶ Compilar", style='TButton', command=compile_code)

compile_button.pack(pady=20)

# Configuración de eventos y estilos
code_area.bind("<<Modified>>", on_content_change)
configure_tags()
redraw()

root.mainloop()


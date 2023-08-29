from datetime import datetime
from tkinter import Text, ttk
import tkinter as tk
import platform 
import re
import os

from Compiler import *

# Paso 1: Función para poblar el árbol de directorios
def populate_tree(tree, node):
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

reserved_words, variable_types = extract_keywords_from_g4('Proyecto1/YAPL.g4')

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


    terminal_messages = [
            "Errores léxicos:\n" + "\n".join(compilador.lexicalErrors) if len(compilador.lexicalErrors) > 0 else "No hay errores léxicos",
            "Errores sintácticos:\n" + "\n".join(compilador.error_listener.errors) if len(compilador.error_listener.errors) > 0 else "No hay errores sintácticos",
    ]

    try:
        terminal_messages.append(
            "Errores semánticos:\n" + "\n".join(compilador.semanticAnalyzer.errors) if len(compilador.semanticAnalyzer.errors) > 0 else "No hay errores semánticos"
        )
    except:
        pass

    terminal_content = "\n".join(terminal_messages)
    
    terminal_area.config(state=tk.NORMAL)
    terminal_area.delete(1.0, tk.END)
    terminal_area.insert(tk.END, terminal_content)
    terminal_area.config(state=tk.DISABLED)
    

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
    
    # Restablecer el estado "modificado" para futuros eventos
    code_area.edit_modified(False)

# Configurar el resaltado
def configure_tags():
    for word in reserved_words:
        code_area.tag_configure(word, foreground="yellow")
    
    for vtype in variable_types:
        code_area.tag_configure(vtype, foreground="green")





root = tk.Tk()
root.title("IDE Compiladores")
root.geometry("1200x1000")

# Hacer la ventana no redimensionable
root.resizable(False, False)

# Frame superior que contendrá el editor y el árbol de archivos
upper_frame = tk.Frame(root)
upper_frame.pack(side="top", fill="both", expand=True)

# Frame para el editor de código
editor_frame = tk.Frame(upper_frame)
editor_frame.pack(side="left", fill="both", expand=True)

# Canvas para números de línea
line_numbers_canvas = tk.Canvas(editor_frame, width=30)
line_numbers_canvas.pack(side="left", fill="y", padx=(5, 0))

# Área de código con espacio entre líneas
code_area = Text(editor_frame, wrap="none", undo=True, spacing1=5)
code_area.pack(pady=20, padx=20, expand=True, fill="both")





# Obtener el directorio de trabajo actual
current_directory = os.getcwd()

# Ruta a la carpeta 'Ejemplos/' en el directorio de trabajo actual
ejemplos_path = os.path.join(current_directory, "Proyecto1/Ejemplos")

# Verificar si el directorio 'Ejemplos/' existe
if not os.path.exists(ejemplos_path):
    print(f"El directorio 'Proyecto1/Ejemplos/' no existe en {current_directory}. Asegúrate de que la carpeta esté presente.")
else:
    # Crear el Treeview para los archivos
    file_tree = ttk.Treeview(upper_frame, columns=("fullpath",), displaycolumns=(), height=25)
    file_tree.pack(side="right", fill="both")

    # Agregar el directorio base al Treeview
    root_node = file_tree.insert("", "end", text="Ejemplos", values=(ejemplos_path,))
    populate_tree(file_tree, root_node)

# Agregar un "+" para indicar que se puede expandir
file_tree.insert(root_node, "end")

# Configurar el evento para expandir el directorio
file_tree.bind("<<TreeviewOpen>>", lambda event: populate_tree(file_tree, file_tree.focus()))

# Configurar el evento para cargar archivos al hacer doble clic
file_tree.bind("<Double-1>", load_file_into_editor)






# Área de la "terminal"
terminal_area = Text(root, height=6, wrap="none", state=tk.DISABLED)
terminal_area.pack(pady=(0, 20), padx=20, fill="x")

# Detectar el sistema operativo
os_name = platform.system()

# Si es Windows, usar un botón verde. Si es macOS, usar el estilo predeterminado.
if os_name == "Windows":
    compile_button = tk.Button(root, text="▶ Compilar", bg="green", fg="white", command=compile_code)
else:
    # Estilo para el botón
    style = ttk.Style()
    style.configure('TButton', foreground='white')
    compile_button = ttk.Button(root, text="▶ Compilar", style='TButton', command=compile_code)

compile_button.pack(pady=20)

# Configurar el evento para el área de texto
code_area.bind("<<Modified>>", on_content_change)

# Configurar estilos de resaltado
configure_tags()

# Llamada inicial para mostrar números de línea
redraw()

root.mainloop()

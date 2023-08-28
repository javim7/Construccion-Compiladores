import tkinter as tk
from tkinter import Text, ttk
import platform 
import re

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

print(reserved_words)
print(variable_types)

def compile_code():
    content = code_area.get(1.0, "end-1c")
    print(content)

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
root.geometry("800x600")

# Hacer la ventana no redimensionable
root.resizable(False, False)

# Canvas para números de línea
line_numbers_canvas = tk.Canvas(root, width=30)
line_numbers_canvas.pack(side="left", fill="y", padx=(5, 0))

# Área de código con espacio entre líneas
code_area = Text(root, wrap="none", undo=True, spacing1=5)
code_area.pack(pady=20, padx=20, expand=True, fill="both")

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

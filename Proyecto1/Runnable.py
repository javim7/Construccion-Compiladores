import tkinter as tk
from tkinter import Text, Scrollbar

def compile_code():
    content = code_area.get(1.0, "end-1c")
    print(content)

def redraw():
    line_numbers_canvas.delete("all")
    i = code_area.index("@0,0")
    while True:
        dline = code_area.dlineinfo(i)
        if dline is None:  # Salir del loop si ya no hay más líneas.
            break
        y = dline[1]
        linenum = str(i).split(".")[0]
        line_numbers_canvas.create_text(10, y+22, anchor="nw", text=linenum)
        i = code_area.index(f"{i}+1line")

    # Actualizar nuevamente después de 100 ms
    line_numbers_canvas.after(1, redraw)

root = tk.Tk()
root.title("IDE")
root.geometry("800x800")

# Scrollbar
scrollbar = Scrollbar(root)
scrollbar.pack(side="right", fill="y")

# Canvas para números de línea
line_numbers_canvas = tk.Canvas(root, width=30)
line_numbers_canvas.pack(side="left", fill="y", padx=(5, 0))

# Área de código con espacio entre líneas
code_area = Text(root, wrap="none", undo=True, yscrollcommand=scrollbar.set, spacing1=5)
code_area.pack(pady=20, padx=20, expand=True, fill="both")

# Conectar scrollbar
# scrollbar.config(command=code_area.yview)

# Botón de compilar
compile_button = tk.Button(root, text="Compilar", command=compile_code)
compile_button.pack(pady=20)

# Llamada inicial para mostrar números de línea
redraw()

root.resizable(False, False)
root.mainloop()

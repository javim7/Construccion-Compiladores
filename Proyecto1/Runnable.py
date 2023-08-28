import tkinter as tk

def compilar(editor):
    codigo = editor.get("1.0", tk.END)
    print(codigo)

def configurar_ventana(ventana):
    ventana.title("Mini IDE con Tkinter")
    ventana.geometry("700x500")

def crear_editor(ventana):
    frame = tk.Frame(ventana)
    frame.pack(pady=20, fill=tk.BOTH, expand=True)
    
    # Barra de desplazamiento
    scrollbar = tk.Scrollbar(frame, orient="vertical")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Área de números de línea
    line_num_area = tk.Text(frame, width=4, padx=5, takefocus=0, border=0, background='lightgray', state=tk.DISABLED, yscrollcommand=scrollbar.set)
    line_num_area.pack(side=tk.LEFT, fill=tk.Y)

    # Editor de texto
    editor = tk.Text(frame, wrap=tk.NONE, yscrollcommand=scrollbar.set)
    editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Función para sincronizar el desplazamiento
    def both_scroll(*args):
        line_num_area.yview(*args)
        editor.yview(*args)

    scrollbar.config(command=both_scroll)
    
    # Función para actualizar los números de línea
    def update_line_numbers(event=None):
        lines = editor.get("1.0", "end-1c").split("\n")
        line_count = len(lines)
        
        line_num_area.config(state=tk.NORMAL)
        line_num_area.delete('1.0', tk.END)
        
        for i in range(1, line_count + 1):
            line_num_area.insert(tk.END, str(i) + '\n')
        
        line_num_area.config(state=tk.DISABLED)

    # Actualizar los números de línea cuando el texto cambie
    editor.bind('<KeyPress>', update_line_numbers)
    editor.bind('<KeyRelease>', update_line_numbers)
    
    return editor

def crear_boton(ventana, editor):
    boton = tk.Button(ventana, text="Compilar", command=lambda: compilar(editor))
    boton.pack()

def main():
    ventana = tk.Tk()
    
    configurar_ventana(ventana)
    
    editor = crear_editor(ventana)
    crear_boton(ventana, editor)
    
    ventana.mainloop()

if __name__ == "__main__":
    main()

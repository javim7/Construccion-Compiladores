# Construccion de Compiladores 2

# Instrucciones para correr
Instalar la libreria ANTLR:
```bash
pip install antlr4-tools
pip install antlr4-python3-runtime
```

Compilar las reglas lexicas y sintacticas:
```bash
antlr4 -Dlanguage=Python3 YAPL.g4
```
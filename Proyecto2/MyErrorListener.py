from YAPLListener import YAPLListener
from antlr4.error.ErrorListener import ErrorListener

class MyErrorListener(ErrorListener):
    def __init__(self):
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if "extraneous input" not in msg:
            error_message = f"ERROR SINTACTICO: El problema es: {msg} : Linea {line}"
            self.errors.append(error_message)
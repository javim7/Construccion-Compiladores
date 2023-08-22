import os
from antlr4 import *
from Drawer import *
from MyErrorListener import *
from ParseTree import *
from YAPLLexer import YAPLLexer
from YAPLParser import YAPLParser
from antlr4.tree.Tree import TerminalNodeImpl

class Compiler():
    def __init__(self, input_file):
        self.input = input_file
        self.input_stream = FileStream(self.input)
        self.lexer = YAPLLexer(self.input_stream)
        self.token_stream = CommonTokenStream(self.lexer)
        self.parser = YAPLParser(self.token_stream)
        self.error_listener = MyErrorListener()
        self.parser.removeErrorListeners()
        self.parser.addErrorListener(self.error_listener)
        self.tree = self.parser.program()
        self.treeStruct = None
        self.lexicalErrors = []

    def lexicalAnalysis(self):
        nonErrors, lexicalErrors = self.get_tokens()

        if lexicalErrors:
            print("\nTOKENS IDENTIFICADOS:")
            for token in nonErrors:
                print(token)
            print("\nERRORES LEXICOS IDENTIFICADOS:")
            for error in lexicalErrors:
                print(error)
            # print()
        else:
            print("\nTOKENS IDENTIFICADOS:")
            for token in nonErrors:
                print(token)
            print()

    def syntacticAnalysis(self):
        if self.error_listener.errors:
            print("\nERRORES SINTACTICOS IDENTIFICADOS:")
            for error in self.error_listener.errors:
                print(error)
        else:
            print("\nARBOL SINTACTICO GENERADO:")
            tree = self.getTreeString()
            root = self.build_tree(self.tree)
            self.treeStruct = ParseTree()
            self.traverse_tree(root, self.treeStruct)
            # for node in self.treeStruct.nodes:
            #     print(node)
            self.treeStruct.root = self.treeStruct.nodes[0]
            # print(self.treeStruct)

            drawTree = Drawer(self.treeStruct)
            drawTree.draw(self.treeStruct.root)
            drawTree.save("parse_tree")
    
    def syntacticAnalysis2(self):
        if self.error_listener.errors:
            print("\nERRORES SINTACTICOS IDENTIFICADOS:")
            for error in self.error_listener.errors:
                print(error)
        else:
            print("\nARBOL SINTACTICO GENERADO:")
            command = f"antlr4-parse Lab0/YAPL.g4 program  -gui {self.input}"
            os.system(command)

    def getTreeString(self):
        tree_str = self.tree.toStringTree(recog=self.parser)
        # print(tree_str)
        return tree_str

    def build_tree(self, node):
        if node is not None:
            # Get the rule name for rule context objects
            if isinstance(node, RuleContext):
                rule_index = node.getRuleIndex()
                rule_name = self.parser.ruleNames[rule_index]
                tree_node = ParseTreeNode(rule_name)
            else:
                tree_node = ParseTreeNode(str(node))
            
            # Set the errorNode attribute to True if the node represents an error
            if isinstance(node, ErrorNode):
                tree_node.errorNode = True
            
            # Recursively build the tree for each child node
            if not isinstance(node, TerminalNodeImpl):
                for child in node.children:
                    child_tree_node = self.build_tree(child)
                    tree_node.add_child(child_tree_node)
            
            return tree_node

    def traverse_tree(self, node, tree):
        if node is not None:
            tree.add_node(node)
            for child in node.children:
                self.traverse_tree(child, tree)

    def get_tokens(self):
        self.token_stream.fill()
        all_tokens = self.token_stream.tokens
        good_tokens = []

        token_type_names = {
            1: "';'",
            2: "'{'",
            3: "'}'",
            4: "'('",
            5: "','",
            6: "')'",
            7: "':'",
            8: "'@'",
            9: "'.'",
            10: "'~'",
            11: "'*'",
            12: "'/'",
            13: "'+'",
            14: "'-'",
            15: "'<='",
            16: "'<'",
            17: "'='",
            18: "WHITESPACE",
            19: "BLOCK_COMMENT",
            20: "LINE_COMMENT",
            21: "CLASS",
            22: "ELSE",
            23: "FALSE",
            24: "FI",
            25: "IF",
            26: "IN",
            27: "INHERITS",
            28: "ISVOID",
            29: "LET",
            30: "LOOP",
            31: "POOL",
            32: "THEN",
            33: "WHILE",
            34: "CASE",
            35: "ESAC",
            36: "NEW",
            37: "OF",
            38: "NOT",
            39: "TRUE",
            40: "STRING",
            41: "INT",
            42: "TYPE",
            43: "ID",
            44: "'<-'",
            45: "'=>'",
            46: "ERROR"
        }

        line = column = 1 
        last_line = 1

        # Calculate the maximum lengths of token name, lexeme, line, and column
        max_name_length = max(len(name) for name in token_type_names.values())
        max_lexeme_length = max(len(token.text) for token in all_tokens)
        max_line_length = len(str(self.lexer.line))
        max_column_length = len(str(self.lexer.column))

        # Iterate through all tokens
        for token in all_tokens:
            # Skip the EOF token
            if token.type == Token.EOF:
                continue

            token_type = token.type
            token_name = token_type_names.get(token_type, f"Unknown token ({token_type})")
            lexeme = token.text

            # Calculate line and column information
            if last_line != token.line:
                line += 1
                column = 1
                last_line = token.line
            else:
                column += len(lexeme)

            if token_name == "ERROR":
                self.lexicalErrors.append(f"{token_name} LEXICO: Caracter '{lexeme}' no identificado en linea {line}, columna {column}")
            else:
                good_tokens.append(f"Token: {token_name:{max_name_length}} | "
                  f"Lexema: {lexeme:{max_lexeme_length}} | "
                  f"Linea: {line:>{max_line_length}} | "
                  f"Columna: {column:>{max_column_length}}")

        return good_tokens, self.lexicalErrors
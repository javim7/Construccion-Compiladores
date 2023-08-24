class ParseTreeNode():
    def __init__(self, val):
        self.val = val
        self.errorNode = False
        self.children = []
        self.parent = None
    
    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        s = f"TreeNode: {self.val}"
        s += f"\n\tErrorNode: {self.errorNode}"
        if len(self.children) > 0:
            s += f"\n\tChildren: {[child.val for child in self.children]}"
        if self.parent:
            s += f"\n\tParent: {self.parent.val}"
        return s
    
class ParseTree():
    def __init__(self):
        self.root = None
        self.nodes = []
    
    def add_node(self, node):
        self.nodes.append(node)

    def __str__(self):
        s = f"ParseTree: {self.root.val}"
        if len(self.nodes) > 0:
            s += f"\n\tNodes: {[node.val for node in self.nodes]}"
        return s
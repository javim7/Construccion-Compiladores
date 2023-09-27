from graphviz import Digraph

class Drawer:
    def __init__(self, parse_tree):
        self.parse_tree = parse_tree
        self.graph = Digraph(comment='Parse Tree', format='png')
        self.node_counter = 0

    def draw(self, node, parent=None):
        node_name = f"node{self.node_counter}"
        self.node_counter += 1

        # Customize node attributes based on the presence of isErrorNode
        node_attributes = {}
        if node.errorNode:
            node_attributes['color'] = 'red'

        # Add the node to the graph
        self.graph.node(node_name, label=node.val, **node_attributes)

        if parent is not None:
            self.graph.edge(parent, node_name)

        for child in node.children:
            self.draw(child, node_name)

    def save(self, filename):
        self.graph.render("Proyecto1/Tree/" + filename, view=False)

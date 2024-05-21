from graphviz import Digraph


class DotRenderer:
    def __init__(self):
        self.dot = Digraph('AST')
        self.seq = 0

    def name(self):
        self.seq += 1
        return f'n{self.seq:02d}'

    def visit(self, node):
        node_type = type(node).__name__
        method_name = f'visit_{node_type}'
        visit_method = getattr(self, method_name, self.generic_visit)
        return visit_method(node)

    def generic_visit(self, node):
        name = self.name()
        self.dot.node(name, label=type(node).__name__)
        return name

    def visit_Program(self, node):
        name = self.name()
        self.dot.node(name, label='Program')
        for cmd in node.cmds:
            self.dot.edge(name, self.visit(cmd))
        return name

    def visit_Command(self, node):
        name = self.name()
        self.dot.node(name, label=f'Command\n{node.lineno}')
        self.dot.edge(name, self.visit(node.command), label='cmd')
        return name

    def visit_Remark(self, node):
        name = self.name()
        self.dot.node(name, label=f'REM\n{node.text}')
        return name

    def visit_ForStmt(self, node):
        name = self.name()
        self.dot.node(name, label='ForStmt')
        self.dot.edge(name, self.visit(node.ident), label='ident')
        self.dot.edge(name, self.visit(node.low), label='low')
        self.dot.edge(name, self.visit(node.top), label='top')
        if node.step:
            self.dot.edge(name, self.visit(node.step), label='step')
        return name

    def visit_Let(self, node):
        name = self.name()
        self.dot.node(name, label='Let')
        self.dot.edge(name, self.visit(node.var), label='var')
        self.dot.edge(name, self.visit(node.expr), label='expr')
        return name

    def visit_Next(self, node):
        name = self.name()
        self.dot.node(name, label='Next')
        self.dot.edge(name, self.visit(node.ident))
        return name

    def visit_End(self, node):
        name = self.name()
        self.dot.node(name, label='END')
        return name

    def visit_Variable(self, node):
        name = self.name()
        self.dot.node(name, label=f'Variable\nname: {node.name}')
        return name
    
    def accept(self, visitor):
        return visitor.visit_Program(self)
    
    def visit_InputStmt(self, node):
        pass

import ast 
import networkx as nx
from pathlib import Path
from util import notebook_to_script


class VariableDependencyAnalyzer(ast.NodeVisitor):
    
    def __init__(self):
        self.current_variable = None
        self.dependency_graph = nx.DiGraph()

    def visit_Assign(self, assign_node):
        if len(assign_node.targets) == 1 and isinstance(assign_node.targets[0], ast.Name):
            self.current_variable = assign_node.targets[0].id
            self.dependency_graph.add_node(self.current_variable)
            self.visit(assign_node.value)
            self.current_variable = None

    def visit_Name(self, name_node):
        if self.current_variable and isinstance(name_node.ctx, ast.Load):
           self.dependency_graph.add_edge(name_node.id, self.current_variable)


def analyze_variable_dependencies(code: str) -> VariableDependencyAnalyzer:
    
    node = ast.parse(code)

    analyzer = VariableDependencyAnalyzer()
    analyzer.visit(node)

    return analyzer


def find_wcc(graph: nx.DiGraph) -> tuple[list[list[str], int]]:
    wcc = list(nx.weakly_connected_components(graph))
    lens = [len(c) for c in wcc]
    if len(lens) == 0:
        return [], 0
    else: 
        return wcc, sum(lens) / len(lens)


def count_wcc(code: str) -> tuple[list[list[str]], int]:
    """Analyses the notebook and returns the list of weakly connected components, plus the average size of the weakly connected components."""
    
    analyzer = analyze_variable_dependencies(code)
    wcc, size = find_wcc(analyzer.dependency_graph)
    return wcc, size


if __name__ == "__main__":
    notebook = Path("sample/0a7ef9adf5ac046721fd011e83acd6a2ef5d10/LSTM-Text-Generation/RNN-keras-Text.ipynb")
    code = notebook_to_script(notebook)
    count, avg = count_wcc(code) 

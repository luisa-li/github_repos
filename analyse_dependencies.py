import ast 
import networkx as nx
from pathlib import Path
import nbformat
from nbconvert import PythonExporter


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


def is_valid_code(code: str) -> bool:
    try:
        compile(code, "<string>", "exec")
        return True
    except SyntaxError:
        return False

import nbformat
from nbconvert import PythonExporter
from pathlib import Path
import ast

def is_valid_code(code: str) -> bool:
    try:
        compile(code, "<string>", "exec")
        return True
    except SyntaxError:
        return False

def notebook_to_script(notebook_path: Path, script_dir: Path) -> Path:

    with open(notebook_path, 'r', encoding='utf-8') as nb_file:
        notebook_content = nbformat.read(nb_file, as_version=4)
    
    exporter = PythonExporter()
    script, _ = exporter.from_notebook_node(notebook_content)
    
    script_lines = script.split('\n')
    
    valid_code_lines = []
    current_cell = []
    
    for line in script_lines:
        if line.startswith("# In["):
            if current_cell:  
                if is_valid_code("\n".join(current_cell)):
                    valid_code_lines.extend(current_cell) 
            current_cell = [line] 
        else:
            current_cell.append(line)
    
    if current_cell and is_valid_code("\n".join(current_cell)):
        valid_code_lines.extend(current_cell)
    
    valid_script = "\n".join(valid_code_lines)
    
    file_name = notebook_path.stem
    path = script_dir / (file_name + ".py")
    
    with open(path, 'w', encoding='utf-8') as script_file:
        script_file.write(valid_script)
    
    return path


def analyze_variable_dependencies(file_path: Path) -> VariableDependencyAnalyzer:
    
    with open(file_path, 'r') as file:
        node = ast.parse(file.read())

    analyzer = VariableDependencyAnalyzer()
    analyzer.visit(node)

    return analyzer


def avg_wcc_size(graph: nx.DiGraph) -> tuple[list[list[str], int]]:
    wcc = list(nx.weakly_connected_components(graph))
    lens = [len(c) for c in wcc]
    if len(lens) == 0:
        return 0
    else: 
        return wcc, sum(lens) / len(lens)


def analyse_notebook(notebook_path: Path, scripts_dir: Path) -> tuple[list[list[str]], int]:
    """Analyses the notebook and returns the list of weakly connected components, plus the average size of the weakly connected components."""
    script_path = notebook_to_script(notebook_path, scripts_dir)
    analyzer = analyze_variable_dependencies(script_path)
    wcc, size = avg_wcc_size(analyzer.dependency_graph)
    return wcc, size


if __name__ == "__main__":
    notebook = Path("sample/0a7ef9adf5ac046721fd011e83acd6a2ef5d10/LSTM-Text-Generation/RNN-keras-Text.ipynb")
    path = notebook_to_script(notebook, Path("."))
    analyzer = analyze_variable_dependencies(path)
    size = avg_wcc_size(analyzer.dependency_graph)

from nbconvert import PythonExporter
from pathlib import Path
import nbformat


def notebook_to_script(notebook_path: Path) -> str:

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
    
    return valid_script


def is_valid_code(code: str) -> bool:
    try:
        compile(code, "<string>", "exec")
        return True
    except SyntaxError:
        return False
"""Analyse all the notebooks in the three downloaded repositories and compile results"""

import os
import json 
from pathlib import Path
from analyse_dependencies import analyse_notebook

def get_all_notebooks(dir: Path) -> list[Path]:
    notebooks = []
    for root, _, files in os.walk(dir):
        for file in files:
            if file.endswith('.ipynb'):
                notebooks.append(Path(os.path.join(root, file))) 
    return notebooks


def convert_set(obj):
    if isinstance(obj, set): 
        return list(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


if __name__ == "__main__":
    
    results = {}
    failures = []
    
    dir = Path("sample")
    script_dir = Path("scripts")
    notebooks = get_all_notebooks(dir)
    for notebook in notebooks:
        try:
            wcc, size = analyse_notebook(notebook, script_dir)
            results[notebook.name] = {"wccs": wcc, "avg_wcc_size": size}
        except Exception as e:
            failures.append((notebook, e))
    
    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4, default=convert_set)
    
    with open('failures.txt', 'w', encoding='utf-8') as file:
        for failure in failures: 
            file.write(str(failure) + '\n')
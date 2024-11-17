"""Analyse all the notebooks in the given repository with average wcc size, verb count and code text ratio and compile the results"""

import csv
from util import get_all_notebooks, notebook_to_script
from count_code_text import count_code_text
from count_verbs import count_verbs
from count_wcc import count_wcc


def convert_set(obj):
    if isinstance(obj, set): 
        return list(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


def analyse_all(hexdir):
    
    # writing some column names 
    with open('dataset.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["full_path", "file_name", "lines_of_code", "lines_of_text", "verb_count", "wccs", "avg_wcc_size"])
    with open('failures.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["full_path", "error"])
        
    
    notebooks = get_all_notebooks(hexdir)
    for path in notebooks:
        try:
            raw_text = notebook_to_script(path)
            code, text = count_code_text(path)
            verbs = count_verbs(raw_text)
            wcc, avg_wcc_size = count_wcc(raw_text)
            with open('dataset.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([path, path.name, code, text, verbs, wcc, avg_wcc_size])
        except Exception as e:
            with open('failures.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([path, e])
        

if __name__ == "__main__":
    
    dir = 'sample'
    analyse_all(dir)
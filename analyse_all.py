"""Analyse all the notebooks in the given repository with average wcc size, verb count and code text ratio and compile the results"""

import csv
import argparse
from tqdm import tqdm
from util import get_all_notebooks, notebook_to_script
from count_code_text import count_code_text
from count_verbs import count_verbs
from count_wcc import count_wcc


def convert_set(obj):
    if isinstance(obj, set): 
        return list(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


def analyse_all(dir, output):
    """Computes all the metrics for all the notebooks in the given directory, saves outputs."""
    
    dataset_path = f"{output}/dataset.csv"
    failures_path = f"{output}/failures.csv"
    
    # writing some column names 
    with open(dataset_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["full_path", "file_name", "lines_of_code", "lines_of_text", "verb_count", "wccs", "avg_wcc_size"])
    with open(failures_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["full_path", "error"])
        
    notebooks = get_all_notebooks(dir)
    for path in tqdm(notebooks):
        try:
            raw_text = notebook_to_script(path)
            code, text = count_code_text(path)
            verbs = count_verbs(raw_text)
            wcc, avg_wcc_size = count_wcc(raw_text)
            with open(dataset_path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([path, path.name, code, text, verbs, wcc, avg_wcc_size])
        except Exception as e:
            with open(failures_path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([path, e])
        
def main():
    
    parser = argparse.ArgumentParser(description="Script to run through all notebook files in a given directory, and calculate a score for each")
    parser.add_argument("directory", type=str, help="Path to the directory holding the notebooks")
    parser.add_argument("output", type=str, help="Path to the directory to output results to.")
    
    args = parser.parse_args()
    analyse_all(args.directory, args.output)

if __name__ == "__main__":

    main() 
import os
import shutil
from pathlib import Path
import pandas as pd

def move_files(csv_path, target_dir, column):
    df = pd.read_csv(csv_path)
    os.makedirs(target_dir, exists_ok=True)
    
    for file in df[column]:
        target = os.path.join(target_dir, Path(file).stem)
        shutil.move(file, target)

if __name__ == "__main__":
    
    verb_samples = pd.read_csv('samples/verb_samples')
    ct_ratio_samples = pd.read_csv('samples/ct_ratio_samples.csv')
    wcc_size_samples = pd.read_csv('samples/wcc_size_samples.csv')
    move_files(verb_samples, "samples/verb/", "full_path")
    move_files(ct_ratio_samples, "samples/ct_ratio/", "full_path") 
    move_files(wcc_size_samples, "samples/wcc_size/", "full_path")

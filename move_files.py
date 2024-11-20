import os
import shutil
from pathlib import Path
import pandas as pd

def move_files(csv_path, target_dir, column):
    df = pd.read_csv(csv_path)
    os.makedirs(target_dir, exists_ok=True)
    
    for file in df[column]:
        breakpoint()
        target = os.path.join(target_dir, Path(file).name)
        shutil.copy(file, target)

if __name__ == "__main__":
    
    move_files('samples/verb_samples.csv', "samples/verb/", "full_path")
    move_files('samples/ct_ratio_samples.csv', "samples/ct_ratio/", "full_path") 
    move_files('samples/wcc_size_samples.csv', "samples/wcc_size/", "full_path")


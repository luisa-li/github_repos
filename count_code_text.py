import json

def count_code_text(file_path):
    
    with open(file_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    code_count = 0
    text_count = 0
    
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            code_count += sum(len(line) for line in cell.get('source', []))
        elif cell['cell_type'] == 'markdown':
            text_count += sum(len(line) for line in cell.get('source', []))
    
    return code_count, text_count
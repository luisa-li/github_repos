import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize

from util import notebook_to_script
from pathlib import Path


nltk.download("punkt")
nltk.download('punkt_tab')
nltk.download("averaged_perceptron_tagger_eng")


def count_verbs(text):

    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    verb_count = sum(1 for _, tag in pos_tags if tag.startswith("VB"))
    
    return verb_count
    

if __name__ == "__main__":
    notebook = Path("sample/0a7ef9adf5ac046721fd011e83acd6a2ef5d10/LSTM-Text-Generation/RNN-keras-Text.ipynb")
    code = notebook_to_script(notebook)
    count = count_verbs(code)    
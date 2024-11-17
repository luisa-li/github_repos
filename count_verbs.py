import spacy

def count_verbs(model, text):

    doc = model(text)
    verb_count = sum(1 for token in doc if token.pos_ == "VERB")
    return verb_count
    

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
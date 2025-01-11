import spacy

nlp = spacy.load("en_core_web_sm")

def extract_key_concepts(text):
    doc = nlp(text)
    return [chunk.text for chunk in doc.noun_chunks]

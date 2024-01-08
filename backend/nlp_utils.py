import spacy

# Load the SpaCy language model
nlp = spacy.load("en_core_web_sm")

def extract_entities(sentence):
    """
    Extract named entities from a sentence.
    """
    doc = nlp(sentence)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def parse_dependencies(sentence):
    """
    Perform dependency parsing on a sentence.
    """
    doc = nlp(sentence)
    parsed = [(token.text, token.dep_, token.head.text) for token in doc]
    return parsed

# Example usage of the functions
if __name__ == "__main__":
    # Process user input using SpaCy for named entity recognition (NER)
    user_input = "Tell me about autism symptoms in children"
    named_entities = extract_entities(user_input)
    print("Named Entities:", named_entities)

    # Perform dependency parsing on a sentence
    sentence = "Autism is a neurodevelopmental disorder."
    dependency_info = parse_dependencies(sentence)
    print("Dependency Parsing:", dependency_info)

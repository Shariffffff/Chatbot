import openai
import os
import numpy as np
import json
import torch
from nltk_utils import bag_of_words, tokenize
from model import NeuralNet
import spacy
from documents import docsearch, chain
from spellchecker import SpellChecker
from document_processor import search_documents_for_answer

# Load the SpaCy language model
nlp = spacy.load("en_core_web_sm")

# Set the OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("The OpenAI API key has not been set as an environment variable.")

# Load saved model data
data = torch.load('data.pth')
model = NeuralNet(data['input_size'], data['hidden_size'], data['output_size'])
model.load_state_dict(data['model_state'])
model.eval()
all_words = data['all_words']
tags = data['tags']

# Load intents file
with open('intents.json', 'r') as f:
    intents = json.load(f)

conversation_history = []

def extract_entities(sentence):
    doc = nlp(sentence)
    return [(ent.text, ent.label_) for ent in doc.ents]

def analyze_sentence(sentence):
    doc = nlp(sentence)
    return [(token.text, token.pos_) for token in doc]

def update_conversation(user_input, bot_response):
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": bot_response})

def correct_spelling(sentence):
    spell = SpellChecker()
    corrected_words = []
    for word in sentence.split():
        corrected_word = spell.correction(word)
        if corrected_word is not None:
            corrected_words.append(corrected_word)
        else:
            corrected_words.append(word)  # Use the original word if correction is None
    return ' '.join(corrected_words)

def get_neural_response(sentence):
    sentence_tokens = tokenize(sentence)
    X = bag_of_words(sentence_tokens, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    confidence_threshold = 0.75
    if prob.item() > confidence_threshold:
        for intent in intents['intents']:
            if tag == intent['tag']:
                return np.random.choice(intent['responses'])

    return None


def get_gpt3_response(user_input, conversation_history):
    # Focused prompt with clearer context
    prompt = "The following is a conversation providing support and information strictly about autism.\n"

    # Add only the last few relevant exchanges from the conversation history
    history = conversation_history[-5:]
    for exchange in history:
        prompt += f"{exchange['role'].capitalize()}: {exchange['content']}\n"

    prompt += f"User: {user_input}\nAssistant:"

    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=50,
            temperature=0.7,  # Adjust temperature as needed
            stop=["\nUser:", "\nAssistant:"]  # Stop tokens to control the response flow
        )
        generated_response = response.choices[0].text.strip()

        # Additional check to filter irrelevant responses
        if len(generated_response.split()) < 5 or "autism" not in generated_response.lower():
            return "I'm sorry, I don't have enough information to answer that question."

        return generated_response
    except Exception as e:
        print("Error generating response from OpenAI:", e)
        return "I'm sorry, I'm having trouble accessing my resources at the moment."


def get_chatbot_response(user_input):
    corrected_input = correct_spelling(user_input)

    # Check documents first
    document_response = search_documents_for_answer(corrected_input)
    if document_response:
        update_conversation(user_input, document_response)
        return document_response

    # Check intents next
    neural_response = get_neural_response(corrected_input)
    if neural_response:
        update_conversation(user_input, neural_response)
        return neural_response

    # Finally, use OpenAI's GPT-3 for queries outside the scope of predefined intents and documents
    gpt3_response = get_gpt3_response(corrected_input, conversation_history)
    if gpt3_response and gpt3_response.strip() != "":
        update_conversation(user_input, gpt3_response)
        return gpt3_response

    # Default response if no answer is found
    default_response = "I'm sorry, I couldn't find an answer to your question."
    update_conversation(user_input, default_response)
    return default_response

if __name__ == '__main__':
    print("Let's chat! (type 'quit' to exit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("ChatBot: Goodbye!")
            break

        response = get_chatbot_response(user_input)
        print("ChatBot:", response)

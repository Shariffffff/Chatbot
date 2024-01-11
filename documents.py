from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from database import Document

docsearch = None
chain = None

def init_docsearch_and_chain(app):
    global docsearch, chain
    with app.app_context():
        text = read_documents_from_database()

        # Check if there is any text from documents
        if not text.strip():
            print("No documents found in the database.")
            return

        char_text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
        text_chunks = char_text_splitter.split_text(text)

        # Debugging: Check if text chunks are created
        print("Number of text chunks:", len(text_chunks))
        if text_chunks:
            print("Sample text chunk:", text_chunks[0][:100])  # Print first 100 characters of the first chunk
        else:
            print("No text chunks created. Please check the document contents.")
            return  # Exit the function as there are no text chunks

        embeddings = OpenAIEmbeddings()
        docsearch = FAISS.from_texts(text_chunks, embeddings)
        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type="stuff")

def read_documents_from_database():
    combined_text = ""
    documents = Document.query.all()
    for doc in documents:
        combined_text += doc.content + "\n\n"
    return combined_text

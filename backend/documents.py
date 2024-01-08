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

        char_text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000,
                                                   chunk_overlap=200, length_function=len)
        text_chunks = char_text_splitter.split_text(text)

        embeddings = OpenAIEmbeddings()
        docsearch = FAISS.from_texts(text_chunks, embeddings)

        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type="stuff")

def read_documents_from_database():
    combined_text = ""
    documents = Document.query.all()  # Fetch all documents from the database
    for doc in documents:
        combined_text += doc.content + "\n\n"  # Concatenate the content of each document
    return combined_text

from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
import os

import threading

app = Flask(__name__)
CORS(app)

# Global variables
vectorstore = None
llm = None
pdf_path = os.path.join(os.path.dirname(__file__), "document.pdf")

def initialize_chatbot():
    global vectorstore, llm
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(text)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma.from_texts(chunks, embeddings)
        llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama3-8b-8192")
        return True
    except Exception as e:
        print(f"Error initializing: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pdf')
def get_pdf():
    return send_file(pdf_path, mimetype='application/pdf')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        docs = vectorstore.similarity_search(question, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        prompt = f"Based on the following context, answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"
        response = llm.invoke(prompt).content
        
        return jsonify({'answer': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    return jsonify({'ready': vectorstore is not None and llm is not None})

# Initialize in background so port binds immediately
print("Starting chatbot initialization in background...")
threading.Thread(target=initialize_chatbot, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

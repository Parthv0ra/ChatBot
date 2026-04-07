from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
import os

app = Flask(__name__)
CORS(app)

# Global variables
vectorstore = None
llm = None
pdf_path = "document.pdf"  # Place your PDF in the backend folder

def initialize_chatbot():
    global vectorstore, llm
    try:
        if not os.path.exists(pdf_path):
            print(f"PDF not found at {pdf_path}")
            return False
            
        print("Loading PDF...")
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        print("Creating embeddings...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(text)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma.from_texts(chunks, embeddings)
        
        print("Connecting to Ollama...")
        llm = Ollama(model="llama2", base_url=os.getenv("OLLAMA_URL", "http://localhost:11434"))
        
        print("Chatbot initialized successfully!")
        return True
    except Exception as e:
        print(f"Error initializing: {e}")
        return False

@app.route('/')
def index():
    return jsonify({"message": "AI Master Document Assistant API", "status": "running"})

@app.route('/api/pdf')
def get_pdf():
    if os.path.exists(pdf_path):
        return send_file(pdf_path, mimetype='application/pdf')
    return jsonify({'error': 'PDF not found'}), 404

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        if not vectorstore or not llm:
            return jsonify({'error': 'Chatbot not initialized'}), 503
        
        docs = vectorstore.similarity_search(question, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        prompt = f"Based on the following context, answer the question concisely.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"
        response = llm.invoke(prompt)
        
        return jsonify({'answer': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    return jsonify({
        'ready': vectorstore is not None and llm is not None,
        'pdf_exists': os.path.exists(pdf_path)
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    print("Starting AI Master Document Assistant API...")
    initialize_chatbot()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

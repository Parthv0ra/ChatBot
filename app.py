from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
import os

app = Flask(__name__)
CORS(app)

chunks = []
llm = None
is_ready = False
pdf_path = os.path.join(os.path.dirname(__file__), "document.pdf")

def simple_search(question, k=3):
    question_words = set(question.lower().split())
    scored = []
    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        score = len(question_words & chunk_words)
        scored.append((score, chunk))
    scored.sort(reverse=True)
    return [c for _, c in scored[:k]]

def initialize_chatbot():
    global chunks, llm, is_ready
    try:
        print("Loading PDF...")
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        print("Splitting text...")
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_text(text)

        print("Connecting to Groq...")
        llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.3-70b-versatile")

        is_ready = True
        print("Chatbot ready!")
    except Exception as e:
        print(f"Error initializing: {e}")

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
        if not chunks or not llm:
            return jsonify({'error': 'Chatbot is still initializing, please wait...'}), 503
        relevant = simple_search(question, k=3)
        context = "\n\n".join(relevant)
        prompt = f"Based on the following context, answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"
        response = llm.invoke(prompt).content
        return jsonify({'answer': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    return jsonify({'ready': is_ready})

print("Starting chatbot initialization...")
initialize_chatbot()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

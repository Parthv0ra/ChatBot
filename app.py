from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
import os
import json
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)
CORS(app)

chunks = []
llm = None
is_ready = False
pdf_path = os.path.join(os.path.dirname(__file__), "document.pdf")

log_path = os.path.join(os.path.dirname(__file__), "chat_logs.json")

SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def get_sheet():
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    if not creds_json:
        return None
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(os.getenv("GOOGLE_SHEET_ID")).sheet1

def log_chat(question, answer):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Save locally
    entry = {"timestamp": timestamp, "question": question, "answer": answer}
    logs = []
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            logs = json.load(f)
    logs.append(entry)
    with open(log_path, "w") as f:
        json.dump(logs, f, indent=2)
    # Save to Google Sheet
    try:
        sheet = get_sheet()
        if sheet:
            if sheet.row_count == 0 or sheet.cell(1, 1).value != "Timestamp":
                sheet.append_row(["Timestamp", "Question", "Answer"])
            sheet.append_row([timestamp, question, answer])
    except Exception as e:
        print(f"Google Sheets logging error: {e}")


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
        log_chat(question, response)
        return jsonify({'answer': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logs')
def get_logs():
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.route('/api/status')
def status():
    return jsonify({'ready': is_ready})

print("Starting chatbot initialization...")
initialize_chatbot()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

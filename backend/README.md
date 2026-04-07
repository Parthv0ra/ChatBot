# AI Master Document Assistant - Backend

## Setup Instructions

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Place your PDF file in this directory and name it `document.pdf`

3. Run the server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Deploy to Render

1. Create a new account on [Render](https://render.com)

2. Create a new **Web Service**

3. Connect your GitHub repository

4. Configure the service:
   - **Name**: ai-document-assistant-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

5. Add your PDF file to the repository as `document.pdf`

6. Deploy!

### Important Notes

- **Ollama Limitation**: The free Render deployment won't support Ollama (requires GPU/local setup)
- **Alternative**: Replace Ollama with OpenAI API or use Hugging Face Inference API
- For production, consider using OpenAI GPT-3.5/4 or Anthropic Claude

### API Endpoints

- `GET /` - API info
- `GET /api/pdf` - Get PDF file
- `POST /api/chat` - Send question, get answer
- `GET /api/status` - Check if chatbot is ready
- `GET /health` - Health check

### Environment Variables (Optional)

- `PORT` - Server port (default: 5000)
- `OLLAMA_URL` - Ollama server URL (default: http://localhost:11434)

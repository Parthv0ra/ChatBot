# AI Master Document Assistant

A web-based AI chatbot that answers questions about PDF documents using RAG (Retrieval Augmented Generation).

## 🚀 Features

- 📄 **PDF Viewer** - View documents in the browser
- 💬 **AI Chatbot** - Ask questions about the document
- 🎨 **Modern UI** - Beautiful, responsive design
- 🔄 **Real-time** - Instant responses
- 📱 **Mobile Friendly** - Works on all devices

## 📁 Project Structure

```
pdf_chatbot/
├── backend/           # Flask API
│   ├── app.py
│   ├── requirements.txt
│   ├── Procfile
│   └── document.pdf   # Your PDF file
├── frontend/          # Static HTML/CSS/JS
│   └── index.html
└── README.md
```

## 🛠️ Local Development

### Backend

1. Navigate to backend folder:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Place your PDF as `document.pdf` in the backend folder

4. Run the server:
```bash
python app.py
```

Backend will run at `http://localhost:5000`

### Frontend

1. Open `frontend/index.html` in a web browser
2. The app will connect to `http://localhost:5000`

## 🌐 Deployment Guide

### Step 1: Deploy Backend to Render

1. Create a [Render](https://render.com) account

2. Create a new **Web Service**

3. Connect your GitHub repository

4. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

5. Add your `document.pdf` to the backend folder

6. Deploy and copy the backend URL (e.g., `https://your-app.onrender.com`)

### Step 2: Deploy Frontend

#### Option A: Netlify (Recommended)

1. Go to [Netlify](https://www.netlify.com)
2. Drag and drop the `frontend` folder
3. Update `API_URL` in `index.html` with your Render backend URL
4. Done! Share your Netlify URL

#### Option B: Vercel

1. Install Vercel CLI: `npm install -g vercel`
2. Run `vercel` in frontend directory
3. Update `API_URL` in `index.html`
4. Share your Vercel URL

#### Option C: GitHub Pages

1. Create a GitHub repository
2. Upload `frontend/index.html`
3. Enable GitHub Pages in Settings
4. Update `API_URL` in `index.html`
5. Share your GitHub Pages URL

### Step 3: Update API URL

In `frontend/index.html`, find line ~318 and update:

```javascript
const API_URL = 'https://your-backend-url.onrender.com';
```

## ⚠️ Important Notes

### Ollama Limitation

The current backend uses Ollama which requires:
- Local installation
- GPU/CPU resources
- Not available on free hosting

### Production Alternative

For production deployment, replace Ollama with:

1. **OpenAI API** (Recommended)
```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(api_key="your-key", model="gpt-3.5-turbo")
```

2. **Anthropic Claude**
```python
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(api_key="your-key")
```

3. **Hugging Face Inference API**
```python
from langchain_huggingface import HuggingFaceEndpoint
llm = HuggingFaceEndpoint(repo_id="meta-llama/Llama-2-7b-chat-hf")
```

## 📤 Sharing Your App

Once deployed:

1. **Frontend URL**: Share this with users
   - Example: `https://ai-document-assistant.netlify.app`

2. **Backend URL**: Keep this private (API endpoint)
   - Example: `https://your-backend.onrender.com`

Users can:
- View the PDF
- Click the chat icon
- Ask questions about the document
- Get AI-powered answers

## 🔧 Troubleshooting

### CORS Errors
- Make sure `flask-cors` is installed
- Check that backend URL is correct in frontend

### PDF Not Loading
- Verify `document.pdf` exists in backend folder
- Check browser console for errors

### Chatbot Not Responding
- Check backend logs on Render
- Verify Ollama is running (local) or API keys are set (production)

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Pull requests are welcome!

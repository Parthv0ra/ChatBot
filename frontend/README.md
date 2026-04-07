# AI Master Document Assistant - Frontend

## Setup Instructions

### Local Development

1. Open `index.html` in a web browser
2. Make sure the backend is running at `http://localhost:5000`
3. If your backend is at a different URL, edit line 318 in `index.html`:
   ```javascript
   const API_URL = 'http://localhost:5000'; // Change this
   ```

### Deploy to Render (Static Site)

1. Create a new account on [Render](https://render.com)

2. Create a new **Static Site**

3. Connect your GitHub repository (frontend folder)

4. Configure the service:
   - **Name**: ai-document-assistant-frontend
   - **Build Command**: (leave empty)
   - **Publish Directory**: `.`
   - **Plan**: Free

5. **IMPORTANT**: After deploying backend, update the API_URL in `index.html`:
   ```javascript
   const API_URL = 'https://your-backend-url.onrender.com';
   ```

6. Deploy!

### Alternative: Deploy to Netlify/Vercel

#### Netlify:
1. Drag and drop the `frontend` folder to [Netlify Drop](https://app.netlify.com/drop)
2. Update API_URL in index.html with your backend URL
3. Done!

#### Vercel:
1. Install Vercel CLI: `npm install -g vercel`
2. Run `vercel` in the frontend directory
3. Update API_URL in index.html with your backend URL
4. Done!

### GitHub Pages (Free Hosting)

1. Create a GitHub repository
2. Upload `index.html` to the repository
3. Go to Settings > Pages
4. Select main branch as source
5. Update API_URL with your backend URL
6. Your site will be at: `https://yourusername.github.io/repo-name`

## Configuration

Edit the `API_URL` constant in `index.html` (around line 318):

```javascript
const API_URL = 'https://your-backend-url.onrender.com';
```

## Features

- 📄 PDF Viewer
- 💬 Floating Chat Bot
- 🎨 Modern UI
- 📱 Responsive Design
- ⚡ Real-time Chat

## Sharing

Once deployed, share the frontend URL with anyone:
- Example: `https://ai-document-assistant.netlify.app`
- Users can view the PDF and chat with the AI assistant

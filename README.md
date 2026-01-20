# spotify-ai

🎧 **spotify-ai** is a Streamlit web app that uses OpenAI's GPT-4 and the Spotify API to generate personalized Spotify playlists based on user-submitted moods, moments, or memories.

Users describe a moment or feeling in natural language, and the AI creates a playlist title and description. The app then lets users create that playlist directly in their Spotify account.

---

## Features

- OAuth 2.0 authentication with Spotify for secure access to user accounts  
- Natural language input for describing moods or moments  
- GPT-4 powered playlist title and description generation  
- Create and save playlists directly on Spotify  
- Simple, clean Streamlit frontend for easy user interaction  

---

## Getting Started

### Prerequisites

- Python 3.8+  
- Spotify Developer account with an app created (get Client ID and Client Secret)  
- OpenAI API key (with access to GPT-4)  

### Installation

1. Clone the repo

   ```bash
   git clone https://github.com/your-username/spotify-ai.git
   cd spotify-ai
2. Install dependencies

   ```bash
    pip install -r requirements.txt

4. Create a .env file with the following variables:
  
  ```bash
    SPOTIFY_CLIENT_ID=your_spotify_client_id
    SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
    REDIRECT_URI=http://localhost:8501/
    OPENAI_API_KEY=your_openai_api_key

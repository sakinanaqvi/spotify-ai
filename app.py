import streamlit as st
import requests
import os
from urllib.parse import urlencode
import openai

# --- CONFIG ---
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "https://spotify-ai.streamlit.app/callback"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1"

SCOPES = "playlist-modify-public playlist-modify-private"

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="spotify-ai", page_icon="🎧")

st.title("🎧 spotify-ai")
st.caption("Turn memories, moods, and moments into Spotify playlists")

# --- AUTH LINK ---
params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPES,
    "show_dialog": "true",
}

auth_url = f"{AUTH_URL}?{urlencode(params)}"

# --- CALLBACK HANDLING ---
query_params = st.experimental_get_query_params()

if "code" not in query_params:
    st.markdown(f"### [Connect your Spotify account]({auth_url})")
    st.stop()

code = query_params["code"][0]

# --- TOKEN EXCHANGE ---
token_response = requests.post(
    TOKEN_URL,
    data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    },
)

access_token = token_response.json().get("access_token")

headers = {"Authorization": f"Bearer {access_token}"}

# --- GET USER PROFILE ---
profile = requests.get(f"{API_BASE_URL}/me", headers=headers).json()
user_id = profile["id"]

st.success(f"Connected as {profile['display_name']}")

st.markdown("## Describe the moment you want music for")

user_input = st.text_area(
    "",
    placeholder="A late-night drive, quiet but hopeful...",
)

def generate_playlist_metadata(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a music curator."},
            {"role": "user", "content": f"Create a playlist title and description for this moment: {prompt}"}
        ]
    )
    return response.choices[0].message.content

def create_playlist(user_id, name, description):
    res = requests.post(
        f"{API_BASE_URL}/users/{user_id}/playlists",
        headers=headers,
        json={
            "name": name,
            "description": description,
            "public": True,
        },
    )
    return res.json()

metadata = None

if user_input:
    with st.spinner("✨ Generating playlist idea..."):
        try:
            metadata = generate_playlist_metadata(user_input)
            st.write(metadata)
        except Exception as e:
            st.error(f"Oops, something went wrong: {e}")

if metadata:
    if st.button("Create Playlist on Spotify"):
        # For now, just pass the whole metadata string as the playlist name
        # You can parse out name and description separately if you want
        result = create_playlist(user_id, metadata, metadata)
        if "id" in result:
            st.success("Playlist created successfully!")
        else:
            st.error("Failed to create playlist.")

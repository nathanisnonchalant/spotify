import spotipy
from spotipy.oauth2 import SpotifyOAuth
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# ---------------- Spotify API Credentials ----------------
CLIENT_ID = "9a4c582f7e7240c1b3c3ab675ff03926"
CLIENT_SECRET = "4ba21e33bf7d43f29189d80fa32aa24b"
REDIRECT_URI = "http://127.0.0.1:8080/callback"

# ---------------- Spotify Authentication ----------------
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-playback-state user-modify-playback-state user-read-currently-playing"
))

# ---------------- Tkinter GUI ----------------
root = tk.Tk()
root.title("Spotify Controller")

# Album art display
album_art_label = tk.Label(root)
album_art_label.pack(pady=10)

# Label to show now playing info
now_playing_label = tk.Label(root, text="Loading current song...", font=("Arial", 14))
now_playing_label.pack(pady=10)

# ---------------- Functions ----------------
def update_now_playing():
    track = sp.current_playback()
    if track and track['item']:
        song_name = track['item']['name']
        artist_name = track['item']['artists'][0]['name']
        now_playing_label.config(text=f"Now Playing: {song_name} - {artist_name}")

        # Get album art
        album_url = track['item']['album']['images'][0]['url']
        response = requests.get(album_url)
        img_data = Image.open(BytesIO(response.content))
        img_data = img_data.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img_data)

        album_art_label.config(image=img_tk)
        album_art_label.image = img_tk  # keep reference
    else:
        now_playing_label.config(text="No song is playing.")
        album_art_label.config(image='')

    root.after(5000, update_now_playing)  # refresh every 5 sec

def play_song():
    sp.start_playback()
    update_now_playing()

def pause_song():
    sp.pause_playback()
    update_now_playing()

def next_song():
    sp.next_track()
    update_now_playing()

def prev_song():
    sp.previous_track()
    update_now_playing()

# ---------------- Buttons ----------------
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

play_btn = tk.Button(button_frame, text="▶ Play", command=play_song, width=10)
play_btn.grid(row=0, column=0, padx=5)

pause_btn = tk.Button(button_frame, text="⏸ Pause", command=pause_song, width=10)
pause_btn.grid(row=0, column=1, padx=5)

next_btn = tk.Button(button_frame, text="⏭ Next", command=next_song, width=10)
next_btn.grid(row=0, column=2, padx=5)

prev_btn = tk.Button(button_frame, text="⏮ Previous", command=prev_song, width=10)
prev_btn.grid(row=0, column=3, padx=5)

# ---------------- Start ----------------
update_now_playing()
root.mainloop()

import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
from pydub import AudioSegment
from mutagen.mp3 import MP3
from plyer import notification
import os
import random

# Initialize pygame mixer
pygame.mixer.init()

# Function to apply equalizer effects using pydub
def apply_equalizer(audio, bass=0, mid=0, treble=0):
    bass_audio = audio.low_pass_filter(250).apply_gain(bass)
    mid_audio = audio.high_pass_filter(250).low_pass_filter(4000).apply_gain(mid)
    treble_audio = audio.high_pass_filter(4000).apply_gain(treble)
    processed_audio = bass_audio.overlay(mid_audio).overlay(treble_audio)
    return processed_audio

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Music Player")
        self.root.geometry("600x400")

        # Initialize variables
        self.playlist = []
        self.current_song = None
        self.paused = False
        self.equalized_audio = None
        self.volume = 0.5
        self.repeat_mode = False
        self.shuffle_mode = False
        self.song_index = 0

        # Initialize GUI
        self.setup_ui()

    def setup_ui(self):
        # Load button
        self.load_button = tk.Button(self.root, text="Load", command=self.load_song)
        self.load_button.pack()

        # Play/Pause button
        self.play_button = tk.Button(self.root, text="Play", command=self.play_pause_song)
        self.play_button.pack()

        # Stop button
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_song)
        self.stop_button.pack()

        # Volume control
        self.volume_scale = tk.Scale(self.root, from_=0, to=1, resolution=0.1, orient="horizontal", command=self.set_volume)
        self.volume_scale.set(self.volume)
        self.volume_scale.pack()

        # Equalizer controls
        self.bass_scale = tk.Scale(self.root, from_=-10, to=10, resolution=1, orient="horizontal", label="Bass")
        self.bass_scale.pack()
        self.mid_scale = tk.Scale(self.root, from_=-10, to=10, resolution=1, orient="horizontal", label="Mid")
        self.mid_scale.pack()
        self.treble_scale = tk.Scale(self.root, from_=-10, to=10, resolution=1, orient="horizontal", label="Treble")
        self.treble_scale.pack()
        self.equalizer_button = tk.Button(self.root, text="Apply Equalizer", command=self.apply_equalizer_settings)
        self.equalizer_button.pack()

        # Playlist
        self.playlist_box = tk.Listbox(self.root)
        self.playlist_box.pack(fill=tk.BOTH, expand=True)

        # Control buttons
        self.next_button = tk.Button(self.root, text="Next", command=self.next_song)
        self.next_button.pack()
        self.prev_button = tk.Button(self.root, text="Previous", command=self.prev_song)
        self.prev_button.pack()

        # Shuffle and repeat controls
        self.shuffle_button = tk.Button(self.root, text="Shuffle", command=self.toggle_shuffle)
        self.shuffle_button.pack()
        self.repeat_button = tk.Button(self.root, text="Repeat", command=self.toggle_repeat)
        self.repeat_button.pack()

        # Display metadata
        self.metadata_label = tk.Label(self.root, text="Metadata: ")
        self.metadata_label.pack()

        # Song lyrics display
        self.lyrics_box = tk.Text(self.root, height=5)
        self.lyrics_box.pack()

    def load_song(self):
        song = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if song:
            self.playlist.append(song)
            self.playlist_box.insert(tk.END, os.path.basename(song))
            self.display_metadata(song)

    def play_pause_song(self):
        if not self.paused:
            if self.current_song:
                pygame.mixer.music.unpause()
            else:
                self.play_song()
        else:
            pygame.mixer.music.pause()
            self.paused = True
            self.play_button.config(text="Play")

    def play_song(self):
        if self.playlist:
            self.current_song = self.playlist[self.song_index]
            if self.equalized_audio:
                temp_file = "temp_eq_song.mp3"
                self.equalized_audio.export(temp_file, format="mp3")
                pygame.mixer.music.load(temp_file)
            else:
                pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play()
            self.paused = False
            self.play_button.config(text="Pause")
            self.display_metadata(self.current_song)
            self.show_notification()

    def stop_song(self):
        pygame.mixer.music.stop()
        self.play_button.config(text="Play")

    def next_song(self):
        if self.shuffle_mode:
            self.song_index = random.randint(0, len(self.playlist) - 1)
        else:
            self.song_index = (self.song_index + 1) % len(self.playlist)
        self.play_song()

    def prev_song(self):
        self.song_index = (self.song_index - 1) % len(self.playlist)
        self.play_song()

    def set_volume(self, val):
        self.volume = float(val)
        pygame.mixer.music.set_volume(self.volume)

    def apply_equalizer_settings(self):
        if self.current_song:
            audio = AudioSegment.from_file(self.current_song)
            bass = self.bass_scale.get()
            mid = self.mid_scale.get()
            treble = self.treble_scale.get()
            self.equalized_audio = apply_equalizer(audio, bass, mid, treble)
            messagebox.showinfo("Equalizer", f"Equalizer applied: Bass {bass}, Mid {mid}, Treble {treble}")

    def toggle_shuffle(self):
        self.shuffle_mode = not self.shuffle_mode
        messagebox.showinfo("Shuffle", f"Shuffle {'On' if self.shuffle_mode else 'Off'}")

    def toggle_repeat(self):
        self.repeat_mode = not self.repeat_mode
        messagebox.showinfo("Repeat", f"Repeat {'On' if self.repeat_mode else 'Off'}")

    def display_metadata(self, song):
        try:
            audio = MP3(song)
            metadata = f"Title: {audio.get('TIT2')}, Artist: {audio.get('TPE1')}, Length: {audio.info.length:.2f}s"
            self.metadata_label.config(text=metadata)
        except Exception as e:
            print("Error loading metadata:", e)

    def show_notification(self):
        title = os.path.basename(self.current_song)
        notification.notify(title="Now Playing", message=title, timeout=10)

root = tk.Tk()
app = MusicPlayer(root)
root.mainloop()
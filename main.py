import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

# Create a simple class for the music player
class MusicPlayer:
    def __init__(self):
        self.current_song = None
        self.paused = False

    def load_song(self, file_path):
        if os.path.exists(file_path):
            pygame.mixer.music.load(file_path)
            self.current_song = file_path
            print(f"Loaded: {file_path}")
        else:
            print(f"File not found: {file_path}")

    def play_song(self):
        if self.current_song:
            pygame.mixer.music.play()
            print(f"Playing: {self.current_song}")
        else:
            print("No song loaded")

    def pause_song(self):
        if not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
            print("Paused")
        else:
            print("Already paused")

    def resume_song(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            print("Resumed")
        else:
            print("Not paused")

    def stop_song(self):
        pygame.mixer.music.stop()
        print("Stopped")
        
# Main Program
if __name__ == "__main__":
    player = MusicPlayer()
    
    while True:
        print("\nOptions: load, play, pause, resume, stop, quit")
        action = input("Select an action: ").lower()
        
        if action == "load":
            song_path = input("Enter the path of the song: ")
            player.load_song(song_path)
        elif action == "play":
            player.play_song()
        elif action == "pause":
            player.pause_song()
        elif action == "resume":
            player.resume_song()
        elif action == "stop":
            player.stop_song()
        elif action == "quit":
            player.stop_song()
            break
        else:
            print("Invalid action. Please choose again.")
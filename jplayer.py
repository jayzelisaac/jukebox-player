# Import necessary libraries
import os
import pygame
import tkinter as tk
from tkinter import ttk

# Define the MusicPlayer class
class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title('Music Player')
        self.root.geometry('600x800')

        pygame.init()
        pygame.mixer.init()

        # Define music folder and list music files
        self.music_folder = r"C:\Users\User\Documents\Dev\jukebox player\music"
        self.music_files = [f for f in os.listdir(self.music_folder) if f.endswith('.mp3')]
        
        # Create and pack the playlist Listbox
        self.playlist = tk.Listbox(self.root, selectmode=tk.SINGLE, bg="black", fg="white", font=('arial', 12), width=50)
        self.playlist.pack(padx=15, pady=15)

        # Insert music files into the playlist
        for file in self.music_files:
            self.playlist.insert(tk.END, file)

        # Create and pack status and mode labels
        self.status_label = tk.Label(self.root, text="Now playing: ", font=('arial', 10))
        self.status_label.pack()
        self.mode_label = tk.Label(self.root, text="Mode: Song Mode", font=('arial', 10))
        self.mode_label.pack()

        # Create and pack song ID entry field
        self.song_id_entry = tk.Entry(self.root)
        self.song_id_entry.pack(pady=5)
        self.song_id_entry.focus_set()
        self.song_id_entry.bind('<Return>', self.play_song_by_id)

    # Define method to play song by ID
    def play_song_by_id(self, event):
        song_id = self.song_id_entry.get()
        try:
            song_id = int(song_id) - 1
            if 0 <= song_id < len(self.music_files):
                song_path = os.path.join(self.music_folder, self.music_files[song_id])
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play()
                self.status_label.config(text=f"Now playing: {self.music_files[song_id]}")
            else:
                self.status_label.config(text="Invalid song ID")
        except ValueError:
            self.status_label.config(text="Please enter a valid number")
        finally:
            self.song_id_entry.delete(0, tk.END)
            self.song_id_entry.focus_set()

# Create the main window and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
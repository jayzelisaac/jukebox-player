#F1r3F1ng3r5
import os
import pygame
import tkinter as tk
from tkinter import ttk

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title('Music Player')
        self.root.geometry('400x500')  # Adjusted window size to accommodate song ID entry

        pygame.init()
        pygame.mixer.init()

        self.music_folder = "C:\\Users\\User\\Documents\\Dev\\jukebox player\\music"
        self.music_files = [f for f in os.listdir(self.music_folder) if f.endswith('.mp3')]
        
        self.playlist = tk.Listbox(self.root, selectmode=tk.SINGLE, bg="black", fg="white", font=('arial', 12), width=50)
        self.playlist.pack(padx=15, pady=15)

        for file in self.music_files:
            self.playlist.insert(tk.END, file)

        # Display controls
        controls_label = tk.Label(self.root, text="Controls: Enter ID & Spacebar - Play, N - Next, P - Previous", font=('arial', 10))
        controls_label.pack()

        # Entry widget for song ID, accepting only numeric input
        vcmd = (self.root.register(self.validate_numeric_input), '%S')
        self.song_id_entry = tk.Entry(self.root, validate='key', validatecommand=vcmd)
        self.song_id_entry.pack(pady=5)
        self.song_id_entry.focus_set()  # Keep the Entry widget focused

        # Bind key events
        self.root.bind('<space>', self.play_selected_song)
        self.root.bind('n', self.play_next_song)
        self.root.bind('p', self.play_previous_song)
        self.root.bind('<Key>', self.keep_focus)  # Keep focus on the Entry widget

        self.current_song_index = None

    def validate_numeric_input(self, S):
        """Validate that the input is numeric."""
        return S.isdigit()

    def keep_focus(self, event):
        """Keep the Entry widget focused."""
        if event.keysym != 'space':
            self.song_id_entry.focus_set()
            return True
        return False

    def play_selected_song(self, event):
        try:
            song_id = int(self.song_id_entry.get()) - 1  # Convert to 0-based index
            if 0 <= song_id < len(self.music_files):
                self.current_song_index = song_id
                pygame.mixer.music.load(os.path.join(self.music_folder, self.music_files[song_id]))
                pygame.mixer.music.play()
            else:
                print("Invalid song ID")
        except ValueError:
            print("Please enter a valid song ID")
        return 'break'  # Prevent space from being added to the Entry widget

    def play_next_song(self, event):
        if self.current_song_index is not None:
            self.current_song_index = (self.current_song_index + 1) % len(self.music_files)
            self.play_song(self.current_song_index)

    def play_previous_song(self, event):
        if self.current_song_index is not None:
            self.current_song_index = (self.current_song_index - 1) % len(self.music_files)
            self.play_song(self.current_song_index)

    def play_song(self, index):
        pygame.mixer.music.load(os.path.join(self.music_folder, self.music_files[index]))
        pygame.mixer.music.play()

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
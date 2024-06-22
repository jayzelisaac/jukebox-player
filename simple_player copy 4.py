import os
import pygame
import tkinter as tk
from tkinter import ttk
from mutagen.mp3 import MP3

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title('Music Player')
        self.root.geometry('600x800')

        # Initialize pygame and mixer
        pygame.init()
        pygame.mixer.init()

        # Music folders
        self.music_folder = r"C:\Users\User\Documents\Dev\jukebox player\music"
        self.music_files = [f for f in os.listdir(self.music_folder) if f.endswith('.mp3')]
        self.music_folder2 = r"C:\Users\User\Documents\Dev\jukebox player\music2"
        self.music_files2 = [f for f in os.listdir(self.music_folder2) if f.endswith('.mp3')]

        # UI elements
        self.setup_ui()

        # Initialize player state
        self.current_song_index = None
        self.current_song_path = None

        # Bind keyboard events
        self.root.bind('<space>', self.play_selected_song)
        self.root.bind('n', self.play_next_song)
        self.root.bind('p', self.play_previous_song)
        self.root.bind('<Key>', self.keep_focus)

        # Check pygame events (e.g., song end)
        self.check_pygame_events()

        # Start automatic playback if there are songs in the second folder
        self.start_automatic_playback()

    def setup_ui(self):
        # Playlist for first folder
        self.playlist_frame = ttk.Frame(self.root)
        self.playlist_frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

        self.playlist_label = ttk.Label(self.playlist_frame, text="Music Folder 1", font=('Arial', 12, 'bold'))
        self.playlist_label.pack(pady=5)

        self.playlist = tk.Listbox(self.playlist_frame, selectmode=tk.SINGLE, bg="black", fg="white", font=('Arial', 12), width=50)
        self.playlist.pack(pady=5, fill=tk.BOTH, expand=True)

        for file in self.music_files:
            self.playlist.insert(tk.END, file)

        # Playlist for second folder
        self.playlist2_frame = ttk.Frame(self.root)
        self.playlist2_frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

        self.playlist2_label = ttk.Label(self.playlist2_frame, text="Music Folder 2", font=('Arial', 12, 'bold'))
        self.playlist2_label.pack(pady=5)

        self.playlist2 = tk.Listbox(self.playlist2_frame, selectmode=tk.SINGLE, bg="black", fg="white", font=('Arial', 12), width=50)
        self.playlist2.pack(pady=5, fill=tk.BOTH, expand=True)

        for file in self.music_files2:
            self.playlist2.insert(tk.END, file)

        # Controls and status labels
        self.controls_frame = ttk.Frame(self.root)
        self.controls_frame.pack(padx=15, pady=10)

        self.controls_label = ttk.Label(self.controls_frame, text="Controls: Enter ID & Spacebar - Play, N - Next, P - Previous", font=('Arial', 10))
        self.controls_label.pack()

        self.status_label = ttk.Label(self.root, text="Now playing: ", font=('Arial', 10))
        self.status_label.pack(pady=5)

        self.mode_label = ttk.Label(self.root, text="Mode: Song Mode", font=('Arial', 10))
        self.mode_label.pack()

        # Song ID entry
        self.song_id_entry = ttk.Entry(self.root, font=('Arial', 12))
        self.song_id_entry.pack(pady=5)
        self.song_id_entry.focus_set()

        # Progress bar and duration label
        self.progress_frame = ttk.Frame(self.root)
        self.progress_frame.pack(padx=15, pady=10, fill=tk.X)

        self.progress_label = ttk.Label(self.progress_frame, text="Progress: ")
        self.progress_label.pack(side=tk.LEFT)

        self.progress = ttk.Progressbar(self.progress_frame, orient='horizontal', length=300, mode='determinate')
        self.progress.pack(fill=tk.X, expand=True)

        self.duration_label = ttk.Label(self.root, text="00:00 / 00:00", font=('Arial', 10))
        self.duration_label.pack(pady=5)

    def validate_numeric_input(self, S):
        return S.isdigit()

    def keep_focus(self, event):
        if event.keysym != 'space':
            self.song_id_entry.focus_set()
            return True
        return False

    def check_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.handle_song_end()
        self.root.after(100, self.check_pygame_events)

    def play_selected_song(self, event):
        try:
            song_id = int(self.song_id_entry.get()) - 1
            if 0 <= song_id < len(self.music_files):
                self.current_song_index = song_id
                self.current_song_path = os.path.join(self.music_folder, self.music_files[song_id])
                pygame.mixer.music.load(self.current_song_path)
                pygame.mixer.music.play()
                self.status_label.config(text=f"Now playing: {self.music_files[song_id]}")
                self.mode_label.config(text="Mode: Song Mode")
                self.update_progress_and_duration()
            else:
                print("Invalid song ID")
        except ValueError:
            print("Please enter a valid song ID")
        return 'break'

    def play_next_song(self, event):
        if self.current_song_index is not None:
            self.current_song_index = (self.current_song_index + 1) % len(self.music_files)
            self.play_song(self.current_song_index)

    def play_previous_song(self, event):
        if self.current_song_index is not None:
            self.current_song_index = (self.current_song_index - 1) % len(self.music_files)
            self.play_song(self.current_song_index)

    def play_song(self, index):
        self.current_song_path = os.path.join(self.music_folder, self.music_files[index])
        pygame.mixer.music.load(self.current_song_path)
        pygame.mixer.music.play()
        self.status_label.config(text=f"Now playing: {self.music_files[index]}")
        self.mode_label.config(text="Mode: Song Mode")
        self.update_progress_and_duration()

    def start_automatic_playback(self):
        if self.music_files2:
            self.play_music2()

    def play_music2(self):
        self.current_song_path = os.path.join(self.music_folder2, self.music_files2[self.current_music2_index])
        pygame.mixer.music.load(self.current_song_path)
        pygame.mixer.music.play(fade_ms=1000)
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        self.status_label.config(text=f"Now playing: {self.music_files2[self.current_music2_index]}")
        self.mode_label.config(text="Mode: Mix Mode")
        self.update_progress_and_duration()
        self.current_music2_index = (self.current_music2_index + 1) % len(self.music_files2)

    def handle_song_end(self):
        if self.mode_label.cget("text") == "Mode: Song Mode":
            self.play_music2()

    def update_progress_and_duration(self):
        if pygame.mixer.music.get_busy() and self.current_song_path:
            audio = MP3(self.current_song_path)
            total_length = audio.info.length
            playback_time = pygame.mixer.music.get_pos() / 1000
            remaining_time = total_length - playback_time

            self.progress['value'] = (playback_time / total_length) * 100

            total_str = f"{int(total_length // 60)}:{int(total_length % 60):02d}"
            playback_str = f"{int(playback_time // 60)}:{int(playback_time % 60):02d}"
            self.duration_label.config(text=f"{playback_str} / {total_str}")

            self.root.after(1000, self.update_progress_and_duration)
        else:
            self.progress['value'] = 0
            self.duration_label.config(text="00:00 / 00:00")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()

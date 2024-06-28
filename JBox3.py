import os
import pygame
import tkinter as tk
from tkinter import ttk
from mutagen.mp3 import MP3
from pathlib import Path

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title('Music Player')
        self.root.geometry('900x900')
        self.root.configure(bg="#E5B402")

        pygame.init()
        pygame.mixer.init()

        # Change working directory to desktop
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        os.chdir(desktop)

        # Ensure music folders exist
        self.music_folder = os.path.join(desktop, 'music')
        self.music_folder2 = os.path.join(desktop, 'music2')
        os.makedirs(self.music_folder, exist_ok=True)
        os.makedirs(self.music_folder2, exist_ok=True)

        self.music_files = [f for f in os.listdir(self.music_folder) if f.endswith('.mp3')]
        self.music_files2 = [f for f in os.listdir(self.music_folder2) if f.endswith('.mp3')]

        self.current_music2_index = 0
        self.current_song_path = None

        self.setup_ui()
        self.check_pygame_events()
        self.start_automatic_playback()

    def setup_ui(self):
        # Configure grid layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # Title
        title_label = tk.Label(self.root, text="J-Box player", font=("Inter SemiBold", 40), bg="#E5B402", fg="#1E1E1E")
        title_label.grid(row=0, column=0, columnspan=3, pady=20, sticky="n")

        # Music Folder Listbox (Scrollable) - Top Left
        playlist_frame = tk.Frame(self.root, bg="#E5B402")
        playlist_frame.grid(row=1, column=0, sticky="nw", padx=20, pady=20)
        playlist_scrollbar = tk.Scrollbar(playlist_frame)
        self.playlist = tk.Listbox(
            playlist_frame,
            selectmode=tk.SINGLE,
            bg="black",
            fg="white",
            font=('arial', 12),
            width=40,
            height=10,
            yscrollcommand=playlist_scrollbar.set
        )
        playlist_scrollbar.config(command=self.playlist.yview)
        playlist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.playlist.pack(side=tk.LEFT, fill=tk.BOTH)
        for file in self.music_files:
            self.playlist.insert(tk.END, file)

        # Music2 Folder Listbox (Scrollable) - Bottom Left
        playlist2_frame = tk.Frame(self.root, bg="#E5B402")
        playlist2_frame.grid(row=2, column=0, sticky="nw", padx=20, pady=20)
        playlist2_scrollbar = tk.Scrollbar(playlist2_frame)
        self.playlist2 = tk.Listbox(
            playlist2_frame,
            selectmode=tk.SINGLE,
            bg="black",
            fg="white",
            font=('arial', 12),
            width=40,
            height=10,
            yscrollcommand=playlist2_scrollbar.set
        )
        playlist2_scrollbar.config(command=self.playlist2.yview)
        playlist2_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.playlist2.pack(side=tk.LEFT, fill=tk.BOTH)
        for file in self.music_files2:
            self.playlist2.insert(tk.END, file)

        # User Input Section - Top Right
        user_input_frame = tk.Frame(self.root, bg="#E5B402")
        user_input_frame.grid(row=1, column=2, sticky="n", padx=20, pady=20)

        self.song_id_entry = tk.Entry(user_input_frame, bg="#FFFFFF", bd=0)
        self.song_id_entry.grid(row=0, column=0, padx=5, pady=5)

        vcmd = (self.root.register(self.validate_numeric_input), '%S')
        self.song_id_entry.config(validate='key', validatecommand=vcmd)
        self.song_id_entry.focus_set()

        # Status Section - Center
        status_frame = tk.Frame(self.root, bg="#E5B402")
        status_frame.grid(row=2, column=2, rowspan=2, padx=20, pady=20, sticky="n")

        self.status_label = tk.Label(status_frame, text="Now playing: ", font=('arial', 10), bg="#E5B402")
        self.status_label.pack(pady=5)

        self.mode_label = tk.Label(status_frame, text="Mode: Song Mode", font=('arial', 10), bg="#E5B402")
        self.mode_label.pack(pady=5)

        self.controls_label = tk.Label(
            status_frame, text="Controls: Enter ID & Spacebar - Play, N - Next, P - Previous", font=('arial', 10), bg="#E5B402")
        self.controls_label.pack(pady=5)

        self.progress = ttk.Progressbar(status_frame, orient='horizontal', length=300, mode='determinate', value=0)
        self.progress.pack(pady=10)

        self.duration_label = tk.Label(status_frame, text="00:00 / 00:00", font=("Inter", 12), bg="#FFFFFF")
        self.duration_label.pack(pady=5)

        # Spinning Logo - Bottom Right
        spinning_logo_frame = tk.Frame(self.root, bg="#E5B402")
        spinning_logo_frame.grid(row=2, column=2, sticky="se", padx=20, pady=20)
        # You can place your spinning logo implementation here.

        self.root.bind('<space>', self.play_selected_song)
        self.root.bind('n', self.play_next_song)
        self.root.bind('p', self.play_previous_song)
        self.root.bind('<Key>', self.keep_focus)

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
            remaining_str = f"{int(remaining_time // 60)}:{int(remaining_time % 60):02d}"
            self.duration_label.config(text=f"{total_str}, {remaining_str}")

            self.root.after(1000, self.update_progress_and_duration)
        else:
            self.progress['value'] = 0
            self.duration_label.config(text="00:00 / 00:00")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()

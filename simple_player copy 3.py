import os
import pygame
import tkinter as tk
from tkinter import ttk
from mutagen.mp3 import MP3

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title('Music Player')
        self.root.geometry('600x800')  # Maintain the larger window size

        pygame.init()
        pygame.mixer.init()

        self.music_folder = r"C:\Users\User\Documents\Dev\jukebox player\music"
        self.music_files = [f for f in os.listdir(self.music_folder) if f.endswith('.mp3')]
        self.playlist = tk.Listbox(self.root, selectmode=tk.SINGLE, bg="black", fg="white", font=('arial', 12), width=50)
        self.playlist.pack(padx=15, pady=15)

        for file in self.music_files:
            self.playlist.insert(tk.END, file)

        self.status_label = tk.Label(self.root, text="Now playing: ", font=('arial', 10))
        self.status_label.pack()
        self.mode_label = tk.Label(self.root, text="Mode: Song Mode", font=('arial', 10))
        self.mode_label.pack()

        self.controls_label = tk.Label(self.root, text="Controls: Enter ID & Spacebar - Play, N - Next, P - Previous", font=('arial', 10))
        self.controls_label.pack()

        vcmd = (self.root.register(self.validate_numeric_input), '%S')
        self.song_id_entry = tk.Entry(self.root, validate='key', validatecommand=vcmd)
        self.song_id_entry.pack(pady=5)
        self.song_id_entry.focus_set()

        self.root.bind('<space>', self.play_selected_song)
        self.root.bind('n', self.play_next_song)
        self.root.bind('p', self.play_previous_song)
        self.root.bind('<Key>', self.keep_focus)

        self.progress = ttk.Progressbar(self.root, orient='horizontal', length=300, mode='determinate', value=0)
        self.progress.pack(pady=10)
        self.duration_label = tk.Label(self.root, text="00:00, 00:00")
        self.duration_label.pack()

        self.music_folder2 = r"C:\Users\User\Documents\Dev\jukebox player\music2"
        self.music_files2 = [f for f in os.listdir(self.music_folder2) if f.endswith('.mp3')]

        self.playlist2 = tk.Listbox(self.root, selectmode=tk.SINGLE, bg="black", fg="white", font=('arial', 12), width=50)
        self.playlist2.pack(padx=15, pady=15)

        for file in self.music_files2:
            self.playlist2.insert(tk.END, file)

        self.current_music2_index = 0
        self.current_song_path = None

        self.check_pygame_events()
        self.start_automatic_playback()

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
            self.duration_label.config(text="00:00, 00:00")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()

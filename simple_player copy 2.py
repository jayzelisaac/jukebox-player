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

        self.song_id_entry = tk.Entry(self.root)
        self.song_id_entry.pack(pady=5)
        self.song_id_entry.focus_set()
        self.song_id_entry.bind('<Return>', self.play_song_by_id)
        self.root.bind('<Key>', self.filter_keys)

        self.controls_label = tk.Label(self.root, text="Enter ID & Spacebar - Play, N - Next, P - Previous", font=('arial', 10))
        self.controls_label.pack()

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
        self.music2_paused_at = 0

        # Disable mouse selection events on the playlists
        self.playlist.unbind('<<ListboxSelect>>')
        self.playlist2.unbind('<<ListboxSelect>>')

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        # Removed the problematic line and added check_pygame_events method call
        self.check_pygame_events()

        self.start_automatic_playback()

    def check_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.handle_song_end()
        # Call this method again after a short delay
        self.root.after(100, self.check_pygame_events)

    def filter_keys(self, event):
        if event.keysym not in ('n', 'p', 'space', 'Return') and not event.char.isdigit():
            return 'break'

    def play_song_by_id(self, event):
        song_id = self.song_id_entry.get()
        try:
            song_id = int(song_id) - 1
            if 0 <= song_id < len(self.music_files):
                pygame.mixer.music.fadeout(500)
                song_path = os.path.join(self.music_folder, self.music_files[song_id])
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play(fade_ms=1000)
                self.status_label.config(text=f"Now playing: {self.music_files[song_id]}")
                self.update_progress_and_duration(song_path)
                self.mode_label.config(text="Mode: Song Mode")
            else:
                self.status_label.config(text="Invalid song ID")
        except ValueError:
            self.status_label.config(text="Please enter a valid number")
        finally:
            self.song_id_entry.delete(0, tk.END)
            self.song_id_entry.focus_set()

    def start_automatic_playback(self):
        if self.music_files2:
            self.play_music2()

    def play_music2(self):
        song_path = os.path.join(self.music_folder2, self.music_files2[self.current_music2_index])
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(fade_ms=1000)
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        self.status_label.config(text=f"Mix Mode: {self.music_files2[self.current_music2_index]}")
        self.update_progress_and_duration(song_path)
        self.current_music2_index = (self.current_music2_index + 1) % len(self.music_files2)

    def handle_song_end(self):
        if self.mode_label.cget("text") == "Mode: Song Mode":
            self.play_music2()

    def update_progress_and_duration(self, song_path):
        audio = MP3(song_path)
        total_length = audio.info.length
        playback_time = pygame.mixer.music.get_pos() / 1000
        remaining_time = total_length - playback_time

        self.progress['value'] = (playback_time / total_length) * 100

        total_str = f"{int(total_length // 60)}:{int(total_length % 60):02d}"
        remaining_str = f"{int(remaining_time // 60)}:{int(remaining_time % 60):02d}"
        self.duration_label.config(text=f"{total_str}, {remaining_str}")

        if pygame.mixer.music.get_busy():
            self.root.after(1000, lambda: self.update_progress_and_duration(song_path))
        else:
            self.progress['value'] = 0
            self.duration_label.config(text="00:00, 00:00")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()

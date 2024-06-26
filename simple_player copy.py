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

        self.playlist.bind('<<ListboxSelect>>', self.on_music_folder_select)

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        self.update_progress()

    def filter_keys(self, event):
        if event.keysym not in ('n', 'p', 'space', 'Return') and not event.char.isdigit():
            return 'break'

    def play_song_by_id(self, event):
        song_id = self.song_id_entry.get()
        try:
            song_id = int(song_id) - 1
            if 0 <= song_id < len(self.music_files):
                self.music2_paused_at = pygame.mixer.music.get_pos()
                song_path = os.path.join(self.music_folder, self.music_files[song_id])
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play()
                self.status_label.config(text=f"Now playing: {self.music_files[song_id]}")
                self.update_progress_and_duration(song_path)
            else:
                self.status_label.config(text="Invalid song ID")
        except ValueError:
            self.status_label.config(text="Please enter a valid number")
        finally:
            self.song_id_entry.delete(0, tk.END)
            self.song_id_entry.focus_set()

    def on_music_folder_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            song = self.music_files[index]
            pygame.mixer.music.fadeout(500)
            song_path = os.path.join(self.music_folder, song)
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play(fade_ms=1000)
            self.mode_label.config(text="Mode: Song Mode")
            self.status_label.config(text=f"Now playing: {song}")
            self.update_progress_and_duration(song_path)

    def update_progress_and_duration(self, song_path):
        if pygame.mixer.music.get_busy():
            audio = MP3(song_path)
            total_length = audio.info.length  # Total length of the song in seconds
            playback_time = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
            remaining_time = total_length - playback_time

            # Update progress bar
            self.progress['value'] = (playback_time / total_length) * 100

            # Update duration label
            total_str = f"{int(total_length // 60)}:{int(total_length % 60):02d}"
            remaining_str = f"{int(remaining_time // 60)}:{int(remaining_time % 60):02d}"
            self.duration_label.config(text=f"{total_str}, {remaining_str}")

            self.root.after(1000, lambda: self.update_progress_and_duration(song_path))
        else:
            self.progress['value'] = 0
            self.duration_label.config(text="00:00, 00:00")

    def update_progress(self):
        # This method is now replaced by update_progress_and_duration
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
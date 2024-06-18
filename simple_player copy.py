import os
import pygame
import tkinter as tk
from tkinter import ttk

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

        self.music_folder2 = r"C:\Users\User\Documents\Dev\jukebox player\music2"
        self.music_files2 = [f for f in os.listdir(self.music_folder2) if f.endswith('.mp3')]
        
        self.playlist2 = tk.Listbox(self.root, selectmode=tk.SINGLE, bg="black", fg="white", font=('arial', 12), width=50)
        self.playlist2.pack(padx=15, pady=15)
        
        for file in self.music_files2:
            self.playlist2.insert(tk.END, file)

        self.progress = ttk.Progressbar(self.root, orient='horizontal', length=300, mode='determinate')
        self.progress.pack(pady=10)

        self.current_music2_index = 0
        self.music2_paused_at = 0

        self.play_song_from_folder2()

        self.playlist.bind('<<ListboxSelect>>', self.on_music_folder_select)

        # Set up event listening for song end
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

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
                # Listen for song end to resume music2
                self.root.after(100, self.check_music_end)
            else:
                self.status_label.config(text="Invalid song ID")
        except ValueError:
            self.status_label.config(text="Please enter a valid number")
        finally:
            self.song_id_entry.delete(0, tk.END)
            self.song_id_entry.focus_set()

    def play_song_from_folder2(self, start_at=0):
        if self.music_files2:
            pygame.mixer.music.fadeout(500)
            song_path = os.path.join(self.music_folder2, self.music_files2[self.current_music2_index])
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play(fade_ms=1000, start=start_at/1000.0)
            self.mode_label.config(text="Mode: Mix Mode")
            self.status_label.config(text=f"Now playing: {self.music_files2[self.current_music2_index]}")

    def on_music_folder_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            song = self.music_files[index]
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.load(os.path.join(self.music_folder, song))
            pygame.mixer.music.play(fade_ms=1000)
            self.mode_label.config(text="Mode: Song Mode")
            self.status_label.config(text=f"Now playing: {song}")

    def check_music_end(self):
        if not pygame.mixer.music.get_busy():
            # Song has ended, resume music2
            self.play_song_from_folder2(start_at=self.music2_paused_at)
        else:
            # Check again after 100ms
            self.root.after(100, self.check_music_end)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
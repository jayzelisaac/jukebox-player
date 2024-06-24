import os
import pygame
import tkinter as tk
from tkinter import ttk
from mutagen.mp3 import MP3
from pathlib import Path
from PIL import Image, ImageTk, ImageSequence

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title('Music Player')
        self.root.geometry('1200x900')
        self.create_gradient_bg()

        pygame.init()
        pygame.mixer.init()

        self.music_folder = r"C:\Users\User\Documents\Dev\jukebox player\music"
        self.music_files = [f for f in os.listdir(self.music_folder) if f.endswith('.mp3')]

        self.music_folder2 = r"C:\Users\User\Documents\Dev\jukebox player\music2"
        self.music_files2 = [f for f in os.listdir(self.music_folder2) if f.endswith('.mp3')]

        self.current_music2_index = 0
        self.current_song_path = None

        self.setup_ui()
        self.check_pygame_events()
        self.start_automatic_playback()

    def create_gradient_bg(self):
        self.canvas = tk.Canvas(self.root, width=1200, height=900)
        self.canvas.pack(fill="both", expand=True)
        self.gradient = Image.new('RGB', (1200, 900), color='#E5B402')
        self.draw_gradient(self.gradient)
        self.bg_image = ImageTk.PhotoImage(self.gradient)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

    def draw_gradient(self, img):
        width, height = img.size
        for y in range(height):
            r = int(229 * (height - y) / height + 255 * y / height)
            g = int(180 * (height - y) / height + 255 * y / height)
            b = int(2 * (height - y) / height + 255 * y / height)
            line = Image.new('RGB', (width, 1), color=(r, g, b))
            img.paste(line, (0, y))

    def setup_ui(self):
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\User\Documents\Dev\Tkinter-Designer-master\build\assets\frame0")

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_rowconfigure(1, weight=4)
        self.canvas.grid_rowconfigure(2, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(1, weight=1)

        # Title
        title_label = tk.Label(self.root, text="J-Box player", font=("Inter SemiBold", 40), bg="#E5B402", fg="#1E1E1E")
        self.canvas.create_window(20, 31, anchor="nw", window=title_label)

        # Playlist 1
        self.playlist = tk.Listbox(
            self.root,
            selectmode=tk.SINGLE,
            bg="black",
            fg="white",
            font=('arial', 14),
            width=40,
            height=20
        )
        self.canvas.create_window(50, 100, anchor="nw", window=self.playlist)
        for file in self.music_files:
            self.playlist.insert(tk.END, file)

        # Playlist 2
        self.playlist2 = tk.Listbox(
            self.root,
            selectmode=tk.SINGLE,
            bg="black",
            fg="white",
            font=('arial', 14),
            width=40,
            height=10
        )
        self.canvas.create_window(50, 520, anchor="nw", window=self.playlist2)
        for file in self.music_files2:
            self.playlist2.insert(tk.END, file)

        # Controls frame
        controls_frame = tk.Frame(self.root, bg="#E5B402")
        self.canvas.create_window(700, 100, anchor="nw", window=controls_frame)

        self.song_id_entry = tk.Entry(controls_frame, bg="#FFFFFF", bd=0)
        self.song_id_entry.grid(row=0, column=0, padx=5, pady=5)

        self.duration_label = tk.Label(controls_frame, text="00:00, 00:00", font=("Inter", 14), bg="#FFFFFF")
        self.duration_label.grid(row=1, column=0, padx=5, pady=5)

        self.status_label = tk.Label(controls_frame, text="Now playing: ", font=('arial', 12), bg="#E5B402")
        self.status_label.grid(row=2, column=0, padx=5, pady=5)

        self.mode_label = tk.Label(controls_frame, text="Mode: Song Mode", font=('arial', 12), bg="#E5B402")
        self.mode_label.grid(row=3, column=0, padx=5, pady=5)

        self.controls_label = tk.Label(
            controls_frame, text="Controls: Enter ID & Spacebar - Play, N - Next, P - Previous", font=('arial', 12), bg="#E5B402")
        self.controls_label.grid(row=4, column=0, padx=5, pady=5)

        self.progress = ttk.Progressbar(controls_frame, orient='horizontal', length=400, mode='determinate', value=0)
        self.progress.grid(row=5, column=0, padx=5, pady=10)

        # Load and place the spinning logo
        self.load_spinning_logo()

        vcmd = (self.root.register(self.validate_numeric_input), '%S')
        self.song_id_entry.config(validate='key', validatecommand=vcmd)
        self.song_id_entry.focus_set()

        self.root.bind('<space>', self.play_selected_song)
        self.root.bind('n', self.play_next_song)
        self.root.bind('p', self.play_previous_song)
        self.root.bind('<Key>', self.keep_focus)

    def load_spinning_logo(self):
        logo_path = r"C:\Users\User\Documents\Dev\jukebox-player\assests\images\spinning record.gif"  # Replace with the path to your spinning logo GIF
        self.logo_image = Image.open(logo_path)
        self.logo_frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(self.logo_image)]
        self.logo_index = 0

        self.logo_label = tk.Label(self.root, bg="#E5B402")
        self.canvas.create_window(1000, 700, anchor="nw", window=self.logo_label)
        self.animate_logo()

    def animate_logo(self):
        self.logo_label.config(image=self.logo_frames[self.logo_index])
        self.logo_index = (self.logo_index + 1) % len(self.logo_frames)
        self.root.after(100, self.animate_logo)

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

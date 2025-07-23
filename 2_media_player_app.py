import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pygame import mixer


# initialize Pygame mixer 
mixer.init()


# media player class
class MediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Player")
        self.root.geometry("400x300")

        self.playlist = []
        self.current_index = 0
        self.is_paused = False

        # buttons
        tk.Button(root, text="Load Songs", command=self.load_songs).pack(pady=10)
        tk.Button(root, text="Play", command=self.play_song).pack()
        tk.Button(root, text="Pause/Resume", command=self.pause_resume).pack()
        tk.Button(root, text="Next", command=self.next_song).pack()
        tk.Button(root, text="Previous", command=self.previous_song).pack()

        self.label = tk.Label(root, text="No Song Playing", fg="blue")
        self.label.pack(pady=20)

    def load_songs(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.playlist = [os.path.join(folder_path, f)
                             for f in os.listdir(folder_path) if f.endswith(".mp3")]
            if self.playlist:
                self.current_index = 0
                self.label.config(text=f"Loaded {len(self.playlist)} songs")
            else:
                messagebox.showerror("Error", "No MP3 files found in folder")

    def play_song(self):
        if self.playlist:
            mixer.music.load(self.playlist[self.current_index])
            mixer.music.play()
            song_name = os.path.basename(self.playlist[self.current_index])
            self.label.config(text=f"Playing: {song_name}")
        else:
            messagebox.showerror("Error", "Load songs first")

    def pause_resume(self):
        if mixer.music.get_busy():
            if not self.is_paused:
                mixer.music.pause()
                self.label.config(text="Paused")
                self.is_paused = True
            else:
                mixer.music.unpause()
                song_name = os.path.basename(self.playlist[self.current_index])
                self.label.config(text=f"Playing: {song_name}")
                self.is_paused = False

    def next_song(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play_song()

    def previous_song(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play_song()


# main
if __name__ == "__main__":
    root = tk.Tk()
    app = MediaPlayer(root)
    root.mainloop()

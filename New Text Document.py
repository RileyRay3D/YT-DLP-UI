import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Function to read config file
def read_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            name, value = line.strip().split('=')
            config[name] = value
    return config

# Function to download video
def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return

    format_option = format_var.get()
    yt_dlp_path = config['yt_dlp_path']
    download_dir = config['download_dir']
    ffmpeg_path = config['ffmpeg_path']
    os.makedirs(download_dir, exist_ok=True)

    if format_option == "mp4":
        cmd = f'"{yt_dlp_path}" -o "{download_dir}/%(title)s.%(ext)s" {url}'
    elif format_option == "mp3":
        cmd = f'"{yt_dlp_path}" -x --audio-format mp3 --ffmpeg-location "{ffmpeg_path}" -o "{download_dir}/%(title)s.%(ext)s" {url}'

    try:
        subprocess.run(cmd, check=True, shell=True)
        messagebox.showinfo("Success", "Download completed successfully")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to download")

# Get the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Read the config file
config_path = os.path.join(script_dir, 'config.txt')
config = read_config(config_path)

# Create the main window
root = tk.Tk()
root.title("yt-dlp GUI")

# URL entry
tk.Label(root, text="URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Format option
format_var = tk.StringVar(value="mp4")
tk.Radiobutton(root, text="MP4", variable=format_var, value="mp4").grid(row=1, column=0, padx=10, pady=10)
tk.Radiobutton(root, text="MP3", variable=format_var, value="mp3").grid(row=1, column=1, padx=10, pady=10)

# Download button
download_button = tk.Button(root, text="Download", command=download_video)
download_button.grid(row=2, columnspan=2, pady=20)

# Run the application
root.mainloop()

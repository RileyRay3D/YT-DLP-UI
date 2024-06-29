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

# Function to write config file
def write_config(file_path, config):
    with open(file_path, 'w') as file:
        for name, value in config.items():
            file.write(f"{name}={value}\n")

# Function to download video
def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return

    format_option = format_var.get()
    yt_dlp_path = yt_dlp_path_entry.get()
    download_dir = download_dir_entry.get()
    ffmpeg_path = ffmpeg_path_entry.get()
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

# Function to save configurations
def save_config():
    config['yt_dlp_path'] = yt_dlp_path_entry.get()
    config['download_dir'] = download_dir_entry.get()
    config['ffmpeg_path'] = ffmpeg_path_entry.get()
    write_config(config_path, config)
    messagebox.showinfo("Success", "Configurations saved successfully")

# Get the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Read the config file
config_path = os.path.join(script_dir, 'config.txt')
config = read_config(config_path)

# Create the main window
root = tk.Tk()
root.title("yt-dlp GUI")

# Configure the grid to make the second column expandable
root.grid_columnconfigure(1, weight=1)

# URL entry
tk.Label(root, text="URL:").grid(row=0, column=0, padx=10, pady=1, sticky="e")
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="we")

# Format option
format_var = tk.StringVar(value="mp4")
tk.Radiobutton(root, text="MP4", variable=format_var, value="mp4").grid(row=1, column=0, padx=10, pady=1, sticky="w")
tk.Radiobutton(root, text="MP3", variable=format_var, value="mp3").grid(row=1, column=1, padx=10, pady=1, sticky="w")

# yt-dlp path entry
tk.Label(root, text="yt-dlp Path:").grid(row=2, column=0, padx=10, pady=1, sticky="e")
yt_dlp_path_entry = tk.Entry(root, width=50)
yt_dlp_path_entry.grid(row=2, column=1, padx=10, pady=1, sticky="we")
yt_dlp_path_entry.insert(0, config['yt_dlp_path'])

# Download directory entry
tk.Label(root, text="Download Directory:").grid(row=3, column=0, padx=10, pady=1, sticky="e")
download_dir_entry = tk.Entry(root, width=50)
download_dir_entry.grid(row=3, column=1, padx=10, pady=10, sticky="we")
download_dir_entry.insert(0, config['download_dir'])

# ffmpeg path entry
tk.Label(root, text="ffmpeg Path:").grid(row=4, column=0, padx=10, pady=1, sticky="e")
ffmpeg_path_entry = tk.Entry(root, width=50)
ffmpeg_path_entry.grid(row=4, column=1, padx=10, pady=10, sticky="we")
ffmpeg_path_entry.insert(0, config['ffmpeg_path'])

# Save config button
save_config_button = tk.Button(root, text="Save Config", command=save_config)
save_config_button.grid(row=5, column=0, padx=10, pady=1, sticky="e")

# Download button
download_button = tk.Button(root, text="Download", command=download_video)
download_button.grid(row=5, column=1, padx=10, pady=1, sticky="w")

# Run the application
root.mainloop()

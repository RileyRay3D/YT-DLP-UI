import customtkinter as ctk
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

# Toggle visibility of yt-dlp and ffmpeg path entries
def toggle_settings():
    if settings_frame.winfo_viewable():
        settings_frame.grid_remove()
    else:
        settings_frame.grid()

# Get the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Read the config file
config_path = os.path.join(script_dir, 'config.txt')
config = read_config(config_path)

# Create the main window
root = ctk.CTk()
root.title("yt-dlp GUI")

# Disable vertical resizing
root.resizable(width=True, height=False)

# Configure the grid to make the second column expandable
root.grid_columnconfigure(1, weight=1)

# URL entry
ctk.CTkLabel(root, text="URL:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
url_entry = ctk.CTkEntry(root, width=400)
url_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="we")

# Format options label
ctk.CTkLabel(root, text="Format:").grid(row=1, column=0, padx=10, pady=5, sticky="e")

# Format option
format_var = ctk.StringVar(value="mp4")
ctk.CTkRadioButton(root, text="MP4", variable=format_var, value="mp4").grid(row=1, column=1, padx=(10, 5), pady=5, sticky="w")
ctk.CTkRadioButton(root, text="MP3", variable=format_var, value="mp3").grid(row=1, column=1, padx=(100, 10), pady=5, sticky="w")

# Download directory entry
ctk.CTkLabel(root, text="Downloads:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
download_dir_entry = ctk.CTkEntry(root, width=400)
download_dir_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="we")
download_dir_entry.insert(0, config['download_dir'])

# Collapsible settings frame
settings_frame = ctk.CTkFrame(root)
settings_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="we")

# yt-dlp path entry
ctk.CTkLabel(settings_frame, text="yt-dlp Path:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
yt_dlp_path_entry = ctk.CTkEntry(settings_frame, width=400)
yt_dlp_path_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="we")
yt_dlp_path_entry.insert(0, config['yt_dlp_path'])

# ffmpeg path entry
ctk.CTkLabel(settings_frame, text="ffmpeg Path:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
ffmpeg_path_entry = ctk.CTkEntry(settings_frame, width=400)
ffmpeg_path_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="we")
ffmpeg_path_entry.insert(0, config['ffmpeg_path'])

# Initially hide the settings frame
settings_frame.grid_remove()

# Buttons frame
buttons_frame = ctk.CTkFrame(root)
buttons_frame.grid(row=4, column=0, columnspan=3, pady=5, sticky="we")

# Configure grid columns for buttons frame to make buttons stretch
buttons_frame.grid_columnconfigure(0, weight=1)
buttons_frame.grid_columnconfigure(1, weight=1)
buttons_frame.grid_columnconfigure(2, weight=1)

# Toggle settings button
toggle_settings_button = ctk.CTkButton(buttons_frame, text="Toggle Settings", command=toggle_settings)
toggle_settings_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

# Save config button
save_config_button = ctk.CTkButton(buttons_frame, text="Save Config", command=save_config)
save_config_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

# Download button
download_button = ctk.CTkButton(buttons_frame, text="Download", command=download_video)
download_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

# Run the application
root.mainloop()

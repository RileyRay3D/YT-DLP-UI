# yt_dlp_logic.py
import subprocess
import os
import threading

def get_yt_dlp_path(yt_dlp_path):
    # If the path is a directory, append yt-dlp.exe to it
    if os.path.isdir(yt_dlp_path):
        yt_dlp_path = os.path.join(yt_dlp_path, "yt-dlp.exe")
    return yt_dlp_path

# Read config file
def read_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            name, value = line.strip().split('=')
            config[name] = value
    return config

# Write config file
def write_config(file_path, config):
    with open(file_path, 'w') as file:
        for name, value in config.items():
            file.write(f"{name}={value}\n")

def run_command(cmd, output_callback, status_callback):
    def command_thread():
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in iter(process.stdout.readline, ''):
            output_callback(line)
        for line in iter(process.stderr.readline, ''):
            output_callback(line)
        process.stdout.close()
        process.stderr.close()
        process.wait()
        if process.returncode == 0:
            status_callback("Success: Download completed successfully", "green")
        else:
            status_callback("Error: Failed to download", "red")

    threading.Thread(target=command_thread).start()

def download_start(config, url, format_option, audio_quality, output_callback, status_callback):
    if not url:
        status_callback("Error: Please enter a URL", "red")
        return

    yt_dlp_path = get_yt_dlp_path(config['yt_dlp_path'])
    download_dir = config['download_dir']
    ffmpeg_path = config['ffmpeg_path']
    os.makedirs(download_dir, exist_ok=True)

    if format_option == "mp4":
        cmd = f'"{yt_dlp_path}" -o "{download_dir}/%(title)s.%(ext)s" {url}'
    elif format_option == "mp3":
        cmd = f'"{yt_dlp_path}" -x --audio-format mp3 --ffmpeg-location "{ffmpeg_path}" -o "{download_dir}/%(title)s.%(ext)s" {url}'
        if audio_quality == "Auto (Best Availible)":
            cmd += f' --audio-quality 0'
        elif audio_quality != "Auto":
            cmd += f' --audio-quality {audio_quality}'

    run_command(cmd, output_callback, status_callback)

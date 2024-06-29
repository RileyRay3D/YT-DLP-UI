
import customtkinter as ctk
import os
import threading
from yt_dlp_downloader import read_config, write_config, download_start

# Initialize timer
status_timer = None

# Show status message and manage the timer
def show_status(message, color):
    global status_timer
    if status_timer is not None:
        status_timer.cancel()
    status_button.configure(text=message, fg_color=color, text_color="white", state="normal")
    status_button.grid()
    root.update_idletasks()
    root.geometry(f"{root.winfo_width()}x{root.winfo_reqheight()}")
    status_timer = threading.Timer(10, hide_status)
    status_timer.start()

def hide_status():
    global status_timer
    status_button.grid_remove()
    status_button.configure(state="disabled")
    root.update_idletasks()
    root.geometry(f"{root.winfo_width()}x{root.winfo_reqheight()}")
    status_timer = None

# Save configurations to config.txt
def save_config():
    config['yt_dlp_path'] = yt_dlp_path_entry.get()
    config['download_dir'] = download_dir_entry.get()
    config['ffmpeg_path'] = ffmpeg_path_entry.get()
    write_config(config_path, config)
    show_status("Success: Configurations saved successfully", "teal")

# Toggle visibility of settings frame
def toggle_settings():
    settings_frame.grid_remove() if settings_frame.winfo_viewable() else settings_frame.grid()
    root.update_idletasks()
    root.geometry(f"{root.winfo_width()}x{root.winfo_reqheight()}")

# Toggle visibility of debug window
def toggle_debug():
    output_text.grid_remove() if output_text.winfo_viewable() else output_text.grid()
    root.update_idletasks()
    root.geometry(f"{root.winfo_width()}x{root.winfo_reqheight()}")

# Update the output text widget
def output_callback(line):
    output_text.insert(ctk.END, line)
    output_text.see(ctk.END)


def status_callback(message, color):
    show_status(message, color)

def paste_clipboard():
    try:
        clipboard_content = root.clipboard_get()
        url_entry.delete(0, ctk.END)
        url_entry.insert(0, clipboard_content)
    except Exception as e:
        status_callback("Error: Unable to paste from clipboard", "red")


# Initialize the main window
def init_main_window():
    global root, url_entry, format_var, download_dir_entry, yt_dlp_path_entry, ffmpeg_path_entry, audio_quality_var, settings_frame, buttons_frame, output_text, status_button

    root = ctk.CTk()
    root.title("yt-dlp GUI")
    root.resizable(width=True, height=True)
    root.minsize(width=400, height=160)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(5, weight=1)

    # Create URL entry
    #create_label(root, "URL:", 0, 0, "e")
    paste_button = ctk.CTkButton(root, text="Paste URL:", command=paste_clipboard, width=80)
    paste_button.grid(row=0, column=0, padx=5, pady=5)
    url_entry = create_entry(root, 0, 1, 2)

    #paste_button = ctk.CTkButton(root, text="Paste", command=paste_clipboard, width=50)
    #paste_button.grid(row=0, column=2, padx=10, pady=5)

    # Create format options
    create_label(root, "Format:", 1, 0, "e")
    format_var = ctk.StringVar(value="mp4")
    create_radiobutton(root, "MP4", format_var, "mp4", 1, 1, "w", (10, 5))
    create_radiobutton(root, "MP3", format_var, "mp3", 1, 1, "w", (100, 10))

    # Create download directory entry
    create_label(root, "Downloads:", 2, 0, "e")
    download_dir_entry = create_entry(root, 2, 1, 2)
    download_dir_entry.insert(0, config['download_dir'])

    # Create settings frame
    settings_frame = create_frame(root, 3, 0, 3)
    create_label(settings_frame, "yt-dlp Path:", 0, 0, "e")
    yt_dlp_path_entry = create_entry(settings_frame, 0, 1, 2)
    yt_dlp_path_entry.insert(0, config['yt_dlp_path'])

    create_label(settings_frame, "ffmpeg Path:", 1, 0, "e")
    ffmpeg_path_entry = create_entry(settings_frame, 1, 1, 2)
    ffmpeg_path_entry.insert(0, config['ffmpeg_path'])

    create_label(settings_frame, "Audio Quality:", 2, 0, "e")
    audio_quality_var = ctk.StringVar(value="default")
    audio_quality_menu = ctk.CTkOptionMenu(settings_frame, variable=audio_quality_var, values=["default", "192K", "256K", "320K"])
    audio_quality_menu.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="we")

    toggle_debug_button = ctk.CTkButton(settings_frame, text="Toggle Debug Window", command=toggle_debug, fg_color="teal", hover_color="darkslategrey")
    toggle_debug_button.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="we")
    settings_frame.grid_remove()

    # Create buttons frame
    buttons_frame = create_frame(root, 4, 0, 3)
    buttons_frame.grid_columnconfigure(0, weight=1)
    buttons_frame.grid_columnconfigure(1, weight=1)
    buttons_frame.grid_columnconfigure(2, weight=1)
    
    create_button(buttons_frame, "Settings", toggle_settings, 0, 0)
    create_button(buttons_frame, "Save Config", save_config, 0, 1)
    create_button(buttons_frame, "Download", lambda: download_start(config, url_entry.get(), format_var.get(), audio_quality_var.get(), output_callback, status_callback), 0, 2)

    # Create output text widget
    output_text = ctk.CTkTextbox(root, width=600, height=100)
    output_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    # Create status button
    status_button = ctk.CTkButton(buttons_frame, text="", fg_color="gray", state="disabled", command=hide_status)
    status_button.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
    status_button.grid_remove()

# Helper functions to create widgets
def create_label(parent, text, row, column, sticky):
    label = ctk.CTkLabel(parent, text=text)
    label.grid(row=row, column=column, padx=5, pady=5, sticky=sticky)
    return label

def create_entry(parent, row, column, columnspan):
    entry = ctk.CTkEntry(parent, width=400)
    entry.grid(row=row, column=column, columnspan=columnspan, padx=5, pady=5, sticky="we")
    return entry

def create_radiobutton(parent, text, variable, value, row, column, sticky, padx):
    radiobutton = ctk.CTkRadioButton(parent, text=text, variable=variable, value=value)
    radiobutton.grid(row=row, column=column, padx=padx, pady=5, sticky=sticky)
    return radiobutton

def create_frame(parent, row, column, columnspan):
    frame = ctk.CTkFrame(parent)
    frame.grid(row=row, column=column, columnspan=columnspan, padx=10, pady=5, sticky="we")
    frame.grid_columnconfigure(1, weight=1)
    return frame

def create_button(parent, text, command, row, column):
    button = ctk.CTkButton(parent, text=text, command=command)
    button.grid(row=row, column=column, padx=5, pady=5, sticky="ew")
    return button

# Main
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.txt')
    config = read_config(config_path)
    init_main_window()
    root.mainloop()

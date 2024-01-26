import customtkinter as ctk
from pytube import YouTube
# from tkinter import ttk
# import os

# Single video download
def download_video():
    if tabview.get() == "Video":
        option = res_box.get()
        path = 'Downloaded Videos'
    else:
        option = audio_box.get()
        path = 'Downloaded Audio'
    progress_bar.set(0)
    progress_label.pack(pady=10, padx=5)
    progress_bar.pack(pady=10, padx=5)
    status_label.pack(pady=10, padx=5)

    try:
        if tabview.get() == "Video":
            stream = v_streams.filter(res=option).first()
        else:
            stream = a_streams.filter(abr=option).first()
        stream.download(output_path=path)
        status_label.configure(text=f'Downloaded "{yt.title}"', text_color='white', fg_color='green')
    except Exception as e:
        status_label.configure(text=f"Error: {str(e)}", text_color='white', fg_color='red')

# Custom progress bar function
def prog_func(stream, chunk, bytes_remaining):
    video_size = stream.filesize
    bytes_downloaded = video_size - bytes_remaining
    percentage = bytes_downloaded / video_size * 100

    progress_label.configure(text=str(int(percentage)) + '%')
    progress_label.update()
    progress_bar.set(percentage / 100)

# Show available formats
def show_options():        
    tabview.pack(pady=10, padx=5)
    resolutions = []
    bitrates = []
    global v_streams, a_streams, yt
    yt = YouTube(entry_url.get(), on_progress_callback=prog_func)

    v_streams = yt.streams.filter(progressive=True)
    a_streams = yt.streams.filter(mime_type='audio/webm')

    for stream in v_streams:
        resolutions.append(stream.resolution)
    for stream in a_streams:
        bitrates.append(stream.abr)
    
    # chosen_res = ctk.StringVar()
    res_box.configure(values=resolutions)
    res_box.set(resolutions[-1])
    audio_box.configure(values=bitrates)
    audio_box.set(bitrates[-1])
    
    dl_button = ctk.CTkButton(content_frame, text="Download", command=download_video)
    dl_button.pack(pady=10, padx=5)

# Root window creation
root = ctk.CTk()
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
root.title("Best Youtube Downloader Ever")

# Window size restrictions
root.geometry("800x600")
root.minsize(800, 600)
root.maxsize(1080, 720)

# Content Frame
content_frame = ctk.CTkFrame(root)
content_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

# URL Entry label
url_label = ctk.CTkLabel(content_frame, text="Enter video link")
entry_url = ctk.CTkEntry(content_frame, width=400, height=40)
url_label.pack(pady=10, padx=5)
entry_url.pack(pady=10, padx=5)

#Video and Audio tabs
tabview = ctk.CTkTabview(content_frame, width=250, height=100)
tabview.add("Video")
tabview.add("Audio")

# Download button
check_button = ctk.CTkButton(content_frame, text="Show Options", command=show_options)
check_button.pack(pady=10, padx=5)

# Resolution&Audio Lists
res_box = ctk.CTkOptionMenu(tabview.tab("Video"))
res_box.pack(pady=10, padx=5)
audio_box = ctk.CTkOptionMenu(tabview.tab("Audio"))
audio_box.pack(pady=10, padx=5)

# Progress bar
progress_label = ctk.CTkLabel(content_frame, text="0%")
progress_bar = ctk.CTkProgressBar(content_frame, width=400)

# Status label
status_label = ctk.CTkLabel(content_frame, text="Downloading")

# App execution
root.mainloop()


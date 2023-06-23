import tkinter as tk
from tkinter import ttk
from downloader import YTDownloader
from queue import Queue
import os
from random import randint
from datetime import datetime
from ttkthemes import ThemedStyle
import threading

class Downloader:
    def __init__(self):
        working_directory = os.getcwd()
        files = os.listdir()
        hasDownloads = 'downloads' in files
        self.download_directory = working_directory + "/downloads/"

        # TODO check if downloads folder exists

        if not hasDownloads:
            print("downloads folder not found, creating folder.")
            os.mkdir('downloads')
            hasDownloads = 'downloads' in files
        else: 
            print("downloads folder found.")
            os.chdir(self.download_directory)
            files = os.listdir()
            for file in files:
                pass


        self.data = [
            # (index, song, date, size, link)
        ]
        self.iids = ()

        self.app = tk.Tk()
        self.app.geometry("800x540")

        self.app.rowconfigure(0, weight=1)
        self.app.rowconfigure(1, weight=1)
        self.app.rowconfigure(2, weight=1)

        # create a frame at the top to fill the space in the x axis
        self.titleframe = tk.Frame(self.app)
        self.titleframe.pack(side="top", fill="x")


        self.label = tk.Label(self.titleframe, text='YouTube Audio Downloader', font=('Arial',18))
        self.label.grid(
            row=0,
            column=0,
            pady=5, 
            padx=13,
            sticky="w")
        

        # download bar which is rendered to the title frame
        self.downloadbar = ttk.Progressbar(
            self.titleframe, 
            orient=tk.HORIZONTAL,
            length=200, 
            mode="determinate", 
            style="TProgressbar")
        
        self.downloadbar.grid(
            row=0,
            column=1,
            pady=10, 
            padx=14,
            sticky="e")

        self.titleframe.grid_columnconfigure(0, weight=1)
        self.titleframe.grid_columnconfigure(1, weight=1)

        # frame for link entry field and download button
        self.linkframe = tk.Frame(self.app)
        self.linkframe.pack(fill="x",pady=6,padx=10)


        self.linkentry = tk.Entry(
            self.linkframe,
            width=60,
            font=('Arial',15))
        self.linkentry.grid(row=0,
                            column=0,
                            sticky="ew",
                            padx=3)

        self.formatcombovar = tk.StringVar()
        self.formatcombovar.set("mp3")
        self.formatcombo = ttk.Combobox(
            self.linkframe, 
            textvariable=self.formatcombovar, 
            width=4, 
            font=('Arial', 15),
            values=('mp3', 'wav', 'm4a'),
            state="readonly")
        self.formatcombo.grid(row=0,column=1,padx=5,sticky="e")

        self.submitbtn = tk.Button(
            self.linkframe,
            text="Download",
            font=('Arial', 15), 
            command=lambda: threading.Thread(
                target=self.download_and_save
                ).start())
        self.submitbtn.grid(
            row=0,
            column=2,
            padx=5,
            sticky="e")

        self.linkframe.grid_columnconfigure(0, weight=1)
        self.linkframe.grid_columnconfigure(1, weight=1)
        self.linkframe.grid_columnconfigure(2, weight=1)


        self.tree = ttk.Treeview(self.app,height=22)

        # define columns
        self.tree['columns'] = ("File", "Date Downloaded", "Size", "Link")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("File", anchor=tk.W, width=200)
        self.tree.column("Date Downloaded", anchor=tk.CENTER, width=180)
        self.tree.column("Size", anchor=tk.CENTER, width=50)
        self.tree.column("Link", anchor=tk.CENTER, width=340)

        # create the headings
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("File", text="File", anchor=tk.W)
        self.tree.heading("Date Downloaded", text="Date Downloaded", anchor=tk.CENTER)
        self.tree.heading("Size", text="Size", anchor=tk.CENTER)
        self.tree.heading("Link", text="Link", anchor=tk.CENTER)

        
        self.update_data()

        self.tree.pack(pady=5)

        self.start()
    
    def update_data(self):
        count = 0
        for record in self.data:
            self.tree.insert(
                parent='', 
                index=tk.END, 
                iid=str(count), 
                text="", 
                values=(record[0], record[1], record[2]))
            count += 1

    def download_and_save(self):
        self.submitbtn.config(state=tk.DISABLED)
        url = self.linkentry.get() 
        file_format = self.formatcombovar.get()

        # create the youtube instance
        yt = YTDownloader(url, self.on_progress, file_format) 
        yt_title = yt.get_title()
        yt.download_audio(self.download_directory)

        now = datetime.now()
        format = '%Y-%m-%d %H:%M %p'
        downloaded_time = now.strftime("%B %d, %Y, %I:%M %p")

        #yt_filename = yt.filename
        yt_size = yt.size_in_mb 

        t = (yt_title, downloaded_time,yt_size, url)

        rand_iid = randint(0, 32000)

        if rand_iid in self.iids:
            while rand_iid in self.iids:
                rand_iid = randint(0, 32000)

        self.tree.insert(parent='', index=0, iid=str(rand_iid), text="", values=t)

        print(f'{url} downloaded')
        self.data.insert(0, t)
        self.submitbtn.config(state=tk.NORMAL)

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = (bytes_downloaded / total_size) * 100
        self.downloadbar['value'] = percentage_of_completion
        self.app.update_idletasks()


    def start(self):
        self.app.mainloop()

Downloader()
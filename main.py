import tkinter as tk
from tkinter import ttk
from downloader import YTDownloader
from queue import Queue
import os
import json
from random import randint
from datetime import datetime
import threading

class Downloader:
    def __init__(self):
        self.LOG_FILE = "log.json"
        self.download_directory = os.path.join(os.getcwd(), 'downloads')
        self.data = [
            # (index, song, date, size, link)
        ]
        self.iids = []
        self.app = tk.Tk()
        self.app.geometry("800x540")
        self.app.resizable(False, False)
        self.app.title("YouTube Audio Downloader")

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
        '''self.downloadbar = ttk.Progressbar(
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
            sticky="e")'''

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
        if os.path.exists(self.LOG_FILE):
                print("log.json found, loading logs")
                with open(self.LOG_FILE, 'r') as file:
                    lines = file.readlines()
                
                logs = [json.loads(line) for line in lines]
                logs.sort(key= lambda x: x['timestamp'])

                for log in logs:
                    self.iids.append(log['index'])
                    self.tree.insert("", 0, iid=log['index'], values=(log['filename'], log['formatted_timestamp'], log['size'], log['link']))

    def add_data(self, metadata, timestamp):
        # metadata = (filename, date, size, link)

        # generate random id for the treeview, idk why needed.
        rand_iid = randint(0, 32000)
        if rand_iid in self.iids:
            while rand_iid in self.iids:
                rand_iid = randint(0, 32000)

        log_entry = {
            'index': rand_iid,
            'filename': metadata[0],
            'formatted_timestamp': metadata[1],
            'size': metadata[2],
            'link': metadata[3],
            'timestamp': timestamp.isoformat()

        }

        with open(self.LOG_FILE, 'a') as file:
            json.dump(log_entry, file)
            file.write('\n')

        self.tree.insert(parent='', index=0, iid=str(rand_iid), text="", values=metadata)
        self.data.insert(0, metadata)
        self.iids.append(rand_iid)



    def download_and_save(self):
        self.submitbtn.config(state=tk.DISABLED)
        
        yt_video_url = self.linkentry.get() 
        user_file_format = self.formatcombovar.get()

        # create the youtube instance
        yt = YTDownloader(yt_video_url, user_file_format) 

        # this is sooo janky dude please dont judge but this is how i made it work, deal with it.
        filename = yt.download_audio(self.download_directory)
        timestamp = datetime.now()

        # collect video meta data for saving.
        yt_download_time = timestamp.strftime("%B %d, %Y, %I:%M %p")
        yt_filedata = (filename, yt_download_time, yt.size_in_mb , yt_video_url)

        # add the data to the treeview
        self.add_data(yt_filedata, timestamp)

        print(f'{yt_video_url} downloaded')
        self.submitbtn.config(state=tk.NORMAL)


    def start(self):
        self.app.mainloop()

Downloader()
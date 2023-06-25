from pytube import YouTube
from pydub import AudioSegment
import os


class YTDownloader:
    def __init__(self, url, file_format="mp3"):
        self.url = url
        self.yt = YouTube(url)
        self.filename = ""
        self.file_format = file_format
        self.size_in_mb = 0
        self.file_title = self.yt.title

    def get_exact_filesize_in_mb(self, filename):
        # Get file size in bytes
        file_size_bytes = os.path.getsize(filename)
        # Convert to MB
        file_size_mb = file_size_bytes / (1024 * 1024)
        return round(file_size_mb, 1)
    
    def download_audio(self, download_directory):
        os.makedirs(download_directory, exist_ok=True)  # Ensure the directory exists
        try:
            # filter out the audio streams from yt.stream
            audio_streams = self.yt.streams.filter(only_audio=True)

            # check if the audio streams exist
            if len(audio_streams) == 0:
                print(f'No audio streams available for: {self.url}')
                return

            # select first audio stream
            audio = audio_streams[0]
            print("Downloading audio")
            default_filename = audio.download(output_path=download_directory)
            self.filename = os.path.basename(default_filename)

            if self.file_format and self.file_format not in ['mp3', 'wav', 'm4a']:
                print(f'Invalid file format: {self.file_format}, defaulting to original format')
            elif self.file_format and self.file_format != audio.subtype:
                new_filename = os.path.join(download_directory, os.path.splitext(self.filename)[0] + '.' + self.file_format)
                AudioSegment.from_file(default_filename).export(new_filename, format=self.file_format)
                os.remove(default_filename)
                self.filename = os.path.basename(new_filename)

            self.size_in_mb = str(self.get_exact_filesize_in_mb(os.path.join(download_directory, self.filename))) + " MB"

            return self.filename
        
        except Exception as e:
            print(f'Error: {str(e)}')
    
        

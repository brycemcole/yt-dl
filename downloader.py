from pytube import YouTube
from pydub import AudioSegment
import os


class YTDownloader:
    def __init__(self, url, on_progress, file_format="mp3"):
        self.url = url
        self.yt = YouTube(url)
        self.filename = ""
        self.file_format = file_format
        self.size_in_mb = 0
    
    def download_audio(self, download_directory):
        try:
            os.chdir(download_directory)
            # filter out the audio streams from yt.stream
            audio_streams = self.yt.streams.filter(only_audio=True)

            # check if the audio streams exist
            if len(audio_streams) == 0:
                print(f'No audio streams available for: {self.url}')
                return

            # select first audio stream
            audio = audio_streams[0]
            
            
            self.size_in_mb = round(audio.filesize / (1024 * 1024), 1)

            print("Downloading audio")
            audio.download(output_path=download_directory)

            default_filename = download_directory + audio.default_filename

            new_filename = os.path.splitext(default_filename)[0] + ".mp3"
            os.rename(default_filename, new_filename)

            if self.file_format == "wav":
                print("converting to wav file")
                input_audio = AudioSegment.from_mp3(new_filename)
                input_audio.export(new_filename, format="wav")
                new_filename = os.path.splitext(new_filename)[0] + ".wav"
            elif self.file_format == "m4a":
                input_audio = AudioSegment.from_mp3(new_filename)
                input_audio.export(new_filename, format="m4a")
                new_filename = os.path.splitext(new_filename)[0] + ".m4a"
            
            self.filename = new_filename
            print(f"Audio successfully downloaded as {new_filename}")
        
        except Exception as e:
            print(f'Error: {str(e)}')
    
    def get_title(self):
        return self.yt.title
        

import os
import shutil
import watchdog #Watchdog lib is essential, it tracks changes or events in any files/folders
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
import logging

target_dir = 'C:/Users/theme/Downloads'
image_dir = 'C:/Users/theme/OneDrive/Desktop/moving_files/image'
music_dir = 'C:/Users/theme/OneDrive/Desktop/moving_files/music'
video_dir = 'C:/Users/theme/OneDrive/Desktop/moving_files/video'
doc_dir = 'C:/Users/theme/OneDrive/Desktop/moving_files/textdocuments'

image_ext = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
video_ext =  [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
doc_ext = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]
audio_ext = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# list of extensions assumed for files we download



class LoggingEventHandler(FileSystemEventHandler):
    def on_modified(self,event):
        with os.scandir(target_dir) as downloads:

            for down in downloads:
                name = down.name
                # downloads is parent file, hence when you just print downloads it gives a generic
        # description as output. If we wanna extract all the files from the os.scandir of target dir, thnhen we gotta
        # iterate inside downloads. Printing that will you the files inside downloads. And .name will specifically extract the
        # names
                self.check_audio_files(down, name)
                self.check_document_files(down, name)
                self.check_video_files(down, name)
                self.check_image_files(down, name)
    def check_audio_files(self,down,name):
        for ext in audio_ext:
            if name.endswith(ext):
                dest = music_dir
                shutil.move(down.path,os.path.join(dest,name)) # Move function likely needs a full path in destination
                 #so just putting the destination directory as the path won't cut it. You'll need to attach the file
                # that you're moving to the directory along with the directory path.
                logging.info(f'Moved Audio file from{target_dir} to {dest}')
    def check_document_files(self, down, name):
        for ext in doc_ext:
            if name.endswith(ext):
                dest = doc_dir
                shutil.move(down.path, os.path.join(dest, name))
                logging.info(f'Moved Document file from{target_dir} to {dest}')
    def check_video_files(self, down,name):
        for ext in video_ext:
            if name.endswith(ext):
                dest = video_dir
                shutil.move(down.path, os.path.join(dest, name))
                logging.info(f'Moved Video file from{target_dir} to {dest}')
    def check_image_files(self, down, name):
        for ext in image_ext:
            if name.endswith(ext):
                dest = image_dir
                shutil.move(down.path, os.path.join(dest, name))
                logging.info(f'Moved Image file from{target_dir} to {dest}')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = target_dir
    event_handler = LoggingEventHandler() #create event handler instance
    observer = Observer() #create observer instance
    observer.schedule(event_handler, path, recursive=True) # .schedule configures the behavior of the observer instance
    # we're setting the obserer to use the event_handler to manage system file events and to monitor changes in taregt dir
    # recursive means it's set to track changes in all the subdirectories of target_dir
    observer.start()
    try:
        while True: # creates an infinite loop that adds a 1 second pause after each iteration
            time.sleep(1)
    except KeyboardInterrupt: # adding an exception that the loop stops functioning only when the user presses Ctrl + C
        # as a keyboard interrupt.
        observer.stop()
    observer.join() # This function ensures that the loop terminates only when the observer has finished completely.
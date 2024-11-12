import time, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            print(f"Directory modified: {event.src_path}")
        else:
            print(f"File modified: {event.src_path}")

    def on_created(self, event):
        if event.is_directory:
            print(f"Directory created: {event.src_path}")
        else:
            print(f"File created: {event.src_path}")

    def on_deleted(self, event):
        if event.is_directory:
            print(f"Directory deleted: {event.src_path}")
        else:
            print(f"File deleted: {event.src_path}")

    def on_moved(self, event):
        if event.is_directory:
            print(f"Directory moved: {event.src_path} -> {event.dest_path}")
        else:
            print(f"File moved: {event.src_path} -> {event.dest_path}")

def monitor_directory(path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)  # Keeps the script running to monitor changes
    except KeyboardInterrupt:
        observer.stop()
        print("Monitoring stopped")
    observer.join()

if __name__ == "__main__":
    folder_path = os.path.expandvars(r"C:\Users\%username%\temp")  # Replace with your folder path
    monitor_directory(folder_path)

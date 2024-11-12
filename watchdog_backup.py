import logging
from backuperV2 import main_task, root_copy_from

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta
import json, time, os

timestamp_file = "last_operation_time.json"

backup_every_h = 0
backup_every_m = 1
backup_every_s = 0

def get_last_operation_time():
    try:
        with open(timestamp_file, "r") as f:
            data = json.load(f)
            return datetime.fromisoformat(data["last_operation_time"])
    except (FileNotFoundError, KeyError, ValueError):
        return None

def save_last_operation_time():
    with open(timestamp_file, "w") as f:
        json.dump({"last_operation_time": datetime.now().isoformat()}, f)

def perform_operation():
    main_task()
    save_last_operation_time()

class MyHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        super().__init__()
        self.last_op_time = get_last_operation_time()
        
    def on_modified(self, event):
        self.handle_event(event)

    def on_created(self, event):
        self.handle_event(event)

    def on_deleted(self, event):
        self.handle_event(event)

    def on_moved(self, event):
        self.handle_event(event)

    def handle_event(self, event):
        logging.debug(f"--> Detected change: {event.src_path}")
        
        # last_op_time = get_last_operation_time()
        now = datetime.now()

        # If the last operation time is not set or 1 hour has passed since the last operation
        if self.last_op_time is None or now - self.last_op_time >= timedelta(hours=backup_every_h, minutes=backup_every_m, seconds=backup_every_s):
            logging.debug(f"----> Performing backup operation...  delta: {now - self.last_op_time} ")
            perform_operation()
            self.last_op_time =datetime.now()#.isoformat()
        else:
            logging.debug(f"--> Operation skipped. Only {now - self.last_op_time} has passed since last operation.")

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
        logging.info("Monitoring stopped")
    observer.join()


if __name__ == "__main__":
    folder_path = os.path.expandvars(root_copy_from)  # Replace with your folder path
    monitor_directory(folder_path)

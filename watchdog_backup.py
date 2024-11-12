import logging
import threading
import app_logging

from backuperV2 import main_task, root_copy_from

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta
import json, time, os

timestamp_file = "last_operation_time.json"

backup_every_h = 0
backup_every_m = 10
backup_every_s = 0
tot_backup_every_s = (backup_every_h*3600) + (backup_every_m*60) + backup_every_s

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


class MyHandler(FileSystemEventHandler):
    
    def perform_operation(self, trigger=None):
        if trigger != None: logging.info(F"----> Performing operation, trigger: {trigger}")
        main_task()
        save_last_operation_time()
        self.last_op_time =datetime.now()#.isoformat()

        
    def __init__(self) -> None:
        super().__init__()
        self.last_op_time = get_last_operation_time()
        self.timer_handle = None
        self.prev_call_time = 0
        self.prev_event = None
        self.cur_event = None
        
    def on_modified(self, event):
        self.handle_event(event)

    def on_created(self, event):
        self.handle_event(event)

    def on_deleted(self, event):
        self.handle_event(event)

    def on_moved(self, event):
        self.handle_event(event)

    def handle_event(self, event):
        self.prev_event = self.cur_event
        self.cur_event = event
        if time.time() - self.prev_call_time > 0.1 or self.prev_event != self.cur_event:
            self.prev_call_time = time.time()
            logging.debug(f"--> Detected change: {event.src_path}")
            
            now = datetime.now()

            if self.last_op_time is None or now - self.last_op_time >= timedelta(hours=backup_every_h, minutes=backup_every_m, seconds=backup_every_s):
                logging.debug(f"-----> Performing backup operation...  delta: {now - self.last_op_time} ")
                self.perform_operation()
            else:
                logging.debug(f"--> Operation skipped. Only {now - self.last_op_time} has passed since last operation.")
                if self.timer_handle:
                    logging.debug("--> Cancelling timer handle")
                    self.timer_handle.cancel()
                logging.debug("--> Setting delayed timer ")
                self.timer_handle = threading.Timer(tot_backup_every_s, lambda: self.perform_operation("delayed timer"))
                self.timer_handle.start()

def monitor_directory(path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    import msvcrt
    logging.info("Monitor started")
    try:
        while True:
            while msvcrt.kbhit():
                k = msvcrt.getch()
                if k == b'b' or k == b'B':
                    logging.info("----> b pressed, doing backup")
                    event_handler.perform_operation("key press")
                
            time.sleep(1)  # Keeps the script running to monitor changes
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Monitoring stopped")
    observer.join()


if __name__ == "__main__":
    folder_path = os.path.expandvars(root_copy_from)  # Replace with your folder path
    monitor_directory(folder_path)

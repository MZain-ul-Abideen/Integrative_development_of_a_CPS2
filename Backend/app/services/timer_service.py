import threading
import time

def start_timer(interval, callback):
    def timer_loop():
        while True:
            time.sleep(interval)
            callback()

    thread = threading.Thread(target=timer_loop)
    thread.daemon = True
    thread.start()
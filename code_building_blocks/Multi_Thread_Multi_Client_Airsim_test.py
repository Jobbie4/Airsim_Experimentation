import setup_path
import airsim
import pprint
import threading
import time
#Intended to test simple combinations of commands without injecting any thing else 

class RepeatThread:
    def __init__(self):

        self.image_callback_thread = threading.Thread(
            target=self.repeat_timer_image_callback, 
            args=(self.image_callback, 1),
        )
        self.odometry_callback_thread = threading.Thread(
            target=self.repeat_timer_odometry_callback,
            args=(self.odometry_callback, 0.5),
        )
        self.is_image_thread_active = False
        self.is_odometry_thread_active = False

    def repeat_timer_image_callback(self, task, period):
        while self.is_image_thread_active:
            task()
            time.sleep(period)

    def repeat_timer_odometry_callback(self, task, period):
        while self.is_odometry_thread_active:
            task()
            time.sleep(period)

    def image_callback(self):
        # get uncompressed fpv cam image
       print("called image function")
  

    def odometry_callback(self):
        print("called odometry function")
    
    def start_image_callback_thread(self):
        if not self.is_image_thread_active:
            self.is_image_thread_active = True
            self.image_callback_thread.start()
            print("Started image callback thread")

    def stop_image_callback_thread(self):
        if self.is_image_thread_active:
            self.is_image_thread_active = False
            self.image_callback_thread.join()
            print("Stopped image callback thread.")

    def start_odometry_callback_thread(self):
        if not self.is_odometry_thread_active:
            self.is_odometry_thread_active = True
            self.odometry_callback_thread.start()
            print("Started odometry callback thread")

    def stop_odometry_callback_thread(self):
        if self.is_odometry_thread_active:
            self.is_odometry_thread_active = False
            self.odometry_callback_thread.join()
            print("Stopped odometry callback thread.")
    
def main():
    TestThread = RepeatThread()

    TestThread.start_image_callback_thread()
    TestThread.start_odometry_callback_thread()
    time.sleep(5)
    TestThread.stop_image_callback_thread()
    TestThread.stop_odometry_callback_thread()

main()
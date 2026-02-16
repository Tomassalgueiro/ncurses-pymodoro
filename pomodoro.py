import sounddevice as sd
import soundfile as sf

data,fs = sf.read("alarm.wav", dtype='float32')

# POMODORO LOGIC FIRST
class Pomodoro:
    # this implementation follows the method:
    # work small break 3 times and then work and a big break (usually 20 min, but may add option to change it later)

    def __init__(self, small_break=3, big_break=1, time_session=1500, time_small_break=300, time_big_break=1200):
        self.small_break = small_break
        self.big_break = big_break
        self.time_session = time_session
        self.time_small_break = time_small_break
        self.time_big_break = time_big_break
        self.count = 0
        self.mode = "Work"
        self.running = False
        self.remaining = time_session

    def toggle(self):
        self.running = not self.running

    def tick(self):
        if not self.running:
            return False

        self.remaining -=1
        if self.remaining <= 0:
            self.switch_mode()
            self.toggle() 
            return True
        return False

    def switch_mode(self):
        if self.mode == "Work":
            if self.count == self.small_break:
                self.mode = "Big Break"
                self.remaining = self.time_big_break 
                self.count = 0
            else:
                self.mode = "Small Break"
                self.remaining = self.time_small_break 
                self.count += 1
        else:
            self.mode = "Work"
            self.remaining =  self.time_session


import curses
import time
from curses import wrapper

#stdscr = curses.initscr()

#def main(stdscr):

#   curses.noecho()
#   curses.cbreak()
#   stdscr.keypad(True)
#   curses.nocbreak()
#   stdscr.keypad(False)
#   curses.echo()
#   curses.endwin()

#    stdscr.clear()

#    for i in range(0,11):
#        v = i-10
#        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))

#        stdscr.refresh()
#        stdscr.getkey()

# wrapper(main)

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
        self.mode = "work"
        self.running = False
        self.remaining = time_session

    def toggle(self):
        self.running = not self.running

    def tick(self):
        if not self.running:
            return

        self.remaining -=1
        if self.remaining <= 0:
            self.switch_mode()

    def switch_mode(self):
        if self.mode == "work":
            if self.count >= self.small_break:
                self.mode = "big_break"
                self.remaining = self.time_big_break 
                self.count = 0
            else:
                self.mode = "small_break"
                self.remaining = self.time_small_break 
                self.count += 1
        else:
            self.mode = "work"
            self.remaining =  self.time_session

p1 = Pomodoro(3,1,5,3,12)

p1.toggle()
flag = False
while 1:
    print(p1.remaining)
    p1.tick()
    time.sleep(1)
    if flag == True:
        print("swapping mode")
        flag = False
    if p1.remaining == 1:
        flag = True
print("finished")


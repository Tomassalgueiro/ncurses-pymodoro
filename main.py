import curses
import time
from curses import wrapper
import sounddevice as sd
import soundfile as sf

import pomodoro
import number_design

# the clock is 5 units tall and 17 wide
CLOCK_SIZE_Y = 5
CLOCK_SIZE_X = 17

data,fs = sf.read("alarm.wav", dtype='float32')

def format_time(seconds):
    minute = seconds // 60
    sec = seconds % 60
    return f"{minute:02}:{sec:02}"

def main(stdscr):


    curses.curs_set(0)
    stdscr.timeout(100)
    
    # create pomodoro object (check pomodoro.py for more info on parameters)
    p1 = pomodoro.Pomodoro(3,1,5,3,12)

    last_tick_time = time.time()

    while True:
        
        screen_size_x = curses.COLS
        screen_size_y = curses.LINES
        
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord(' '):
            p1.toggle()
        elif key == ord('t') and not p1.running:
            p1.switch_mode()

        current_time = time.time()
        if current_time - last_tick_time >= 1.0:
            play_alarm = p1.tick()
            last_tick_time = current_time
        else:
            play_alarm = False

        stdscr.erase()
        time_str = format_time(p1.remaining)
        
        # try block to avoid crashes in case the terminal is too small
        try:
            stdscr.addstr(screen_size_y // 2 + 7,screen_size_x // 2 - 17 // 2, f"Mode: {p1.mode}") 
            stdscr.addstr(screen_size_y // 2 + 8,screen_size_x // 2 - 17 // 2, f"Space = Start/Pause")
            stdscr.addstr(screen_size_y // 2 + 9,screen_size_x // 2 - 17 // 2, f"Q = Quit")
            
            current_x = screen_size_x // 2 - CLOCK_SIZE_X // 2  
            for char in time_str:
                if char == ":":
                    stdscr.addstr(screen_size_y // 2 - 1, current_x, "█")
                    stdscr.addstr(screen_size_y // 2 + 1, current_x, "█")
                    current_x += 2
                else:
                    pattern = number_design.num_dict[int(char)]
                    for i, bit in enumerate(pattern):
                        if bit:
                            stdscr.addstr(screen_size_y // 2 - 2 + (i//3), current_x + (i % 3), "█")
                    current_x += 4

        # might add a messsage saying "terminal size too small", not important right now
        except curses.error:
            pass

        stdscr.refresh()
        if play_alarm == True:
            sd.play(data,fs)
            sd.wait()


wrapper(main)

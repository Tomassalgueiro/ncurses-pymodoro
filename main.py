import curses
import time
from curses import wrapper

import pomodoro
import number_design

CLOCK_POS_X = 5
CLOCK_POS_Y = 4



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
        
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord(' '):
            p1.toggle()

        current_time = time.time()
        if current_time - last_tick_time >= 1.0:
            p1.tick()
            last_tick_time = current_time
        
        stdscr.erase()
        time_str = format_time(p1.remaining)
        try:
            stdscr.addstr(0,0, f"Mode: {p1.mode}") 
            stdscr.addstr(2,0, f"Space = Start/Pause")
            stdscr.addstr(3,0, f"Q = Quit")
            
            current_x = CLOCK_POS_X
            for char in time_str:
                if char == ":":
                    stdscr.addstr(CLOCK_POS_Y + 1, current_x, "o")
                    stdscr.addstr(CLOCK_POS_Y + 3, current_x, "o")
                    current_x += 2
                else:
                    pattern = number_design.num_dict[int(char)]
                    for i, bit in enumerate(pattern):
                        if bit:
                            stdscr.addstr(CLOCK_POS_Y + (i//3), current_x + (i % 3), "█")
                    current_x += 4
        except curses.error:
            pass

        stdscr.refresh()


wrapper(main)

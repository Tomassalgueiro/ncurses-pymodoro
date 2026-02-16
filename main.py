import curses
import time
import pomodoro
from curses import wrapper


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
        try:
            stdscr.addstr(0,0, f"Mode: {p1.mode}")
            stdscr.addstr(1,0, f"Remaining: {format_time(p1.remaining)}")
            stdscr.addstr(3,0, f"Space = Start/Pause")
            stdscr.addstr(4,0, f"Q = Quit")
        except curses.error:
            pass

        stdscr.refresh()


wrapper(main)

import curses
import time
from curses import wrapper
import sounddevice as sd
import soundfile as sf
from pathlib import Path

import pomodoro
import number_design

# the clock is 5 units tall and 17 wide
CLOCK_SIZE_Y = 5
CLOCK_SIZE_X = 17

# identify the audio file
# to change it swap alarm.wav in the config 
data,fs = sf.read("alarm.wav", dtype='float32')

# finds the directory 
directory = Path.home()/".config"/"ncurses_pymodoro"
file = directory/"config.txt"

# make sure the file
directory.mkdir(parents=True, exist_ok=True)

# create file if it doesn't exist
if not file.exists():
    with open(file, "w") as config:
        config.write("3\n")
        config.write("1\n")
        config.write("1500\n")
        config.write("300\n")
        config.write("1200\n")
    config_val = [3,1,1500,300,1200]
else:
    with open(file, "r") as config:
        config_val = [int(line.strip()) for line in config.readlines()]        


# define the 3 possible colorschemes
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

def get_text_color(mode):
    match mode:
        # this will output red
        case "Work":
            return 1
        case "Small Break":
            return 2
        case "Big Break":
            return 3

def format_time(seconds):
    minute = seconds // 60
    sec = seconds % 60
    return f"{minute:02}:{sec:02}"

def main(stdscr):

    curses.curs_set(0)
    stdscr.timeout(100)
    
    # create pomodoro object (check pomodoro.py for more info on parameters)
    # hardcoded version
    #p1 = pomodoro.Pomodoro(3,1,1500,300,1200)
    # insert .config version in here    
    p1 = pomodoro.Pomodoro(config_val[0],config_val[1],config_val[2],config_val[3],config_val[4])
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
        # implement helper window if the program is not running
        # this will call another window and pressing backspace will go back
        # elif key == ord('h') and not p1.running: 
        elif key == curses.KEY_RESIZE:
            curses.update_lines_cols()
            stdscr.clear()


        current_time = time.time()
        if current_time - last_tick_time >= 1.0:
            play_alarm = p1.tick()
            last_tick_time = current_time
        else:
            play_alarm = False

        stdscr.clear()
        time_str = format_time(p1.remaining)
        
        # try block to avoid crashes in case the terminal is too small
        try:
            stdscr.addstr(screen_size_y // 2 + 6,screen_size_x // 2 - 17 // 2, f"Mode: {p1.mode}") 
            stdscr.addstr(screen_size_y // 2 + 7,screen_size_x // 2 - 17 // 2, f"Count: {p1.count}") 
            stdscr.addstr(screen_size_y // 2 + 8,screen_size_x // 2 - 17 // 2, f"Cycles: {p1.cycles}") 
            stdscr.addstr(screen_size_y // 2 + 9,screen_size_x // 2 - 17 // 2, f"Space = Start/Pause")
            stdscr.addstr(screen_size_y // 2 + 10,screen_size_x // 2 - 17 // 2, f"Q = Quit")
            
            current_x = screen_size_x // 2 - CLOCK_SIZE_X // 2  
            for char in time_str:
                if char == ":":
                    #stdscr.addstr(screen_size_y // 2 - 1, current_x, "█", curses.color_pair(get_co)
                    stdscr.addstr(screen_size_y // 2 - 1, current_x, "█")
                    stdscr.addstr(screen_size_y // 2 + 1, current_x, "█")
                    current_x += 2
                else:
                    pattern = number_design.num_dict[int(char)]
                    for i, bit in enumerate(pattern):
                        if bit:
                            stdscr.addstr((screen_size_y // 2 - 2 + (i//3)), current_x + (i % 3), "█")
                    current_x += 4

        # might add a messsage saying "terminal size too small", not important right now
        except curses.error:
            pass

        stdscr.refresh()
        if play_alarm == True:
            sd.play(data,fs)
            sd.wait()

wrapper(main)

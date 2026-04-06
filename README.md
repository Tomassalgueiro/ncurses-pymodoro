# ncurses-pymodoro

This is a small project in which i implement a pomodoro timer and draw it on the terminal using the curses (ncurses for C users) library.

### Installation 

Firstly make sure you have all the dependencies installed

```
sudo apt install portaudio19-dev libsndfile1
```

```
sudo dnf install portaudio-devel libsndfile
```

```
sudo pacman -S portaudio libsndfile
```

After that, clone the repo and create a virutal environment on the cloned directory

```
git clone https://github.com/Tomassalgueiro/ncurses-pymodoro.git 
cd ncurses-pymodoro
python -m venv .venv
```
Activate the virutal environment ( this may differ for other shells such as fish or zsh)
```
source .venv/bin/activate
```

Install the pip dependencies and run the program
```
pip install .
pymodoro
```

### Todo

- [x] Keyboard Control to control the timer
- [x] Curses Lib - Terminal Design
- [ ] Custom values for break amounts and times
- [ ] Add more controls to the timer
- [ ] Change the way the numbers look/add more colors
- [x] Fix the bug, where if you resize the terminal it doesn't readjust
- [ ] Change the config file to json format
- [ ] Create Helper page when the program is paused that 


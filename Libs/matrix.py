import platform
import time
import random
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Libs import Colors

if platform.system() == "Windows":
    import msvcrt
else:
    import select
    import tty
    import termios
   
def clean_buffer():
    if platform.system() == "Windows":
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        # Mac/Linux clear buffer
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
        
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def matrix_effect():
    """Classic vertical rain: high-activity, slim tails, buffer-safe."""
    old_settings = None
    os.system('cls' if os.name == 'nt' else 'clear')

    if platform.system() != "Windows":
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

    try:
        width, height = os.get_terminal_size()
    except OSError:
        width, height = 80, 24

    # Each index in columns stores the current 'head' position of a drop
    # 0 means the column is currently empty/inactive
    columns = [0] * width
    chars = "10i!|¦·:;rtv"
    
    print("\033[?25l", end="") # Hide cursor

    try:
        while not kbhit():
            # \033[H keeps the terminal from scrolling (buffer-safe)
            print("\033[H", end="") 
            
            frame = []
            for h in range(height - 1):
                row = ""
                for i in range(width):
                    head_pos = columns[i]
                    
                    # If the row is within the last 6 characters of the head
                    if head_pos > h > (head_pos - 6): 
                        char = random.choice(chars)
                        # Bright white head for the leading character
                        if h == int(head_pos) - 1:
                            row += f"\033[1;37m{char}\033[0m"
                        # Dimmer green tail
                        else:
                            row += f"{Colors.GREEN}{char}{Colors.ENDC}"
                    else:
                        row += " "
                frame.append(row)
            
            # Update positions
            for i in range(width):
                if columns[i] > 0:
                    columns[i] += 0.7  # Increased fall speed for more 'action'
                    if columns[i] > height + 6: 
                        columns[i] = 0
                # INCREASED DENSITY: 0.98 instead of 0.998
                # This causes many more 'fallings' to occur simultaneously
                elif random.random() > 0.98: 
                    columns[i] = 1

            print("\n".join(frame), end="", flush=True)
            time.sleep(0.09)

    finally:
        print("\033[?25h", end="") # Restore cursor
        if old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        if platform.system() == "Windows":
            while msvcrt.kbhit():
                msvcrt.getch()
            
def kbhit():
    if platform.system() == "Windows":
        return msvcrt.kbhit()
    else:
        # Mac/Linux non-blocking check
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

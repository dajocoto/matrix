import os
import platform
import sys
from Libs.Colors import Colors
if platform.system() == "Windows":
    import msvcrt
else:
    import select
    import tty
    import termios

def createDirectory(folder):
    folder.mkdir(parents=True, exist_ok=True)

def showLine():
    print(f"\t{Colors.CYAN}────────────────────────────────────────────{Colors.ENDC}")
    input(f"\t{Colors.YELLOW}Press Enter to return to menu...{Colors.ENDC}")
    
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def clean_buffer():
    if platform.system() == "Windows":
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
        
def kbhit():
    if platform.system() == "Windows":
        return msvcrt.kbhit()
    else:
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
import os
import sys
import subprocess
import platform
import time
import random
import getpass
from pathlib import Path

# Fix Path for Imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Custom Module Imports
from Libs.Colors import Colors
from Libs import matrix

from Utils import Utils
from Libs import PhoneSearcher
from Starters import ApiRest

from DataAccess import DataSource


# Platform-specific input handling
if platform.system() == "Windows":
    import msvcrt
else:
    import select
    import tty
    import termios

# --- Global State ---
SOURCE_STATUS = "[Checking...]"
checks_started = False



def run_background_script(script_path):
    is_windows = platform.system() == "Windows"
    script_path = str(Path(script_path).resolve())
    if is_windows:
        cmd = ["cmd.exe", "/c", f'"{script_path}"']
        flags = 0x08000000 | 0x00000008  # CREATE_NO_WINDOW | DETACHED_PROCESS
    else:
        cmd = ["sh", script_path]
        flags = 0

    print(f"\n\t{Colors.YELLOW}📡 Launching background script: {Path(script_path).name}{Colors.ENDC}")
    try:
        subprocess.Popen(
            cmd,
            creationflags=flags if is_windows else 0,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            close_fds=True,
            start_new_session=not is_windows
        )
        print(f"\t{Colors.GREEN}✔ Script running in background.{Colors.ENDC}")
    except Exception as e:
        print(f"\n\t{Colors.RED}❌ Launch failed: {e}{Colors.ENDC}")
    Utils.showLine()

def run_shell_command(command):
    print(f"\n\t{Colors.YELLOW}⚡ {Colors.BOLD}Executing:{Colors.ENDC} {command}")
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"\n\t{Colors.RED}❌ Error:{Colors.ENDC} {e}")
    Utils.showLine()

# --- Animated Menu Logic ---

def getOptions():
    # Use the globally updated status instead of calling the slow ApiRest here
    global SOURCE_STATUS
    options = [
        ("1", "Sync Branches", "Update all repositories"),
        ("2", "Update Deps", "Copy built JARs to distribution"),
        ("3", "Update Resources", "Deploy properties and license"),        
        ("4", "Run Command", "Execute system command"),
        ("5", "Kill App Port", "Stop Port process"),
        ("6", "Start Designer", "Launch TestDesigner"),
        ("7", "Search files", "Search matching files by name"),
        ("8", "Run Logs Parser", "Format logs into a HTML format"),
        ("a", "Run App", "Start Platform"),
        ("d", "Simple Decryption", "Decrypt Properties"),
        ("e", "Encrypt Properties", "Encrypt Properties"),
        ("f", "Search Phone Number", "Who called"),
        ("h", "Java Help", "Show Java Diagnostic Tools"),
        ("i", "IP Address", "Get Public IP Address"),
        ("p", "AWS Bridge", "Start/Stop"),
        ("r", "Reduce Properties", "Remove Recent scenarios"),
        ("v", "Validate Sources", f"Check sources status {Colors.GREEN}{SOURCE_STATUS:<56}{Colors.ENDC}"),
        ("w", "Data", "Show Properties"),
        ("q", "Exit", "Close toolbox")
        
    ]
    return options

def getMenuBox():
    cpu_str = ApiRest.CPU_USAGE
    mem_str = ApiRest.MEM_USAGE
    dsk_str = ApiRest.DISK_USAGE
    time_str = ApiRest.TIME_NOW
    title = "DEV TOOLBOX MASTER CONTROL"
    stats_line = f"{Colors.GREEN}{time_str:10} {Colors.ENDC}CPU: {Colors.GREEN}{cpu_str}{Colors.ENDC} | MEM: {Colors.GREEN}{mem_str}{Colors.ENDC} | DSK: {Colors.GREEN}{dsk_str}{Colors.ENDC}"
    menu_content = [
        f"{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════╗{Colors.ENDC}",
        f"{Colors.CYAN}║{Colors.ENDC} {Colors.BOLD}{title:<60}{Colors.ENDC} {stats_line:>48} {Colors.CYAN}║{Colors.ENDC}",
        f"{Colors.CYAN}╠═══════════════════════════╦═══════════════════════════════════════════════════════════════════════════════╣{Colors.ENDC}"
    ]

    myOptions = getOptions()
    for key, title, desc in myOptions:
        color = Colors.RED if key == 'q' else Colors.CYAN
        menu_content.append(
            f"{Colors.CYAN}║{Colors.ENDC} {color}{Colors.BOLD}{key:>2}){Colors.ENDC} {title:<21} {Colors.CYAN}║{Colors.ENDC} {desc:<77} {Colors.CYAN}║{Colors.ENDC}"
        )
    menu_content.append(f"{Colors.CYAN}╚═══════════════════════════╩═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
    menu_content.append(f"  {Colors.BOLD}Select an option »{Colors.ENDC} ")
    return menu_content

def matrix_toolbox():
    global SOURCE_STATUS, checks_started
    try:
        width, height = os.get_terminal_size()
    except OSError:
        width, height = 80, 24

    columns = [0] * width
    chars = DataSource.getMatrix()["chars"]
    
    # Start background status check (Assumes your ApiRest has the background logic implemented)

    if not checks_started:
        ApiRest.start_background_checks()
        checks_started = True
        
    print("\033[?25l", end="") 

    try:
        frame_count = 0
        while True:
            # Periodically sync local SOURCE_STATUS with ApiRest cache if needed
            SOURCE_STATUS = ApiRest.getStatus() 
            
            menu_content = getMenuBox()
            if Utils.kbhit():
                if platform.system() == "Windows":
                    key = msvcrt.getch()
                    if key in (b'\xe0', b'\x00'):
                        msvcrt.getch() 
                        continue
                    try:
                        return key.decode().lower()
                    except: return ""
                else:
                    return sys.stdin.read(1).lower()

            sys.stdout.write("\033[H") 
            
            start_y = (height - len(menu_content)) // 2
            start_x = (width - 110) // 2 # Adjusted for box width
            
            frame = []
            for h in range(height - 1):
                row_list = []
                for i in range(width):
                    # SLIM LOGIC: Shorter tails (6 chars)
                    if columns[i] > h > (columns[i] - 6):
                        c = random.choice(chars)
                        if h == int(columns[i]) - 1:
                            color = "\033[1;37m" # Sparkly White Head
                        else:
                            # Color Cycling
                            cycle = (frame_count // 100) % 2
                            color = Colors.GREEN if cycle == 0 else Colors.RED
                        row_list.append(f"{color}{c}{Colors.ENDC}")
                    else:
                        row_list.append(" ")
                
                row_str = "".join(row_list)
                menu_idx = h - start_y
                if 0 <= menu_idx < len(menu_content):
                    # Overlay menu using ANSI positioning
                    frame.append(f"{row_str}\033[{h+1};{start_x}H{menu_content[menu_idx]}")
                else:
                    frame.append(row_str)

            for i in range(width):
                if columns[i] > 0:
                    columns[i] += 0.7
                    if columns[i] > height + 6: columns[i] = 0
                elif random.random() > 0.985: # Slim Density
                    columns[i] = 1

            sys.stdout.write("\n".join(frame))
            sys.stdout.flush()
            frame_count += 1
            time.sleep(0.04)
    finally:
        print("\033[?25h", end="")

# --- Main Application Logic ---

def main_menu():
    while True:
        Utils.clear_screen()
        choice = matrix_toolbox().strip()
        
        Utils.clear_screen()
        Utils.clean_buffer()

        if choice == '1':
            print(f"\n\t{Colors.RED}✔ Action not supported!{Colors.ENDC}")
            Utils.showLine()
        elif choice == '2':
            print(f"\n\t{Colors.RED}✔ Action not supported!{Colors.ENDC}")
            Utils.showLine()
        elif choice == '3':
            print(f"\n\t{Colors.RED}✔ Action not supported!{Colors.ENDC}")
            Utils.showLine()
        elif choice == 'a':
            print(f"\n\t{Colors.RED}✔ Action not supported!{Colors.ENDC}")
            Utils.showLine()
        elif choice == '4':
            print(f"\n\t{Colors.RED}✔ Action not supported!{Colors.ENDC}")
            Utils.showLine()
        elif choice == '5':
            print(f"\n\t{Colors.RED}✔ Action not supported!{Colors.ENDC}")
            Utils.showLine()
        elif choice == '6':
            print(f"\n\t{Colors.RED}✔ Action not supported!{Colors.ENDC}")
            Utils.showLine()
        elif choice == '7':
            print(f"\n\t{Colors.RED}✔ Action not supported!{Colors.ENDC}")
            Utils.showLine()
        elif choice == '8':
            print(f"\n\t{Colors.RED}✔ Action not supported!{Colors.ENDC}")
            Utils.showLine()
        elif choice == 'v':
            print(f"\n\t{Colors.RED}✔ Action not supported!{Colors.ENDC}")
            Utils.showLine()
        elif choice == 'r':
            print(f"\n\t{Colors.RED}✔ Action not supported!{Colors.ENDC}")
            Utils.showLine()
        elif choice == 'd':
            print(f"\n\t{Colors.RED}✔ Action not supported!{Colors.ENDC}")
            Utils.showLine()
        elif choice == 'w':
            print(f"\n\t{Colors.RED}✔ Action not supported!{Colors.ENDC}")
            Utils.showLine()
        elif choice == 'e':
            print(f"\n\t{Colors.RED}✔ Action not supported!{Colors.ENDC}")
            Utils.showLine()
        elif choice == 'f':
            number = input(f"\t{Colors.BOLD}Enter Phone number: {Colors.ENDC}").strip()
            PhoneSearcher.get_basic_info(number)
            Utils.showLine()
        elif choice == 'h':
            print(f"\n\t{Colors.RED}✔ Action not supported!{Colors.ENDC}")
            Utils.showLine()
        elif choice == 'i':            
            print(f"\n\t{Colors.RED}✔ Action not supported!{Colors.ENDC}")
            Utils.showLine()
        elif choice == 'p':
            print(f"\n\t{Colors.RED}✔ Action not supported!{Colors.ENDC}")
            Utils.showLine()
        elif choice in ['q', 'x']:
            print(f"\n\t{Colors.GREEN}✔ Execution complete!{Colors.ENDC}")
            time.sleep(0.8)
            Utils.clear_screen()
            break

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        Utils.clear_screen()
        sys.exit(0)
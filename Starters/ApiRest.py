import psutil
import asyncio
import httpx
import requests
import datetime
import threading
from DataAccess import DataSource
from Libs.Colors import Colors

# Global Status Variable
SOURCE_STATUS = "[Checking...]"
CPU_USAGE = "..."
MEM_USAGE = "..."
DISK_USAGE = "..."
TIME_NOW = "..."



def get_public_ip():
    print("\t🔍 Fetching your public IP address...")
    try:
        # We use a 5-second timeout to prevent the script from hanging
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        
        # Raise an error if the request failed
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()        
        print(f"\t✅ Your Public IP is: {data['ip']}")
        
    except requests.exceptions.RequestException as e:
        print(f"\tError retrieving IP: {e}")
    
def getStatus():
    """Returns the current cached status."""
    return SOURCE_STATUS

async def _performance_loop():
    """Background loop to refresh CPU and Memory metrics."""
    global CPU_USAGE, MEM_USAGE, DISK_USAGE, TIME_NOW
    try:
        process = psutil.Process() # Track the current toolbox process or system
        psutil.cpu_percent(interval=None)
        
        while True:
            
            mem_val = psutil.virtual_memory().percent
            MEM_USAGE = f"{mem_val:>3.0f}%"
            
            cpu = psutil.cpu_percent(interval=None)            
            CPU_USAGE = f"{cpu:>3.0f}%"
            
            try:
                # Try 1: The current directory (best for E:\ or external drives)
                path = os.getcwd()
                disk_val = psutil.disk_usage(path).percent
            except:
                try:
                    # Try 2: The absolute system root ('/' on Mac/Linux, 'C:\' on Win)
                    root = Path(__file__).anchor if "__file__" in locals() else "/"
                    disk_val = psutil.disk_usage(root).percent
                except:
                    # Try 3: Hardcoded common root
                    try:
                        disk_val = psutil.disk_usage('/').percent
                    except:
                        disk_val = 0 # Absolute failure

            DISK_USAGE = f"{disk_val:>3.0f}%"
            try:
                 TIME_NOW = datetime.datetime.now().strftime("%H:%M:%S")
            except:
                TIME_NOW = ".-."
            await asyncio.sleep(1)
    except Exception:
        print("")
        
async def _update_loop():
    """Internal async loop to refresh the status."""
    global SOURCE_STATUS
    # Create the client once and reuse it (more efficient)
    async with httpx.AsyncClient() as client:
        while True:
            try:
                settings = DataSource.getStartUpSettings()
                # Ensure the URL is valid
                dns = settings.get('dns', 'localhost')
                base_url = f"http://{dns}/"
                
                response = await client.head(base_url, timeout=2.0)
                status = "ACTIVE" if response.status_code < 400 else f"ERR {response.status_code}"
            except Exception:
                status = "DOWN"
            
            SOURCE_STATUS = f"{dns} is {status}"
            # Wait 30 seconds before checking again
            await asyncio.sleep(5)

def start_background_checks():
    """
    Entry point for your Toolbox. 
    Starts the async loop in a dedicated background thread.
    """
    def run_async_loop():
        # 1. Create a fresh event loop for this specific thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # 2. Define a wrapper to run both loops together
        async def main_task():
            # Run both tasks concurrently
            await asyncio.gather(
                _performance_loop(),
                _update_loop()
            )

        # 3. Start the loop and keep it alive
        try:
            loop.run_until_complete(main_task())
        except Exception as e:
            # Prevent the background thread from crashing silently
            print(f"Background thread error: {e}")
        finally:
            loop.close()

    # Only start if one isn't already running (checked via a flag in your main script)
    thread = threading.Thread(target=run_async_loop, daemon=True)
    thread.start()
            
def Connector(setting):
    # 1. Initialize the Client (Equivalent to requests.Session)
    # We set a default timeout to prevent the UI from hanging if the server is slow
    print(f"\tChecking...")
    with httpx.Client(timeout=1.0) as client:
        
        # Configuration
        base_url = f"http://{setting['dns']}/st"
        login_payload = {
            "username": setting['username'],
            "password": setting['password']
        }

        try:
            # 2. Perform LOGIN (POST)
            # httpx uses 'data' for form-encoded and 'json' for JSON bodies
            login_url = f"{base_url}/admin/loggin"
            login_response = client.post(login_url, data=login_payload)
            
            if login_response.status_code != 200:
                print(f"\t{Colors.RED}Login Failed (Status {login_response.status_code}){Colors.ENDC}")
                return

            # 3. Verify Login Status (GET)
            check_url = f"{base_url}/Logged"
            params_check = {"_": "1772208894485"}
            check_response = client.get(check_url, params=params_check)        
            
            if not check_response.json().get('logged'):
                print(f"\t{Colors.YELLOW}Session verification failed.{Colors.ENDC}")
                return
            
            # 4. Get Repository List (GET)
            list_url = f"{base_url}/epositoryNamesByUser"
            list_params = {"_": "1772209048785"}
            list_response = client.get(list_url, params=list_params)
            
            if list_response.status_code == 200:
                repos = list_response.json()
            else:
                print(f"\tFailed to fetch repository list. Code: {list_response.status_code}")
                return

            # 5. Loop through each repository to get status
            print("\t" + "─"*60)
            for repo_name in repos:
                repo_url = f"{base_url}/etRepooryStatus"
                repo_params = {
                    "name": repo_name,
                    "_": "1772209048719"
                }
            
                repo_response = client.get(repo_url, params=repo_params)
            
                if repo_response.status_code == 200:
                    data = repo_response.json()
                    status = data.get('status', 'Unknown')
                    # Colorizing output for better readability in your terminal
                    status_color = Colors.GREEN if status == "Active" else Colors.YELLOW
                    print(f"\tRepository: {Colors.CYAN}{repo_name: <20}{Colors.ENDC} | Status: {status_color}{status}{Colors.ENDC}")
                else:
                    print(f"\t[!] Could not get status for {repo_name} (Code: {repo_response.status_code})")
            print("\t" + "─"*60)

            # 6. Get License Info
            license_url = f"{base_url}/"
            license_response = client.get(license_url, params=list_params)
            
            if license_response.status_code == 200:
                # httpx .text provides the decoded string
                license_info = license_response.text
                print(f"\tLicense Info: {Colors.BOLD}{license_info}{Colors.ENDC}")
            else:
                print(f"\tFailed to fetch license. Status: {license_response.status_code}")

        except httpx.RequestError as e:
            print(f"\t{Colors.RED}Network error occurred: {e}{Colors.ENDC}")
        except Exception as e:
            print(f"\t{Colors.RED}An unexpected error occurred: {e}{Colors.ENDC}")     

import phonenumbers
import httpx
from phonenumbers import geocoder, carrier
from bs4 import BeautifulSoup

def get_basic_info(number_str):
    try:
        # Parse number (include country code like +1 for US)
        parsed_number = phonenumbers.parse(number_str)
        
        # Get Region/Location
        region = geocoder.description_for_number(parsed_number, "en")
        
        # Get Carrier name
        service_provider = carrier.name_for_number(parsed_number, "en")
        lookup_syncme(number_str)
        print(f"Number: {number_str}")
        print(f"Location: {region}")
        print(f"Carrier: {service_provider}")
        
    except Exception as e:
        print(f"Error: {e}")
def lookup_syncme(phone_number):
    clean_number = phone_number.replace("+", "").replace(" ", "")
    url = f"https://sync.me/search/?number={clean_number}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        with httpx.Client(headers=headers, follow_redirects=True) as client:
            response = client.get(url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Sync.me usually puts the name in a specific <h2> or <span> class
                name_element = soup.find("h2", class_="name")
                owner_name = name_element.text.strip() if name_element else "Unknown/Private"
                print(f"Owner: {owner_name}")
            else:
                print(f"response: {response}")               
                
    except Exception as e:
        print(f"response: {str(e)}")
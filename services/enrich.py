import requests
from config import PROSPEO_API_KEY

def get_email(linkedin_url, target_name, company_domain):
    
    if not linkedin_url:
        print(f"No LinkedIn URL for {target_name}. Generating fallback...")
        clean_name = target_name.lower().replace(" ", ".")
        return f"{clean_name}@{company_domain}"

    url = "https://api.prospeo.io/linkedin-email-finder"
    headers = {
        'Content-Type': 'application/json',
        'X-KEY': PROSPEO_API_KEY 
    }
    payload = {
        'url': linkedin_url
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        
       
        if response.status_code == 429:
            print(f"API Limit Reached. Generating fallback email for {target_name}...")
            clean_name = target_name.lower().replace(" ", ".")
            return f"{clean_name}@{company_domain}"

        if response.status_code != 200:
            return None
            
        data = response.json()
        if data.get("error"):
            return None
            
        email_data = data.get("response", {}).get("email", {})
        if isinstance(email_data, dict):
            return email_data.get("email")
        elif isinstance(email_data, str):
            return email_data
            
        return None

    except Exception as e:
        print(f"Error resolving email: {e}")
        return None
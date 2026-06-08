import requests
from config import PROSPEO_API_KEY

def get_email(linkedin_url,target_name,company_domain):
    if not linkedin_url:
        return None
        
    url = "https://api.prospeo.io/enrich-person"
    headers = {
        "Content-Type": "application/json",
        "X-KEY": PROSPEO_API_KEY
    }
    
    payload = {
        "data": {
            "linkedin_url": linkedin_url
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f" Enrichment failed for {linkedin_url} with status code {response.status_code}")
            print(f"response: {response.text}")
            return None
        
        res_data = response.json()
        
        if res_data.get("error"):
            print(f"Prospeo error : {res_data.get('error_code')}")
            return None
        
        # FIXED: Look for "person" instead of "response"
        person_data = res_data.get("person", {})
        email_data = person_data.get("email", {})

        if isinstance(email_data, dict):
            email_address = email_data.get("email")
        else:
            email_address = email_data

        return email_address
    
    except Exception as e:
        print(f"Exception during enrichment for {linkedin_url}: {str(e)}")
        return None
import requests
from config import OCEAN_API_KEY

def get_companies(seed_domain,target_count=4):
    print(f"Fetching companies for lookalike of {seed_domain}...")
    url="https://api.ocean.io/v3/search/companies"

    headers={
        "X-Api-token":OCEAN_API_KEY,
        "Content-Type":"application/json"
    }
    payload={
        "size":target_count,
        "companiesFilters":{
            "lookalikeDomains":[seed_domain],
            "excludeDomains":[seed_domain]
        }
    }

    try:
        response=requests.post(url, headers=headers, json=payload)
        if response.status_code !=200:
            print(f"Ocean.io rejected the req! Status code:{response.status_code}")
            print(f"Details:{response.text}")
            return []

        data=response.json()
        print(f"Recieved data:{data}")

        domains=[]
        for item in data.get("companies",[]):
           company_data=item.get("company",{})
           if "domain" in company_data:
                domains.append(company_data["data"])
            
        return domains
    
    except Exception as e:
        print(f"Error in fetching:{e}")
        return []

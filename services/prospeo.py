import requests
from config import PROSPEO_API_KEY

def find_contacts(domains):
    if not domains:
        print("No domains provided to prospeo")
        return []
    
    print(f"Querying Prospeo for contacts across {len(domains)} domains ....")
    url="https://api.prospeo.io/search-person"

    headers={
        "Content-Type":"application/json",
        "X-KEY":PROSPEO_API_KEY
    }

    payload={
        "page":1,
        "filters":{
            "company":{
                "websites":{
                    "include":[domains]
                }
            },
            # "person_seniority":{
            #     "include":["Founder/Owner"]
            # }

        }
    }

    try:
        response=requests.post(url,json=payload,headers=headers)

        if response.status_code !=200:
            print(f"Prospeo rejected the request! Status code:{response.status_code}")
            print(f"Details:{response.text}")
            return []
        data=response.json()

        if data.get("error"):
            print(f"Prospeo API error:{data.get('error_code')}")
            return []
        
       
        results=data.get("results",[])

        # if results:
        #     print("\n raw person data")
        #     print(results[0].get("person",{}))
        
        contacts=[]


        for item in results:
            person =item.get("person",{})
            company=item.get("company",{})

            first_name=person.get("first_name","")
            last_name=person.get("last_name","")
            full_name=person.get("full_name", f"{first_name} {last_name}".strip())

            linkedin_url=person.get("linkedin_url", "")
            company_domain=company.get("domain", "")

            if full_name:
                contacts.append({
                    "name":full_name,
                    "linkedin_url":linkedin_url,
                    "company_domain":company_domain
                })
        return contacts
    
    except Exception as e:
        print(f"Error in prosper API Execution:{e}")
        return []

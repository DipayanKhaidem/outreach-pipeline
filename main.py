# main.py
import time
from services.ocean import get_companies
from services.prospeo import find_contacts
from services.enrich import get_email
from services.brevo import send_email

def main():
    seed_domain = input("Enter the seed company domain (e.g., target.com): ").strip()
    
    if not seed_domain:
        print("Domain cannot be empty. Exiting.")
        return

  
    print(f"\n Finding lookalike companies for {seed_domain}...")
    lookalikes = get_companies(seed_domain) 
    
    if not lookalikes:
        print("No lookalike companies found. Exiting.")
        return
    print("\n Sourcing decision-makers...")
    all_leads = []
    for company in lookalikes:
       
        leads = find_contacts(company)
        all_leads.extend(leads)
        time.sleep(3) 
    if not all_leads:
        print("No decision-makers found. Exiting.")
        return

   
    print("\n Resolving verified work emails...")
    enriched_leads = []
    for lead in all_leads:

        # print(f"\n[DEBUG] Raw lead data: {lead.keys()}") 
        # print(f"[DEBUG] Lead contents: {lead}")

        print(f"  -> Looking up {lead['name']} from {lead['company_domain']}...")
        email = get_email(lead['linkedin_url'])
        
        if email:
            lead['email'] = email
            enriched_leads.append(lead)
            print(f"Found: {email}")
        else:
            print(f"No verified email found.")
        time.sleep(4) 

   
    print("\n" + "="*50)
    print("PIPELINE CHECKPOINT")
    print("="*50)
    print(f"Ready to send {len(enriched_leads)} personalized emails:")
    for lead in enriched_leads:
        print(f" - {lead['name']} ({lead['email']}) at {lead['company_domain']}")
    print("="*50)
    
    confirm = input("\nDo you want to fire the emails via Brevo? (Y/N): ").strip().upper()
    
    if confirm != 'Y':
        print("Pipeline halted. No emails were sent.")
        return

    
    print("\n[Stage 4] Firing personalized outreach...")
    for lead in enriched_leads:
        send_email(lead['email'], lead['name'], lead['company_domain'])
        time.sleep(1)

if __name__ == "__main__":
    main()
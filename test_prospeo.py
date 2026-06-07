
import os

from services import prospeo

if __name__=="__main__":
    mock_domains=["razorpay.com","cashfree.com","adyen.com"]

    print("Testing Prospeo integration with mock domains...")
    contacts=prospeo.find_contacts(mock_domains)

    if contacts:
        print(f"Prospeo returned {len(contacts)} contacts:")
        for contact in contacts:
            print(f"Name:{contact['name']}")
            print(f"Domain:{contact['company_domain']}")
            print(f"LinkedIn:{contact['linkedin_url']}")
    else:
        print("No contacts found or error occurred")




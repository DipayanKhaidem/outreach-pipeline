import os

from services import enrich

if __name__=="__main__":
    print("Prospeo Email Enrichment test ....")

    test_url="https://www.linkedin.com/in/abhayhabbu"

    email=enrich.get_email(test_url)

    if(email):
        print(f"Success! Resolved email:{email}")
    else:
        print("Failed to resolve email")
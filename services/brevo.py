import requests
from config import BREVO_API_KEY, SENDER_EMAIL,DEMO_MODE,TEST_EMAIL

def send_email(target_email,target_name,company_domain):
    if not target_email:
        print(f"No email provided, skipping brevo sending")
        return False
    
    url="https://api.brevo.com/v3/smtp/email"

    headers={
        "accept":"application/json",
        "api-key":BREVO_API_KEY,
        "content-type":"application/json"
    }

    html_content=f"""
   <html>
        <body>
            <p>Hi {target_name},</p>
            <p>I was looking into {company_domain} and was really impressed by what your team is building. 
            I recently built a completely automated, zero-human-in-the-loop pipeline to generate verified B2B leads,
              and I'd love to show you a live demo of how it works.</p>
            <p>Would you be open to a quick chat next week?</p>
            <p>Best regards,
            <br>Dipayan</p>
        </body>
    </html>
    """

    # Test Mode
    actual_recipient=target_email
    if DEMO_MODE:
        print(f"Test Mode: Redirecting mail meant for {target_email} to {TEST_EMAIL}")
        actual_recipient=TEST_EMAIL

    payload={
        "sender":{
            "name":"Dipayan",
            "email":SENDER_EMAIL
        },
        "to":[
            {
                "email":actual_recipient,
                "name":target_name
                }

        ],
        "subject":f"Quick Question about {company_domain}'s outreach",
        "htmlContent":html_content
    }

    try:
        response=requests.post(url,headers=headers,json=payload)

        if response.status_code in [200,201]:
            print(f"Email successfully dispatched to {target_email}")
            return True
        else:
            print(f"Brevo failed to send. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
    except Exception as e:
        print(f"Exception during email dispatch : {e}")
        return False

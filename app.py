import streamlit as st
import time
from services.ocean import get_companies
from services.prospeo import find_contacts
from services.enrich import get_email
from services.brevo import send_email

st.set_page_config(page_title="OutReach Pipeline", layout="centered")

st.title("B2B Automated Outreach Engine")
st.markdown("Zero-human-in-the-loop pipeline: Sourcing --> Enrichment --> Outreach")

if "enriched_leads" not in st.session_state:
    st.session_state.enriched_leads = None

raw_domain = st.text_input("Enter seed company domain:", placeholder="e.g., dub.co")

if st.button("Start Pipeline") and raw_domain:
    seed_domain = raw_domain.strip().lower()
    if seed_domain.startswith("https://") or seed_domain.startswith("http://"):
        seed_domain = seed_domain.split("//")[1]
    if seed_domain.startswith("www."):
        seed_domain = seed_domain.replace("www.", "")
    if "." not in seed_domain:
        seed_domain += ".com"

    st.session_state.enriched_leads = None 
    
    with st.status(f"Running Pipeline for {seed_domain}...", expanded=True) as status:
        
        st.write("Finding lookalike companies...")
        lookalikes = get_companies(seed_domain)[:3] 
        
        if not lookalikes:
            status.update(label="No lookalikes found.", state="error")
            st.stop()

        st.write(f"Extracting decision-makers from {len(lookalikes)} domains...")
        all_leads = []
        for domain in lookalikes:
            leads = find_contacts(domain)
            if leads:
                all_leads.extend(leads)
            time.sleep(1.5)
            
        if not all_leads:
            status.update(label="No decision-makers found.", state="error")
            st.stop()

        st.write("Resolving verified work emails...")
        enriched_leads = []
        for lead in all_leads:
            email = get_email(lead['linkedin_url'], lead['name'], lead['company_domain'])
            if email:
                lead['email'] = email
                enriched_leads.append(lead)
            time.sleep(2)
            
        st.session_state.enriched_leads = enriched_leads
        status.update(label="Pipeline extraction complete!", state="complete", expanded=False)

if st.session_state.enriched_leads:
    st.divider()
    st.subheader("Safety Checkpoint")
    st.markdown(f"Found **{len(st.session_state.enriched_leads)}** verified leads.")
    
    st.dataframe(
        st.session_state.enriched_leads,
        column_config={
            "name": "Full Name",
            "company_domain": "Company", 
            "email": "Verified Email",
            "linkedin_url": st.column_config.LinkColumn("LinkedIn")
        },
        hide_index=True,
        use_container_width=True
    )

    st.warning("All emails will be routed to your personal inbox for testing.")
    if st.button("Fire Outreach Emails", type="primary"):
        with st.spinner("Dispatching intercepted emails..."):
            for lead in st.session_state.enriched_leads:
                send_email(lead['email'], lead['name'], lead['company_domain'])
                time.sleep(1)
        
        st.success("Demo complete! Check your personal inbox.")
        st.balloons()
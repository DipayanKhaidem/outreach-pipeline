from services import ocean

if __name__=="__main__":
    seed="stripe.com"

    print(f"Starting test for {seed}... \n")

    lookalikes=ocean.get_companies(seed,4)
    if lookalikes:
        print(f"Success! Found {len(lookalikes)} domains:")
        for domain in lookalikes:
            print(f"-{domain}")
    else:
        print("failed:no domains or error")
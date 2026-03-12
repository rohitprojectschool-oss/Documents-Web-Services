import requests
import json
import getpass
import sys

# Common SAP BTP Trial/Free Regions
REGIONS = ["us10", "eu10", "us20", "eu20", "us10-001", "eu10-001"]

def wake_up():
    print("\n🚀 SAP HANA Cloud 'Final Attempt' Wake-Up")
    print("-----------------------------------------")
    email = input("SAP ID Email: ")
    password = getpass.getpass("SAP Password: ")

    token = None
    found_api = None

    for reg in REGIONS:
        print(f"📡 Trying region {reg}...")
        uaa_url = f"https://login.cf.{reg}.hana.ondemand.com/oauth/token"
        
        try:
            r = requests.post(uaa_url, data={
                "grant_type": "password",
                "username": email,
                "password": password,
                "client_id": "cf",
                "client_secret": ""
            }, timeout=5)
            
            if r.status_code == 200:
                token = r.json()["access_token"]
                found_api = f"https://api.cf.{reg}.hana.ondemand.com"
                print(f"✅ Logged in to {reg}!")
                break
        except:
            continue

    if not token:
        print("❌ Login failed. Check your password.")
        return

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Fetch all service instances globally for this user in this region
    print("🔍 Searching for HANA instances...")
    r = requests.get(f"{found_api}/v3/service_instances", headers=headers)
    
    if r.status_code != 200:
        print(f"❌ Could not fetch instances: {r.text}")
        return

    instances = r.json().get("resources", [])
    target = None
    for inst in instances:
        name = inst["name"].lower()
        if "hana" in name and "tool" not in name:
            target = inst
            break
    
    if not target:
        print("❌ No HANA database found. Found these instead:")
        for inst in instances: print(f" - {inst['name']}")
        return

    print(f"✅ FOUND: {target['name']} ({target['guid']})")

    # Start it
    print("⚡ Waking up...")
    payload = {"parameters": {"data": {"status": "running"}}}
    r = requests.patch(f"{found_api}/v3/service_instances/{target['guid']}", 
                       headers=headers, data=json.dumps(payload))
    
    if r.status_code in [200, 202, 204]:
        print("\n🎉 SUCCESS! DB is starting. See you in 5 mins!")
    else:
        print(f"⚠️ Response: {r.text}")

if __name__ == "__main__":
    wake_up()

import os
import base64
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
OAUTH2_URL = f"{os.getenv('OAUTH2_BASE_URL')}/token"
API_BASE_URL = os.getenv("API_BASE_URL")

def get_access_token():
    auth_bytes = f"{CLIENT_ID}:{CLIENT_SECRET}".encode("ascii")
    base64_auth = base64.b64encode(auth_bytes).decode("ascii")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64_auth}"
    }
    data = {"grant_type": "client_credentials", "scope": "product.compact"}
    response = requests.post(OAUTH2_URL, headers=headers, data=data)
    response.raise_for_status()
    return response.json().get("access_token")

def get_item_info(search_term, zip_code=None, limit=5): # Added limit parameter
    token = get_access_token()
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    location_id = None
    if zip_code:
        loc_endpoint = f"{API_BASE_URL}/v1/locations"
        loc_params = {"filter.zipCode.near": zip_code, "filter.limit": 1}
        loc_res = requests.get(loc_endpoint, headers=headers, params=loc_params)
        loc_res.raise_for_status()
        data = loc_res.json().get("data", [])
        if data:
            location_id = data[0]["locationId"]

    prod_endpoint = f"{API_BASE_URL}/v1/products"
    prod_params = {
        "filter.term": search_term,
        "filter.limit": limit # Increased the limit 
    }
    
    if location_id:
        prod_params["filter.locationId"] = location_id

    response = requests.get(prod_endpoint, headers=headers, params=prod_params)
    response.raise_for_status()
    return response.json()

def append_list_to_json(new_entries):
    filename = 'data.json'
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except:
                data = []
    else:
        data = []

    # Add the whole list of new entries
    data.extend(new_entries)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ Successfully added {len(new_entries)} items to {filename}!")

if __name__ == "__main__":
    search_term = input("Product Name: ")
    zip_code = input("Zip Code: ")
    
    print(f"Searching Kroger for '{search_term}'...")
    product_data = get_item_info(search_term, zip_code, limit=5) # Requesting top 5
    
    all_new_items = []
    items_found = product_data.get('data', [])

    for item in items_found:
        try:
            name = item['description']
            #  check the first item in the product data
            price_info = item['items'][0].get('price')
            
            if price_info:
                price_val = price_info.get('promo', price_info.get('regular'))
                price = f"${price_val}"
                
                entry = {
                    "name": name,
                    "price": price,
                    "store": "Kroger",
                    "zip": zip_code,
                    "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                all_new_items.append(entry)
                print(f"Found: {name} | {price}")
        except (IndexError, KeyError):
            continue # Skip items that don't have price data

    if all_new_items:
        append_list_to_json(all_new_items)
    else:
        print("❌ No items with prices were found.")
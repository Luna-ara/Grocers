import os
import base64
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL="https://api.kroger.com"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
OAUTH2_URL = f"{os.getenv('OAUTH2_BASE_URL')}/token"
#API_BASE_URL = os.getenv("API_BASE_URL")

def get_access_token():
    credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    response = requests.post(OAUTH2_URL, headers={
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }, data={"grant_type": "client_credentials", "scope": "product.compact"})
    response.raise_for_status()
    return response.json()["access_token"]
def get_store_id(token, zipcode): 
    token = get_access_token()
    response = requests.get(f"{API_BASE_URL}/v1/locations", headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }, params={
        "filter.zipCode.near": zipcode,
        "filter.limit": 1
    })
    response.raise_for_status()
    locations = response.json().get("data", [])
    if not locations:
        raise Exception(f"No Kroger stores found near 80240")
    store = locations[0]
    print(f"  Store: {store['name']} — {store['address']['addressLine1']}, {store['address']['city']}")
    return store["locationId"]
def get_kroger_product_data(token ,productName, zipcode):
    lowest_price = float('inf')
    lowest_priced_item = {}
    print("🔐 Getting access token...")
    token = get_access_token()
    print("✅ Token received!\n")
    store_id = get_store_id(token, zipcode)

    print("🔍 Searching for products near", zipcode, "...")
    response = requests.get(f"{API_BASE_URL}/v1/products", headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }, params={
        "filter.term": productName,
        "filter.locationId": store_id,
        "filter.limit": 10
    })
    response.raise_for_status()
    products = response.json().get("data", [])
    
    for p in products:
        items = p.get("items", [])
        #print(f"  - {p.get('description')} | Brand: {p.get('brand', 'N/A')} | Price: {items[0].get('price', {}).get('regular', 'N/A')}")
        if (items[0].get('price', {}).get('regular', float('inf')) < lowest_price or items[0].get('price', {}).get('promo', float('inf')) < lowest_price):
            lowest_price = min(items[0].get('price', {}).get('regular', float('inf')), items[0].get('price', {}).get('promo', float('inf')))
            lowest_priced_item = p
   
    print(f"Cheapest Product: {lowest_priced_item.get('description')} at ${lowest_price}")
    return {
        "description": lowest_priced_item.get('description', 'Unknown'),
        "price": lowest_price if lowest_price != float('inf') else None,
    }

        
if __name__ == "__main__":
    get_kroger_product_data()
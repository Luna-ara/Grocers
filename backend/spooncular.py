from flask import Flask, request, jsonify
from flask_cors import CORS 
import os
import requests
from dotenv import load_dotenv
from TargetScraping import get_target_prices
from Kroger import get_access_token
from Kroger import get_kroger_product_data
import json
load_dotenv()
app = Flask(__name__)
CORS(app) 

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.spoonacular.com/recipes"

#  search for recipes 
@app.route('/search-recipes', methods=['POST'])
def search_recipes():
    data = request.json
    search_term = data.get('meal') # This matches your JS: body: JSON.stringify({ meal: meal })
    
    search_url = f"{BASE_URL}/complexSearch"
    params = {"query": search_term, "number": 12, "apiKey": API_KEY}
    
    response = requests.get(search_url, params=params).json()
    return jsonify(response.get('results', []))

# get ingredients for the selected recipe 
@app.route('/get-meal-info', methods=['POST'])
def handle_scrape():
    # This receives the 'id' from the clicked recipe card
    data = request.json
    recipe_id = data.get('id')
    recipe_title = data.get('title')
    
    print(f"🍳 User selected: {recipe_title} (ID: {recipe_id})")
    info_url = f"{BASE_URL}/{recipe_id}/ingredientWidget.json"
    recipe_data = requests.get(info_url, params={"apiKey": API_KEY}).json()
    return jsonify(recipe_data)
@app.route('/compare-ingredient', methods=['POST'])
def compare_ingredient():
    data = request.get_json()
    target_total = 0
    kroger_total =0
    token = get_access_token()
    ingredients = data.get('ingredients', [])
    recipe_name = data.get('name', 'Unknown Recipe')
    zipcode = data.get('zipcode', '90001')
    print("recipe name:", recipe_name)
    ingName =[]
    target_items = []
    for item in ingredients:
        ingName.append(item['name'])
   #gets target prices 
    idk =get_target_prices(ingName, zipcode)
    # Loop through the dictionary keys and values
    for ingredient, details in idk.items():
        target_total += details['price']
        print(f"Item: {ingredient:<20} | Brand: {details['brand_name']:<30} | Price: ${details['price']}")
        target_items.append({
            "name": ingredient,
            "brand": details['brand_name'],
            "price": details['price']
        })
    print(f"\nTotal estimated cost for Target '{recipe_name}': ${target_total:.2f}")
    #kroger price 
    kroger_items = []
    for item in ingName:
        
        kroger_result = get_kroger_product_data(token,  item , zipcode)
        kroger_total += kroger_result['price']
        kroger_items.append({
            "name": item,
            # Adjust 'brand_name' depending on what your kroger_result actually returns
            "brand": kroger_result.get('brand', 'Unknown Brand'), 
            "price": kroger_result['price']
        })

    print(f"Total Kroger Cost: ${kroger_total:.2f}")




    return jsonify({
        "status": "success",
        "recipe_name": recipe_name,
        "target": {
            "total": round(target_total, 2),
            "items": target_items
        },
        "kroger": {
            "total": round(kroger_total, 2),
            "items": kroger_items
        }
    })
    

if __name__ == '__main__':
    #app.run(port=5000, debug=True, use_reloader=False)
    app.run(port=5000, debug=True)
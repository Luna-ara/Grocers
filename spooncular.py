from flask import Flask, request, jsonify
from flask_cors import CORS 
import os
import requests
from dotenv import load_dotenv
from TargetScraping import get_target_prices

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

# --- get ingredients for the selected recipe ---
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
    data = request.json
    ingredient_name = data.get('ingredient')
    
    print(f"🚀 Scraping Target for: {ingredient_name}")
    
    # We call the function imported from TargetScraping.py
    # Note: I'm using the 'get_target_prices' you imported at the top
    try:
        prices = get_target_prices(ingredient_name) 
        return jsonify(prices)
    except Exception as e:
        print(f"Scraper error: {e}")
        return jsonify([])

if __name__ == '__main__':
    #app.run(port=5000, debug=True, use_reloader=False)
    app.run(port=5000, debug=True)
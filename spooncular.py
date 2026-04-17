import requests
import os
from dotenv import load_dotenv
from TargetScraping import get_target_prices
load_dotenv()

# Use the exact name from your .env file
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.spoonacular.com/recipes"

def get_recipe_ingredients(recipe_name):
    # Step 1: Search for the recipe ID
    search_url = f"{BASE_URL}/complexSearch"
    params = {"query": recipe_name, "number": 1, "apiKey": API_KEY}
    
    response = requests.get(search_url, params=params).json()
    if 'results' not in response:
        print("--- API ERROR ---")
        print(response) # This will show us if the key is wrong or points are out
        return None

    if not response['results']:
        print("No recipes found for that name.")
        return None
    
    recipe_id = response['results'][0]['id']

    # Step 2: Get the specific ingredients by ID
    info_url = f"{BASE_URL}/{recipe_id}/ingredientWidget.json"
    ingredients_resp = requests.get(info_url, params={"apiKey": API_KEY}).json()
    
    return ingredients_resp['ingredients']

# Example usage
ingredients = get_recipe_ingredients("Pasta Carbonara")
all_grocery_data = {}
for item in ingredients:
    # Extract the name string to use as the key
    ingredient_name = item['name'] if isinstance(item, dict) else item
    
    print(f"🎀 Scraping prices for: {ingredient_name}")
    target_data = get_target_prices(ingredient_name)
    
    # Use the string as the key, not the whole dict
    all_grocery_data[ingredient_name] = target_data

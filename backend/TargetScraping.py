import csv
from datetime import datetime
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import undetected_chromedriver as uc 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
def get_target_prices(search_term,zipcode):
   final_winners_dict = {}
   
   
   
   options = uc.ChromeOptions()
   options.add_argument('--headless') #comment this out if you want to see the browser in action
   driver = uc.Chrome(options=options)

   try:
        scraped_results = []
        url = f"https://www.target.com/s?searchTerm={search_term[0]}"
        driver.get(url)
        time.sleep(5)
        wait = WebDriverWait(driver, 10)
        # find the store button
        store_locator = wait.until(EC.element_to_be_clickable((By.ID, "web-store-id-msg-btn")))
        driver.execute_script("arguments[0].click();", store_locator)
        #insert the zip code to find the store
        try:
            store_zip = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-test="zip-code-search-input"]')))
        except:
            # Fallback: Find any input that mentions "zip" in its ID or Name
            store_zip = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[id*="zip"], input[name*="zip"]')))
       
        time.sleep(0.5) 
        for digit in zipcode:
            store_zip.send_keys(digit)
            time.sleep(0.1) # Wait 100ms between each number
        time.sleep(0.5) 
        store_zip.send_keys(Keys.ENTER)
       
        #look up button
        try:
            look_up = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test*="Lookup"]'))
            )
            look_up.click()
        except:
            # If the button isn't found
            print("Look up button not found or not needed, moving on...")

        #selects the first store from the list
        shop_this_store = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="@web/StoreMenu/ShopThisStoreButton"]')))
        time.sleep(0.5)  # Just to ensure the button is fully interactable
        driver.execute_script("arguments[0].click();", shop_this_store)

        #shop in store
        try:
            is_active = driver.find_elements(By.CSS_SELECTOR, 'button[data-test="facet-card-Shop in store"] #icon-x-mark')
            if len(is_active) == 0:
                print("Targeting: 'Shop in store' is NOT active. Clicking now...")
                # Find the button
                shop_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test="facet-card-Shop in store"]')))
                # Scroll and use the JavaScript click
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", shop_btn)
                time.sleep(1) 
                driver.execute_script("arguments[0].click();", shop_btn)
                print("Successfully activated 'Shop in store' mode!")
                time.sleep(3) # Give the page a few seconds to refresh the results
            else:
                print("'Shop in store' mode is already active. Skipping click to save time.")

        except Exception as e:
            print(f"Still having trouble finding the button: {e}")
        time.sleep(2)
        print("Currently shopping at this store:", driver.find_element(By.CSS_SELECTOR, 'div[data-test="@web/StoreName/StoreName"]').get_attribute("textContent").strip())
        # loop through every item in ingredient list. 
        for i in range(len(search_term)):
            lowest_price = float('inf')
            cheapest_item_data = None
            print("searching for", search_term[i])
            url = f'https://www.target.com/s?searchTerm={search_term[i]}'
            
            driver.get(url)
            results = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="product-grid"]')))
        
            time.sleep(1.5)  # Give the site a second to load the new images/prices
            products = driver.find_elements(By.CSS_SELECTOR, 'div[data-test="@web/site-top-of-funnel/ProductCardWrapper"]')
            print(f"Found {len(products)} products! Here are the details:\n")
            print(f"{'PRODUCT NAME':<50} | {'PRICE'}")
            print("-" * 65)
            for item in products:
                #get picture
                try:
                    name = item.find_element(By.CSS_SELECTOR, '[data-test="@web/ProductCard/title"]').get_attribute('innerText')
                    price = item.find_element(By.CSS_SELECTOR, '[data-test="current-price"]').get_attribute('innerText')
                    if search_term[i].lower() not in name.lower():
                        continue
                    try:
                        # We look for the image tag inside the current product card
                        img_element = item.find_element(By.CSS_SELECTOR, 'picture img')
                        image_url = img_element.get_attribute('src')
                    except:
                        image_url = "https://via.placeholder.com/50" # Fallback if no image found
                    if name and price:
                        print(f"{name[:47] + '...':<50} | {price}")
                        priceNum = float(price.replace('$', '').strip())
                        if priceNum < lowest_price:
                            lowest_price = priceNum  # Update the "score to beat"
                            cheapest_item_data = {
                            "brand_name": name,
                            "price": priceNum,
                            "store": "Target"
                            }
                            
                except:
                    continue
            if cheapest_item_data:
                final_winners_dict[search_term[i]] = cheapest_item_data
                print(f"Cheapest {search_term[i]} found: {cheapest_item_data['brand_name']} for ${lowest_price}")
        return final_winners_dict
        # with open('data.json', 'w', encoding='utf-8') as f:
    
        #     json.dump(scraped_results, f, indent=4, ensure_ascii=False)

   finally:
        driver.quit()
        pass
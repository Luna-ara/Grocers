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
def get_target_prices(search_term):
    #  Setup Portable Chrome Options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        scraped_results = []
        url = 'https://www.target.com'
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        # find the store button
        store_locator = wait.until(EC.element_to_be_clickable((By.ID, "web-store-id-msg-btn")))
        driver.execute_script("arguments[0].click();", store_locator)
        #insert the zip code to find the store
        store_zip = wait.until(EC.visibility_of_element_located((By.ID, "zip-code-city-or-state")))
        zip_code = '80204'
        for digit in zip_code:
            store_zip.send_keys(digit)
            time.sleep(0.1) # Wait 100ms between each number
        time.sleep(0.5) 
        store_zip.send_keys(Keys.ENTER)
        # #look up button
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

        #Find the search box
        q = driver.find_element(By.ID, "search")
        q.send_keys(search_term)
        q.submit()
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
        results = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="product-grid"]')))
        
        print("Scrolling to load all products...")

        # Scroll down multiple times 
        for _ in range(5):  
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(1.5)  # Give the site a second to load the new images/prices

        # Final scroll to the very bottom to catch the stragglers
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        products = driver.find_elements(By.CSS_SELECTOR, 'div[data-test="@web/site-top-of-funnel/ProductCardWrapper"]')
        print(f"Found {len(products)} products! Here are the details:\n")
        print(f"{'PRODUCT NAME':<50} | {'PRICE'}")
        print("-" * 65)
        for item in products:
            try:
                name = item.find_element(By.CSS_SELECTOR, '[data-test="@web/ProductCard/title"]').get_attribute('innerText')
                price = item.find_element(By.CSS_SELECTOR, '[data-test="current-price"]').get_attribute('innerText')
                try:
                    # We look for the image tag inside the current product card
                    img_element = item.find_element(By.CSS_SELECTOR, 'picture img')
                    image_url = img_element.get_attribute('src')
                except:
                    image_url = "https://via.placeholder.com/50" # Fallback if no image found
                if name and price:
                    print(f"{name[:47] + '...':<50} | {price}")
                    product_entry = {
                    "name": name.strip(),
                    "price": price.strip(),
                    "image_url": image_url,
                    "store": "Target",
                    "zip": "80204",
                    "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                    scraped_results.append(product_entry)
                else:
                    continue
                    
            except:
                continue
        with open('data.json', 'w', encoding='utf-8') as f:
    
            json.dump(scraped_results, f, indent=4, ensure_ascii=False)

    finally:
        pass
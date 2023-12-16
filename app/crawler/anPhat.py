# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set path to chromedriver as per your configuration
webdriver_service = Service('/Users/minh/Minh-Codespace/chromedrive/chromedriver')

# Choose Chrome Browser
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
wait = WebDriverWait(driver, 70)

# Loop through pages 1 to 3
for page in range(1, 10):
    driver.get(f"https://www.anphatpc.com.vn/may-tinh-xach-tay-laptop.html?max=20000000&page={page}")

    # Wait for the page to fully load
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section")))

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find all the product elements using CSS selector
    productElements = soup.select("div.product-list-container.bg-white > div.p-list-container.d-flex.flex-wrap > div")

    # Loop through each product element and find the laptop name, price, config, link, promo info and description using CSS selector
    for i, product in enumerate(productElements):
        laptopName = product.select_one("div.p-text > a > h3").text.strip()
        laptopPrice = product.select_one("div.p-text > div.price-container > span.p-price").text.strip()
        laptopConfig = product.select_one("div.p-text > div.box-config").text.strip()
        laptopLink = "https://www.anphatpc.com.vn" + product.select_one("div.p-text > a").get('href')

        print(f"Crawling data for: {laptopName}")

        # Navigate to the laptopLink page
        driver.get(laptopLink)

        print(f"Accessed page: {laptopLink}")

        # Wait for the page to fully load
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section")))

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find the promo price information using CSS selector
        promoPriceInfo = soup.select_one("section > div.container > div.bg-white.product-info-container > div.pro-info-center > div.pro_info-price-container > table")

        # If the promo price information exists, get the text, otherwise, set it to an empty string
        promoPriceText = promoPriceInfo.text.strip() if promoPriceInfo else ""

        # Find the special offer information using CSS selector
        specialOfferInfo = soup.select_one("section > div.container > div.bg-white.product-info-container > div.pro-info-center > div.pro-special-offer-container")

        # If the special offer information exists, get the text, otherwise, set it to an empty string
        specialOfferText = specialOfferInfo.text.strip() if specialOfferInfo else ""

        # Find the product description using CSS selector
        productDescriptionInfo = soup.select_one("section > div.container > div.pro-desc-spec-container.bg-white.clearfix > div.item.item-desc.js-static-container > div.overflow-hidden.js-static-content")

        # If the product description exists, get the text, otherwise, set it to an empty string
        productDescriptionText = productDescriptionInfo.text.strip() if productDescriptionInfo else ""

        # Create a dictionary to store the data
        data = {
            'name': laptopName,
            'price': laptopPrice,
            'config': laptopConfig,
            'link': laptopLink,
            'promo_price': promoPriceText,
            'special_offer': specialOfferText,
            'description': productDescriptionText
        }

        print(data)
        print(f"Collected data for: {laptopName}")

        # Write the data to a JSON file
        with open(f'anphatpc/anphatpc_{page}_{i}.json', 'w') as f:
            json.dump(data, f)

        print(f"Saved data to: anphatpc/anphatpc_{page}_{i}.json")

driver.quit()

print("Finished crawling.")
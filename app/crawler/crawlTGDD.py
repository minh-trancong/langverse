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

driver.get("https://www.thegioididong.com/laptop#c=44&o=17&pi=13")

# Wait for the page to fully load
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#categoryPage")))

soup = BeautifulSoup(driver.page_source, "html.parser")

# Find the category page element using CSS selector
categoryPage = soup.select_one("#categoryPage")

# Find all the product box elements inside the category page element using CSS selector
productBoxList = categoryPage.select("div.container-productbox > ul > li")

# Create a list to store the data
data = []

# Loop through each product box element and find the laptop name, link and price using CSS selector
for i, productBox in enumerate(productBoxList):
    laptopName = productBox.select_one("a.main-contain > h3").text.strip()
    laptopLink = "https://thegioididong.com" + productBox.select_one("a.main-contain")['href']
    laptopPrice = productBox.select_one("a.main-contain")['data-price']

    print(f"Crawling data for: {laptopName}")

    # Navigate to the laptopLink page
    driver.get(laptopLink)

    print(f"Accessed page: {laptopLink}")

    # Wait for the page to fully load
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.detail")))

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find the promo information using CSS selector
    promoInfo = soup.select_one("section.detail > div.box_main > div.box_right > div.box04.box_normal > div.block.block-price1 > div.block__promo")

    # If the promo information exists, get the text, otherwise, set it to an empty string
    promoText = promoInfo.text.strip() if promoInfo else ""

    # Find the configuration information using CSS selector
    configInfoList = soup.select("section.detail > div.box_main > div.box_right > div.parameter > ul > li")

    # If the configuration information exists, get the text of each item, otherwise, set it to an empty list
    configTextList = [item.text.strip() for item in configInfoList] if configInfoList else []

    # Create a dictionary to store the data
    data = {
        'name': laptopName,
        'link': laptopLink,
        'price': laptopPrice,
        'promo': promoText,
        'config': configTextList
    }

    print(data)
    print(f"Collected data for: {laptopName}")

    # Write the data to a JSON file
    with open(f'tgdd/tgdd_{i}.json', 'w') as f:
        json.dump(data, f)

    print(f"Saved data to: tgdd/data_{i}.json")

driver.quit()

print("Finished crawling.")
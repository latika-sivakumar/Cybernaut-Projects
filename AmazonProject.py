import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

chrome_options = Options()  
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

def fetch_product_data(search_query,pages):
    url = f"https://www.amazon.in/s?k={search_query}{pages}"
    driver.get(url)
    time.sleep(2)  
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    product_data = []
    for product in products:
        title = product.h2.text.strip() if product.h2 else "N/A"    
        price = product.find('span', 'a-price-whole')
        price = price.text.strip() if price else "N/A"
        rating = product.find('span', 'a-icon-alt')
        rating = rating.text.strip() if rating else "N/A"     
        reviews = product.find('span', 'a-size-base')
        reviews = reviews.text.strip() if reviews else "N/A"
        image = product.find('img', {'class': 's-image'})
        image_url = image['src'] if image else "N/A"
        product_data.append({
            'Title': title,
            'Price': price,
            'Rating': rating,
            'Reviews': reviews,
            'Image URL': image_url})
    return product_data

def main():
    search_query = "Titan Women Watches"  
    pages=5
    product_data = fetch_product_data(search_query,pages)
    csv_file_path = r'C:\Users\latik\OneDrive\Documents\Project\amazon_products.csv'
    df = pd.DataFrame(product_data)
    df.to_csv(csv_file_path, index=False)
    print(f"Scraping completed and data saved to {csv_file_path}")
    time.sleep(60)  

if __name__ == "__main__":
    main()
    driver.quit()
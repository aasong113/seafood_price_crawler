from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time

# specify the location of the chromedriver, I just put it in my local.
driver = webdriver.Chrome(r"/Users/xzhao/PycharmProjects/ScrapyTutorial/chromedriver")

# Json writer
def writ_json(f_name, data):
    with open('Pikes_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_parser(base_url):
    driver.get(baseurl)
    time.sleep(30)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup

# Collect Sams
def get_sams(base_url):
    soup = get_parser(base_url)

    store_name = str(soup.find_all('title')[0].text.strip())
    product_name = str(soup.find_all('h1', class_ = "")[0].text.strip())
    price_group = str(soup.find_all('span', class_ = "Price-group")[0].text.strip())
    product_price = price_group.split(" ")[2].split("/")[0]

    return store_name, product_name, product_price

# Collect Pike Place Fish
def get_pike(base_url):
    soup = get_parser(base_url)

    store_name = str(soup.find_all('title')[0].text.strip())
    product_name = str(soup.find_all('h1', class_ = "fs-7 fs-md-8 spec__product__name")[0].text.strip())
    product_price = str(soup.find_all('h3', class_ = "fs-8 fs-lg-10 spec__product-price")[0].text.strip())
    
    return store_name, product_name, product_price

if __name__ == '__main__':

    input_data = {
		    "sams": {
                "king_crab": "https://www.samsclub.com/p/star-cut-wild-king-crab-legs/prod22261087"
            },
            "pikes": {
                "king_crab": "https://pikeplacefishseattle.goldbelly.com/alaskan-king-crab-legs-and-claws-by-the-pound?ref=collection"
            }
            }
    out_data = {}

    for key, value in input_data.items():
        if key not in out_data:
            out_data[key] = {}


        for key, value in input_data.items():
            if key == "sams":
                for product, url in value.items():
                    store_name, product_name, product_price = get_sams(url)
                    out_data[store_name] = product_price
            if key == "pikes":
                for product, url in value.items():
                    store_name, product_name, product_price = get_pike(url)
                    out_data[store_name] = product_price

    from datetime import date
    
    today = date.today()
    today = today.strftime("%b-%d-%Y")

    writ_json('seafood_price_'+ str(today)+ '.json', out_data)





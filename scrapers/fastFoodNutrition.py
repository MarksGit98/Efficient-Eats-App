from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
from main import save_into_excel_db

RESTAURANT_LIST_URL = 'https://fastfoodnutrition.org/fast-food-restaurants'
BASE_URL = "https://fastfoodnutrition.org"
PRODUCTS = "/home/products/category/food-8"

def compile_restaurant_list(browser):
    restaurants = []
    browser.get(RESTAURANT_LIST_URL)
    time.sleep(3)
    try:
        browser.execute_script("window.scrollTo(0, 2000);")
        time.sleep(1)
        source = browser.page_source
        soup = BeautifulSoup(source.encode('utf-8'), 'html.parser')
        items = soup.find_all(class_='filter_target')
        
        for item in items:
            
            try:
                if item.text:
                    restaurants.append(item.text.replace('Nutrition', '').strip().replace(' ', '-').replace("'", ""))
            except:
                continue
    except:
        return []
    
    return restaurants

def compile_item_list(restaurants, browser):
    item_href_dict = {}

    for restaurant in restaurants:
        print(restaurant)
        nutrition_dict = {}   
        browser.get(BASE_URL+'/'+restaurant)
        time.sleep(3)
        try:
            #CONTINUE FROM HERE
            browser.execute_script("window.scrollTo(0, 3000);")
            time.sleep(1)
            source = browser.page_source
            soup = BeautifulSoup(source.encode('utf-8'), 'html.parser')
            items = soup.find_all(class_='active_item_link')
            for item in items:
                try:
                    a_href = item.get('href').strip()
                    print(a_href)
                    item_text = item.get('title')
                    item_text = str(item_text).strip("b'").replace('Nutrition Facts', '').strip()
                    print(item_text)
                    nutrition_dict[item_text] = a_href
                except:
                    continue
        except:
            continue
            
        item_href_dict[restaurant] = nutrition_dict
    return item_href_dict

def generate_nutrition_database(item_href_dict, browser):
    item_dict = {}
    
    for restaurant in item_href_dict:
        nutrition_dict = {}
        for item in item_href_dict[restaurant]:
            href = item_href_dict[restaurant][item]
            url= f'{BASE_URL}{href}'
            browser.get(url)
            time.sleep(2)
            try:
                #CONTINUE FROM HERE
                browser.execute_script("window.scrollTo(0, 3000);")
                time.sleep(1)
                more_options_available = browser.find_element(By.XPATH, "//*[contains(text(), 'Select a size to see full nutrition facts')]")

                if not more_options_available:
                    nutrition_label = parse_nutrition_label(browser)
                    nutrition_dict[item] = nutrition_label
                    print(nutrition_label)
                else:
                    options = browser.find_elements(By.CLASS_NAME, 'stub_box')
                    alt_hrefs = []
                    for option in options:
                        alt_hrefs.append(option.get_attribute('href'))

                    for href in alt_hrefs:
                        browser.get(href)
                        time.sleep(2)
                        nutrition_label = parse_nutrition_label(browser)
                        item = browser.find_element(By.TAG_NAME, 'h1').text.replace('Nutrition Facts', '').strip()
                        print(item)
                        nutrition_dict[item] = nutrition_label
                        
            except: 
                continue
    
        item_dict[restaurant] = nutrition_dict
    return item_dict
            
def parse_nutrition_label(browser):
    nutrition_label = browser.find_element(By.CSS_SELECTOR, "table").text.split("\n")
    #PARSE NUTRITION LABEL AND PUT ALL ELEMENTS OF IT IN A DICTIONARY AND RETURN THAT DICTIONARY
    print(nutrition_label)
    return (nutrition_label)

example_restaurants = ['subway']
browser = webdriver.Chrome(ChromeDriverManager().install())
# restaurants = compile_restaurant_list(browser)
item_href_dict = compile_item_list(example_restaurants, browser)
print(item_href_dict)
item_dict = generate_nutrition_database(item_href_dict, browser)
print(item_dict)
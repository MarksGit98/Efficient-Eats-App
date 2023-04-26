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
    nutrition_dict = {}
    nutrition_label = browser.find_element(By.CSS_SELECTOR, "table").text.split("\n")
    try:
        nutrition_dict['Serving Size'] = nutrition_label[0].split(' ')[2]
    except:
        pass
    try:
        nutrition_dict['Calories'] = float(nutrition_label[1].split(' ')[1])
    except:
        pass
    try:
        nutrition_dict['Total Fat (g)'] = float(nutrition_label[4].split(' ')[2].strip('g'))
    except:
        pass
    try:
        nutrition_dict['Saturated Fat (g))'] = float(nutrition_label[5].split(' ')[2].strip('g'))
    except:
        pass
    try:
        nutrition_dict['Trans Fat (g)'] = float(nutrition_label[6].split(' ')[2].strip('g'))
    except:
        pass
    try:
        nutrition_dict['Cholesterol (mg)'] = float(nutrition_label[7].split(' ')[1].strip('mg'))
    except:
        pass
    try:
        nutrition_dict['Sodium (mg)'] = float(nutrition_label[8].split(' ')[1].strip('mg'))
    except:
        pass
    try:
        nutrition_dict['Carbohydrates (g)'] = float(nutrition_label[9].split(' ')[2].strip('g'))
    except:
        pass
    try:
        nutrition_dict['Dietary Fiber'] = float(nutrition_label[10].split(' ')[2].strip('g'))
    except:
        pass
    try:
        nutrition_dict['Sugars (g)'] = float(nutrition_label[11].split(' ')[1].strip('g'))
    except:
        pass
    try:
        nutrition_dict['Protein (g)'] = float(nutrition_label[12].split(' ')[1].strip('g'))
    except:
        pass
    try:
        nutrition_dict['Vitamin A'] = nutrition_label[13].split(' ')[2]
    except:
        pass
    try:
        nutrition_dict['Vitamin C'] = nutrition_label[14].split(' ')[2]
    except:
        pass
    try:
        nutrition_dict['Calcium'] = nutrition_label[15].split(' ')[1]
    except:
        pass
    try:
        nutrition_dict['Iron'] = nutrition_label[16].split(' ')[1]
    except:
        pass
    
    return (nutrition_dict)

example_restaurants = ['subway']
browser = webdriver.Chrome(ChromeDriverManager().install())
# restaurants = compile_restaurant_list(browser)
item_href_dict = compile_item_list(example_restaurants, browser)
print(item_href_dict)
item_dict = generate_nutrition_database(item_href_dict, browser)
print(item_dict)
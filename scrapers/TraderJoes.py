from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
from main import save_into_excel_db

HOME_URL = "https://www.traderjoes.com"
PRODUCTS = "/home/products/category/food-8"

def compile_item_list(browser):
    item_dict = {}
    browser.get(HOME_URL+PRODUCTS)
    time.sleep(3)
    page = True
    page_num = 1
    while page:
        try:
            browser.execute_script("window.scrollTo(0, 2000);")
            time.sleep(1)
            source = browser.page_source
            soup = BeautifulSoup(source.encode('utf-8'), 'html.parser')
            items = soup.find_all('h2')

            for item in items:
                try:
                    a_href = item.find('a').get('href')
                    item_text = item.text.encode('utf-8')
                    item_dict[item_text] = a_href
                except:
                    continue
            
            page_num +=1   
            button = browser.find_element(By.CSS_SELECTOR, f'[aria-label="Go to page {page_num}"]')
            print(button)
            button.click()
            time.sleep(3)
        except:
            page = False
    
    return item_dict

def generate_nutrition_database(item_dict, browser):
    item_nutrition_dict = {}
    for item in item_dict:
        browser.get(HOME_URL+item_dict[item])
        time.sleep(3)
        browser.execute_script("window.scrollTo(0, 1000);")
        try:
            nutrition_label = browser.find_element(By.CSS_SELECTOR, "table").text.split("\n")
            item_details = browser.find_element(By.CSS_SELECTOR, "div[class^='Item_characteristics']").text.split("\n")
            serving_size, calories_per_serving = item_details[1], item_details[3]
            nutrition_dict = {}
            #Add condition for LESS THAN 1 gram (extra spaces)
            try:
                nutrition_dict['Serving Size'] = serving_size
                nutrition_dict['Calories per Serving'] = calories_per_serving
                try:
                    for num in nutrition_label[1].split(' '):
                        if num.isnumeric():
                            nutrition_dict['Total Fat (g)'] = float(num)
                except:
                    nutrition_dict['Total Fat (g)'] = 0
                try:
                    for num in nutrition_label[2].split(' '):
                        if num.isnumeric():
                            nutrition_dict['Saturated Fat (g)'] = float(num)
                except:
                    nutrition_dict['Saturated Fat (g)'] = 0
                try:
                    for num in nutrition_label[3].split(' '):
                        if num.isnumeric():
                            
                            nutrition_dict['Trans Fat (g)'] = float(num)
                except:
                    nutrition_dict['Trans Fat (g)'] = 0
                try:
                    for num in nutrition_label[4].split(' '):
                        if num.isnumeric():
                            nutrition_dict['Cholesterol (mg)'] = float(num)
                except:
                    nutrition_dict['Cholesterol (mg)'] = 0
                try:
                    for num in nutrition_label[5].split(' '):
                        if num.isnumeric():
                            nutrition_dict['Sodium (mg)'] = float(num)
                except:
                    nutrition_dict['Sodium (mg)'] = 0
                try:
                    for num in nutrition_label[6].split(' '):
                        if num.isnumeric():
                            nutrition_dict['Total Carbohydrates (g)']  = float(num)
                except:
                    nutrition_dict['Total Carbohydrates (g)']  = 0
                try:
                    for num in nutrition_label[7].split(' '):
                        if num.isnumeric():
                            nutrition_dict['Dietary Fiber (g)'] = float(num)
                except:
                    nutrition_dict['Dietary Fiber (g)']  = 0
                try:
                    for num in nutrition_label[8].split(' '):
                        if num.isnumeric():
                            nutrition_dict['Total Sugars (g)'] = float(num)
                except:
                    nutrition_dict['Total Sugars (g)'] = 0
                try:
                    for num in nutrition_label[10].split(' '):
                        if num.isnumeric():
                            nutrition_dict['Protein  (g)'] = float(num)
                except:
                    nutrition_dict['Protein  (g)']  = 0
                try:
                    for num in nutrition_label[11].split(' '):
                        if num.isnumeric():
                            nutrition_dict['Vitamin D (mcg)'] = float(num)
                except:
                    nutrition_dict['Vitamin D (mcg)'] = 0
                try:
                    for num in nutrition_label[12].split(' '):
                        if num.isnumeric():
                            nutrition_dict['Calcium (mg)'] = float(num)
                except:
                    nutrition_dict['Calcium (mg)'] = 0
                try:
                    for num in nutrition_label[13].split(' '):
                        if num.isnumeric():
                            nutrition_dict['Iron (mg)'] = float(num)
                except:
                    nutrition_dict['Iron (mg)'] = 0
                try:
                    for num in nutrition_label[14].split(' '):
                        if num.isnumeric():
                            nutrition_dict['Potassium (mg)'] = float(num)
                except:
                    nutrition_dict['Potassium (mg)'] = 0

            except:
                continue

            item_nutrition_dict[str(item).strip("b'")] = nutrition_dict
            print(item_nutrition_dict)
        except:
            continue
        print(item_nutrition_dict)
    return item_nutrition_dict
            
example_dict = {'Avocado Mash': {'Serving Size': '2 Tbsp(30g)', 'Calories per Serving': '45', 'Trans Fat (g)': 0.0, 'Cholesterol (mg)': 0.0, 'Sodium (mg)': 90.0, 'Total Carbohydrates (g)': 3.0, 'Dietary Fiber (g)': 2.0, 'Total Sugars (g)': 0.0, 'Protein  (g)': 1.0, 'Calcium (mg)': 0.0, 'Potassium (mg)': 140.0},
                'Item 2': {'Serving Size': '2 Tbsp(30g)', 'Calories per Serving': '45', 'Trans Fat (g)': 0.0, 'Cholesterol (mg)': 0.0, 'Sodium (mg)': 90.0, 'Total Carbohydrates (g)': 3.0, 'Dietary Fiber (g)': 2.0, 'Total Sugars (g)': 0.0, 'Protein  (g)': 1.0, 'Calcium (mg)': 0.0, 'Potassium (mg)': 140.0}}


# save_into_excel_db(example_dict, 'Test2', 'Supermarket', 'append')

browser = webdriver.Chrome(ChromeDriverManager().install())
item_dict = compile_item_list(browser)
nutrtion_dict = generate_nutrition_database(item_dict, browser)
print(nutrtion_dict)
print(len(nutrtion_dict))
save_into_excel_db(nutrtion_dict, 'Trader Joes', 'Supermarket', 'overwrite')
browser.close()

#Save Data in an excel file

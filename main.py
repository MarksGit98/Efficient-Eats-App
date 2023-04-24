import openfoodfacts

search_result = openfoodfacts.products.search('McDonalds Big Mac')

print(search_result['products'])
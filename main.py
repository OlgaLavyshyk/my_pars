import requests
import csv

def fetch(url, cursor):
    if cursor != "":
        url = url + "&Cursor=" + str(cursor)
    return requests.get(url)

def collect_data(result):
    list = []
    product_list = result['productsList']
    for i in range(0, 20):
        application = product_list[i]
        productId = application['productId']
        list.append(productId)
    return list


base_url = "https://apps.microsoft.com/store/api/Products/GetFilteredProducts/?hl=ru-ru&gl=US&NoItems=24&Category=Business"
all_app = []

x = fetch(base_url, "")
result = x.json()

f = collect_data(result)
all_app += f
# print(f)

cursor = result['cursor']
# print(cursor)
for i in range(1,10):
    y = fetch(base_url, cursor)
    n = collect_data(y.json())
    all_app += n
    cursor = y.json()['cursor']
# print(all_app)


def fetch_detail(productID):
    url_datail = "https://apps.microsoft.com/store/api/ProductsDetails/GetProductDetailsById/" + str(productID) + "?hl=ru-ru&gl=US"
    r = requests.get(url_datail)
    result = r.json()
    app = []
    app.append(result["publisherName"])
    app.append(result["title"])
    app.append(result["releaseDateUtc"])
    app.append(result["supportUris"][0]["uri"])


    return app

list_headers = ["publisherName", "title", "releaseDateUtc", "supportUris"]

with open(file='table.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(list_headers)
    # print("done")

for id in all_app:
    t = fetch_detail(id)
    with open(file='table.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow(t)




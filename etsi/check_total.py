import requests
import json
import math 
# Function to get total count from a URL
def get_total_count(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            datas = response.json()
            for data in datas:
                total_count = data["total_count"]
                return total_count
        except json.JSONDecodeError:
            print(f"Invalid JSON response for URL: {url}")
            return 0
    else:
        print(f"HTTP error {response.status_code} for URL: {url}")
        return 0
def write_total(datas, filename):
    with open(filename, 'w') as file:
        json.dump(datas, file, indent=4)

with open('total.json', 'r') as file:
    datas = json.load(file)
for key, value in datas.items():
    url = value.get("url")
    if url:
        page = 1 
        formatted_url = url.format(page=page)
        total_count = get_total_count(formatted_url)
        value["total_count"] = math.ceil(int(total_count)/50)

write_total(datas, 'total.json')


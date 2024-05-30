import requests
from bs4 import BeautifulSoup 
link ='https://www.en-standard.eu/ieee-standards/'
response = requests.get(link)
soup = BeautifulSoup(response.text, 'html.parser')
level_1 =[element.get('href') for element in soup.find_all('a', class_='kat level1 selected open0')]
for lev in level_1 :
    print(lev)
import requests
from bs4 import BeautifulSoup
import time
def data_out(so_hieu=False, ten_tieng_anh=False, nam_ban_hanh=False, duong_link=False, mo_ta=False, linh_vuc=False, trang_thai='con_hieu_luc', trang_thai_khoi_tao='he_thong_craw', loai='kho'):
    return {
        "so_hieu": so_hieu,
        "ten_tieng_anh": ten_tieng_anh,
        "nam_ban_hanh": nam_ban_hanh,
        "duong_link": duong_link,
        "trang_thai": trang_thai,
        'mo_ta': mo_ta,
        'linh_vuc': linh_vuc,
        'trang_thai_khoi_tao': trang_thai_khoi_tao,
        'loai': loai,
    }
def get_all_level_1(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    level_1 =[element.get('href') for element in soup.find_all('a', class_='kat level1 selected open0')]
    return level_1
def check_level_and_get_standard(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    level_2 = [element.get('href') for element in soup.find_all('a', class_='kat level2 selected open0')]
    standard =[]
    if len(level_2)!= 0 :
        for level in level_2 :
            response= requests.get(level)
            soup = BeautifulSoup(response.text, 'html.parser')
            level_3  = [element.get('href') for element in soup.find_all('a', class_='kat level3 selected open0')]
            if len(level_3)!= 0 :
                for lev in level_3 :
                    standard += fetch_standard_data(lev)
            else :
                standard += fetch_standard_data(level)
    else :
        standard += fetch_standard_data(url)
    return standard
                    
                    
            
        
def get_page(url):
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    check = soup.find_all('span', class_= 'listcontrol')
    if len(check) != 0 :
        pages_span = soup.find('span', class_='pages')
        links = pages_span.find_all('a')
        link_list = [link['href'] for link in links]
        return len(link_list)
    else :
        return True 

def fetch_standard(page, url ):
    if page == 1 :
        return []
    elif page == 0 :
        return fetch_standard_data(url)
    else :
        url = url[:-1]
        newurl = f"{url}-page-{page}/"
        print(newurl)
        return fetch_standard_data(newurl)

def fetch_standard_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    all_links = [link['href'] for link in soup.select('a.katalogProduct__name')]
    standards = []
    
    for link in all_links:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.select_one('div.fleft.detail_right_side').get_text(strip=True)
        price = soup.select_one('div.detailVariants__price').get_text(strip=True)
        description = soup.find_all('div', class_='textFormat')
        descriptions = description[2].get_text(strip=True) if len(description) > 2 else 'n/a'
        date_pub = soup.select_one('.released').get_text(strip=True)
        
        standards.append(data_out(ten_tieng_anh=title, mo_ta=descriptions, nam_ban_hanh=date_pub))
        time.sleep(3)
    
    return standards 

def aiag_standard():
    url = "https://www.en-standard.eu/qs-9000/?mena=1"
    return fetch_standard_data(url)
def atsm(page):
    number_page ='https://www.en-standard.eu/astm-standards/'  
    url = number_page[page]
    return check_level_and_get_standard(url)
def csn(page):
    number_page= get_all_level_1('https://www.en-standard.eu/csn-standards/')
    url = number_page[page]
    return check_level_and_get_standard(url)
def bs(page):
    number_page = get_all_level_1('https://www.en-standard.eu/bs-standards/')
    url = number_page[page]
    return check_level_and_get_standard(url)
    
def eurocode(page):
    number_page = get_all_level_1('https://www.en-standard.eu/eurocodes/')
    url  = number_page[page]
    return check_level_and_get_standard(url)


#ok 

def CQI(page):
    url ='https://www.en-standard.eu/cqi/'
    return fetch_standard(page, url )
def DIN(page):
    url = 'https://www.en-standard.eu/din-standards/'
    return fetch_standard(page, url)
def IEC(page):
    url='https://www.en-standard.eu/iec-standards/'
    return fetch_standard(page, url)
def ISO(page):
    url ='https://www.en-standard.eu/iso-standards/'
    return fetch_standard(page, url)
def UNE(page):
    url ='https://www.en-standard.eu/une-standards/'
    return fetch_standard(page, url)
def VDA(page):
    url ='https://www.en-standard.eu/automotive-quality-standards-qs-9000/'
    return fetch_standard(page, url)
def set_of_en(page):
    url ='https://www.en-standard.eu/sets-of-en-standards/'
    return fetch_standard(page, url)
print(ISO(2098))
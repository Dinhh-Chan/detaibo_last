import requests 
from bs4 import BeautifulSoup
def data_out(so_hieu=False, ten_tieng_anh=False, nam_ban_hanh=False,duong_link=False,mo_ta = False, linh_vuc = False, trang_thai='con_hieu_luc',trang_thai_khoi_tao='he_thong_craw',loai='kho',tac_gia = False,gia = False  ):
    return {
    "so_hieu": so_hieu,
    "ten_tieng_anh" : ten_tieng_anh,
    # "nam_ban_hanh": format_datetime(nam_ban_hanh.strip()),
    "duong_link": duong_link,
    "trang_thai": trang_thai,
    'mo_ta':mo_ta,
    'linh_vuc':linh_vuc,
    'trang_thai_khoi_tao':trang_thai_khoi_tao,
    'loai':loai,
    }
def standard(url):
    standard=[]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    arr_link = []
    all_link = soup.find_all('h1', class_='h4 mb-2 Oswald text-capitalize tracking-tight')
    for link in all_link :
        arr_link.append("https://webstore.ansi.org"+link.find('a').get('href'))
    for link in arr_link:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        all_tieu_de = soup.find('h1', class_='h4 Oswald text-capitalize tracking-tight mt-0')
        if all_tieu_de != None: 
            all_tieu_de = all_tieu_de.get_text(strip=True).split('-')
            so_hieu = all_tieu_de[0]
            ten_tieng_anh = all_tieu_de[1] if len(all_tieu_de)> 1  else all_tieu_de[0]
        else :
            so_hieu='0'
            ten_tieng_anh= '0'
        prices = soup.find('a', class_="u-link-v5 text-dark text-uppercase" )
        if prices !=  None :
            price = prices.get_text(strip = True)
        else :
            price = '0'
        abstract = soup.find('p', class_= "font-16")
        if abstract != None :
            abstract = abstract.get_text(strip = True)
        else :
            abstract = '0'
        duong_link = link
        author = soup.find('span', class_ = "font-20 text-dark")
        if author != None :
            author = author.get_text(strip = True)
        else :
            author ='0'
        standard.append(data_out(so_hieu= so_hieu, ten_tieng_anh=ten_tieng_anh,gia = price,mo_ta=abstract, duong_link=duong_link, tac_gia= author))
    return standard
def Construction_Construction_Safety():
    url = "https://webstore.ansi.org/packages/construction"
    return standard(url)
def Occupational_Health_Safety ():
    url = "https://webstore.ansi.org/packages/occupational"
    return standard(url)
def Machine_Safety():
    url = "https://webstore.ansi.org/packages/machine-safety"
    return standard(url)

def Risk_Management():
    url = "https://webstore.ansi.org/packages/risk-management"
    return standard(url)

def Laboratories():
    url = "https://webstore.ansi.org/packages/laboratories"
    return standard(url)

def Cloud_Security():
    url = "https://webstore.ansi.org/packages/cloud"
    return standard(url)

def Energy_Management():
    url = "https://webstore.ansi.org/packages/energy-management"
    return standard(url)

def Industrial_Robotics():
    url = "https://webstore.ansi.org/packages/industrial-robotics"
    return standard(url)

def IEC_Series():
    url = "https://webstore.ansi.org/packages/iec-series"
    return standard(url)

def IEC_Redlines():
    url = "https://webstore.ansi.org/packages/iec-redline"
    return standard(url)

def Identity_Theft():
    url = "https://webstore.ansi.org/packages/identity-theft"
    return standard(url)

def NSF_Standards_Collections():
    url = "https://webstore.ansi.org/packages/nsf-food"
    return standard(url)

def Radio_Frequency_Disturbance():
    url = "https://webstore.ansi.org/packages/radio"
    return standard(url)

def Electronic_Communications():
    url = "https://webstore.ansi.org/packages/electronic-communications"
    return standard(url)

def ISO_Handbooks():
    url = "https://webstore.ansi.org/packages/iso-handbook"
    return standard(url)

def Certification():
    url = "https://webstore.ansi.org/packages/certification"
    return standard(url)

def Medical_Devices():
    url = "https://webstore.ansi.org/packages/medical"
    return standard(url)

def IT_IT_Security():
    url = "https://webstore.ansi.org/packages/it-security"
    return standard(url)

def Quality_Management():
    url = "https://webstore.ansi.org/packages/quality-management"
    return standard(url)

def Regenerative_Medicine():
    url = "https://webstore.ansi.org/packages/regenerative-medicine"
    return standard(url)

def Road_Vehicles():
    url = "https://webstore.ansi.org/packages/road-vehicles"
    return standard(url)

def Environmental_Management():
    url = "https://webstore.ansi.org/packages/environmental-management"
    return standard(url)

def Management():
    url = "https://webstore.ansi.org/packages/management"
    return standard(url)

def ISO_Redlines():
    url = "https://webstore.ansi.org/packages/iso-redlines"
    return standard(url)

def X9_Standards_Collections():
    url = "https://webstore.ansi.org/packages/x9"
    return standard(url)

def Tolerances_Measurements():
    url = "https://webstore.ansi.org/packages/tolerances-measurements"
    return standard(url)

def SAE_Collections():
    url = "https://webstore.ansi.org/packages/sae-collections"
    return standard(url)

def Plastics():
    url = "https://webstore.ansi.org/packages/plastics"
    return standard(url)

def Lasers():
    url = "https://webstore.ansi.org/packages/lasers"
    return standard(url)

def Societal_Security():
    url = "https://webstore.ansi.org/packages/societal"
    return standard(url)

def ISO_26000():
    url = "https://webstore.ansi.org/packages/iso-26000"
    return standard(url)

def Other_Packages():
    url = "https://webstore.ansi.org/packages/other"
    return standard(url)
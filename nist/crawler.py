
import requests
from bs4 import BeautifulSoup
import time 
def data_out( tieu_de=False, so_hieu=False,status = False , abstract= False,  date_pub = False , athor= False ,keyword = False ,link_download = False , ten_file = False ):
    data = {
        "tiêu đề"  : tieu_de,
        "trạng thái": status, 
        "số hiệu": so_hieu,
        "tóm tắt": abstract,
        "ngày xuất bản": date_pub,
        "tác giả": athor,
        "từ khóa": keyword,
        "link download": link_download,
        "tên file": ten_file
    }
    
    return data
def get(url):
    resonpse = requests.get(url)
    link_arr_standard = []
    standard = []
    if resonpse.status_code == 200 :
        soup = BeautifulSoup(resonpse.text, 'html.parser')
        table = soup.find(id="publications-results-table")
        links = [a.get('href') for a in table.find_all('a', href=True)]
        
        # Hiển thị các liên kết đã trích xuất
        for link in links:
            link_arr_standard.append("https://csrc.nist.gov/"+ link)
    standard=[]
    for link in link_arr_standard: 
        resonpse = requests.get(link)
        soup = BeautifulSoup(resonpse.text, 'html.parser')
        header_text = soup.find(id ='pub-header-display-container').get_text(strip= True )
        date_pub = soup.find(id ='pub-release-date').get_text(strip = True )
        abstract = soup.find(id='pub-detail-abstract-info').get_text(strip= True )
        keyword = soup.find(id = 'pub-keywords-container').get_text(strip= True)
        statuss = soup.find_all('small')
        status = status[len(statuss)-1].get_text(strip = True)
        links_download = soup.find(id = 'pub-local-download-link').get('href')
        author = soup.find(id = 'pub-authors-container').get_text(strip=True)
        tenfile = links_download.split('/')[-1]
        data_out(tieu_de= header_text , so_hieu= statuss, link_download= links_download , ten_file= tenfile,athor= author, date_pub=date_pub, keyword=keyword, abstract=abstract)
        standard.append(data_out)
    return standard
get("https://csrc.nist.gov/publications/fips")


#
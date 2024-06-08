import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import datetime 
import requests
from bs4 import BeautifulSoup
def format_datetime(input_datetime_str):
    if input_datetime_str == False :
        return False
    input_formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%y-%m-%dT%H:%M:%S",
        "%B, %Y",
    ]
    output_format = "%Y-%m-%d %H:%M:%S"
    for input_format in input_formats:
        try:
            datetime_obj = datetime.datetime.strptime(input_datetime_str, input_format)
            if input_format == "%B, %Y":
                datetime_obj = datetime_obj.replace(day=1, hour=0, minute=0, second=0)
                formatted_datetime_str = datetime_obj.strftime(output_format)
            return datetime_obj
        except ValueError:
            continue
    return input_datetime_str
def data_out(trees = False , Corrigenda_IS= False ,language= False , edition = False , duong_link = False , tac_gia = False , ten_tieng_anh=False, loai = 'kho',so_hieu=False,mo_ta= False , nam_ban_hanh= False , wki_id=False,linh_vuc= False , trang_thai = 'con_hieu_luc',  tu_khoa=False,  action_type=False, link_file=False, name_file=False):
    data = {
        "ten_tieng_anh": ten_tieng_anh.strip() if ten_tieng_anh else False,
        "so_hieu": so_hieu.strip() if so_hieu else False,
        "nam_ban_hanh": format_datetime(nam_ban_hanh),
        "wki_id": wki_id,
        "từ khóa": tu_khoa,
        "trang_thai": trang_thai,
        "action_type": action_type,
        "đường link file": link_file,
        "tên file": name_file,
        'linh_vuc':linh_vuc,
        'mo_ta':mo_ta,
        'loai':loai,
        'duong_link': duong_link, 
        'tac_gia': tac_gia, 
        'edition': edition,
        'language': language,
        'Corrigenda_IS': Corrigenda_IS,
        "tree": trees
    }
    return data 

def download_and_identify_file_itu(url,  download_dir=os.getcwd(), timeout=60):
    """
    Tải tệp từ trang web và xác định tên tệp vừa tải về.

    Parameters:
    url (str): Đường dẫn đến trang web chứa tệp cần tải.
    download_dir (str): Thư mục lưu tệp tải về. Mặc định là thư mục hiện tại.
    timeout (int): Thời gian chờ tối đa để tệp tải về (giây). Mặc định là 60 giây.

    Returns:
    str: Tên tệp vừa tải về hoặc None nếu quá thời gian chờ.
    """
    # Thiết lập tùy chọn Chrome
    options = Options()
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    before_download = set(os.listdir(download_dir))
    driver.get(url)
    bttn = driver.find_element(By.XPATH, '//*[@id="ctl00_content_result_ibtnExcel"]')
    bttn.click()
    time.sleep(5)
    start_time = time.time()
    new_file = None

    while True:
        if time.time() - start_time > timeout:
            print("Quá thời gian chờ tải tệp.")
            break
        after_download = set(os.listdir(download_dir))
        new_files = after_download - before_download
        if new_files:
            new_file = new_files.pop()
            break
        time.sleep(1) 
    driver.quit()

    return new_file
def get_infor_itu(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content , 'html.parser')
    span = soup.find('span', id='ctl00_content_main_uc_rec_main_info1_rpt_main_ctl00_Label6')
    text = span.get_text(separator="\n")
    lines = text.split("\n")

    res = ""
    check = 0
    series = ["A", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "X", "Y", "Z"]

    for line in lines:
        line = line.strip()
        if line:
            parts = line.split(':')
            sub_parts = parts[0].strip().split()
            res += sub_parts[0]
        
            if check != len(lines) - 1:
                res += "[RIPT]"
        check += 1

    new_res = res.split("[RIPT]")
    second_res = []
    temp_res = ""

    for i in range(len(new_res)):
        if new_res[i] in series:
            if temp_res:
                second_res.append(temp_res)
            temp_res = new_res[i]
        else:
            if temp_res:
                temp_res += "[RIPT]" + new_res[i]
            else:
                temp_res = new_res[i]

    if temp_res:
        second_res.append(temp_res)

    return second_res
def fetch_standard_from_file(file_path):
    # Đọc nội dung HTML từ tệp với xử lý lỗi mã hóa
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        html_content = file.read()
    
    # Phân tích cú pháp HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', id='ctl00_content_result_grd_result')
    standards = []

    for row in table.find_all('tr')[1:]:  # Bỏ qua hàng tiêu đề
        cells = row.find_all('td')
        if len(cells) == 3:
            title = cells[1].text.strip()
            status = cells[2].text.strip()
            link = cells[0].find('a')['href'] if cells[0].find('a') else ''
            tree = get_infor_itu(link)
            standard_data = data_out(
                ten_tieng_anh=title,
                trang_thai=status,
                duong_link=link,
                trees=tree
                
            )
            standards.append(standard_data)
        if len(standards)== 1 :
            break
    return standards

def itu(page):
    series =[
        "A","D","E","F","G","H","I","J","K", "L", "M", "N","O", "P", "Q", "R", "S","T", "U","V", "X", "Y", "Z"
    ]
    serie = series[page]
    url =f"https://www.itu.int/itu-t/recommendations/search.aspx?ser={serie}&type=30&status=F&pg_size=20"
    file_path= download_and_identify_file_itu(url)
    standard = fetch_standard_from_file(file_path)
    return standard
print(itu(3))
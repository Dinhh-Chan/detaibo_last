import requests
from bs4 import BeautifulSoup
import datetime 
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
        "so_hieu": so_hieu.strip() if ten_tieng_anh else False,
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
def convert_iso_tree(arr_text):
    arr_res = []
    for elements in arr_text :
        res =""
        texts = elements.split(".")
        tree = ""
        for i in range(len(texts)) :
            
            tree = tree + texts[i]
            res = res + tree +"[RIPT]"
            tree = tree +"."
        arr_res.append(res[0:-6] )
    return arr_res
            
            
                

            
    
def iso(page):
    arr_link = ['https://www.iso.org/ics/01.020.html', 'https://www.iso.org/ics/01.040.html', 'https://www.iso.org/ics/01.060.html', 'https://www.iso.org/ics/01.070.html', 'https://www.iso.org/ics/01.075.html', 'https://www.iso.org/ics/01.080.html', 'https://www.iso.org/ics/01.100.html', 'https://www.iso.org/ics/01.110.html', 'https://www.iso.org/ics/01.120.html', 'https://www.iso.org/ics/01.140.html', 'https://www.iso.org/ics/03.020.html', 'https://www.iso.org/ics/03.060.html', 'https://www.iso.org/ics/03.080.html', 'https://www.iso.org/ics/03.100.html', 'https://www.iso.org/ics/03.120.html', 'https://www.iso.org/ics/03.140.html', 'https://www.iso.org/ics/03.160.html', 'https://www.iso.org/ics/03.180.html', 'https://www.iso.org/ics/03.200.html', 'https://www.iso.org/ics/03.220.html', 'https://www.iso.org/ics/03.240.html', 'https://www.iso.org/ics/07.030.html', 'https://www.iso.org/ics/07.040.html', 'https://www.iso.org/ics/07.060.html', 'https://www.iso.org/ics/07.080.html', 'https://www.iso.org/ics/07.100.html', 'https://www.iso.org/ics/07.120.html', 'https://www.iso.org/ics/07.140.html', 'https://www.iso.org/ics/11.020.html', 'https://www.iso.org/ics/11.040.html', 'https://www.iso.org/ics/11.060.html', 'https://www.iso.org/ics/11.080.html', 'https://www.iso.org/ics/11.100.html', 'https://www.iso.org/ics/11.120.html', 'https://www.iso.org/ics/11.140.html', 'https://www.iso.org/ics/11.160.html', 'https://www.iso.org/ics/11.180.html', 'https://www.iso.org/ics/11.200.html', 'https://www.iso.org/ics/13.020.html', 'https://www.iso.org/ics/13.030.html', 'https://www.iso.org/ics/13.040.html', 'https://www.iso.org/ics/13.060.html', 'https://www.iso.org/ics/13.080.html', 'https://www.iso.org/ics/13.100.html', 'https://www.iso.org/ics/13.110.html', 'https://www.iso.org/ics/13.120.html', 'https://www.iso.org/ics/13.140.html', 'https://www.iso.org/ics/13.160.html', 'https://www.iso.org/ics/13.180.html', 'https://www.iso.org/ics/13.200.html', 'https://www.iso.org/ics/13.220.html', 'https://www.iso.org/ics/13.230.html', 'https://www.iso.org/ics/13.240.html', 'https://www.iso.org/ics/13.280.html', 'https://www.iso.org/ics/13.300.html', 'https://www.iso.org/ics/13.310.html', 'https://www.iso.org/ics/13.320.html', 'https://www.iso.org/ics/13.340.html', 'https://www.iso.org/ics/17.020.html', 'https://www.iso.org/ics/17.040.html', 'https://www.iso.org/ics/17.060.html', 'https://www.iso.org/ics/17.080.html', 'https://www.iso.org/ics/17.120.html', 'https://www.iso.org/ics/17.140.html', 'https://www.iso.org/ics/17.160.html', 'https://www.iso.org/ics/17.180.html', 'https://www.iso.org/ics/17.200.html', 'https://www.iso.org/ics/17.220.html', 'https://www.iso.org/ics/17.240.html', 'https://www.iso.org/ics/19.020.html', 'https://www.iso.org/ics/19.040.html', 'https://www.iso.org/ics/19.060.html', 'https://www.iso.org/ics/19.080.html', 'https://www.iso.org/ics/19.100.html', 'https://www.iso.org/ics/19.120.html', 'https://www.iso.org/ics/21.020.html', 'https://www.iso.org/ics/21.040.html', 'https://www.iso.org/ics/21.060.html', 'https://www.iso.org/ics/21.100.html', 'https://www.iso.org/ics/21.120.html', 'https://www.iso.org/ics/21.140.html', 'https://www.iso.org/ics/21.160.html', 'https://www.iso.org/ics/21.200.html', 'https://www.iso.org/ics/21.220.html', 'https://www.iso.org/ics/21.240.html', 'https://www.iso.org/ics/23.020.html', 'https://www.iso.org/ics/23.040.html', 'https://www.iso.org/ics/23.060.html', 'https://www.iso.org/ics/23.080.html', 'https://www.iso.org/ics/23.100.html', 'https://www.iso.org/ics/23.120.html', 'https://www.iso.org/ics/23.140.html', 'https://www.iso.org/ics/23.160.html', 'https://www.iso.org/ics/25.030.html', 'https://www.iso.org/ics/25.040.html', 'https://www.iso.org/ics/25.060.html', 'https://www.iso.org/ics/25.080.html', 'https://www.iso.org/ics/25.100.html', 'https://www.iso.org/ics/25.120.html', 'https://www.iso.org/ics/25.140.html', 'https://www.iso.org/ics/25.160.html', 'https://www.iso.org/ics/25.180.html', 'https://www.iso.org/ics/25.200.html', 'https://www.iso.org/ics/25.220.html', 'https://www.iso.org/ics/27.010.html', 'https://www.iso.org/ics/27.015.html', 'https://www.iso.org/ics/27.020.html', 'https://www.iso.org/ics/27.040.html', 'https://www.iso.org/ics/27.060.html', 'https://www.iso.org/ics/27.075.html', 'https://www.iso.org/ics/27.080.html', 'https://www.iso.org/ics/27.100.html', 'https://www.iso.org/ics/27.120.html', 'https://www.iso.org/ics/27.140.html', 'https://www.iso.org/ics/27.160.html', 'https://www.iso.org/ics/27.180.html', 'https://www.iso.org/ics/27.190.html', 'https://www.iso.org/ics/27.200.html', 'https://www.iso.org/ics/27.220.html', 'https://www.iso.org/ics/29.020.html', 'https://www.iso.org/ics/29.030.html', 'https://www.iso.org/ics/29.035.html', 'https://www.iso.org/ics/29.040.html', 'https://www.iso.org/ics/29.060.html', 'https://www.iso.org/ics/29.080.html', 'https://www.iso.org/ics/29.100.html', 'https://www.iso.org/ics/29.120.html', 'https://www.iso.org/ics/29.130.html', 'https://www.iso.org/ics/29.140.html', 'https://www.iso.org/ics/29.160.html', 'https://www.iso.org/ics/29.180.html', 'https://www.iso.org/ics/29.220.html', 'https://www.iso.org/ics/29.240.html', 'https://www.iso.org/ics/29.260.html', 'https://www.iso.org/ics/29.280.html', 'https://www.iso.org/ics/31.020.html', 'https://www.iso.org/ics/31.040.html', 'https://www.iso.org/ics/31.060.html', 'https://www.iso.org/ics/31.080.html', 'https://www.iso.org/ics/31.120.html', 'https://www.iso.org/ics/31.180.html', 'https://www.iso.org/ics/31.200.html', 'https://www.iso.org/ics/31.220.html', 'https://www.iso.org/ics/31.260.html', 'https://www.iso.org/ics/33.020.html', 'https://www.iso.org/ics/33.040.html', 'https://www.iso.org/ics/33.050.html', 'https://www.iso.org/ics/33.060.html', 'https://www.iso.org/ics/33.070.html', 'https://www.iso.org/ics/33.100.html', 'https://www.iso.org/ics/33.120.html', 'https://www.iso.org/ics/33.160.html', 'https://www.iso.org/ics/33.180.html', 'https://www.iso.org/ics/35.020.html', 'https://www.iso.org/ics/35.030.html', 'https://www.iso.org/ics/35.040.html', 'https://www.iso.org/ics/35.060.html', 'https://www.iso.org/ics/35.080.html', 'https://www.iso.org/ics/35.100.html', 'https://www.iso.org/ics/35.110.html', 'https://www.iso.org/ics/35.140.html', 'https://www.iso.org/ics/35.160.html', 'https://www.iso.org/ics/35.180.html', 'https://www.iso.org/ics/35.200.html', 'https://www.iso.org/ics/35.210.html', 'https://www.iso.org/ics/35.220.html', 'https://www.iso.org/ics/35.240.html', 'https://www.iso.org/ics/35.260.html', 'https://www.iso.org/ics/37.020.html', 'https://www.iso.org/ics/37.040.html', 'https://www.iso.org/ics/37.060.html', 'https://www.iso.org/ics/37.080.html', 'https://www.iso.org/ics/37.100.html', 'https://www.iso.org/ics/39.040.html', 'https://www.iso.org/ics/39.060.html', 'https://www.iso.org/ics/43.020.html', 'https://www.iso.org/ics/43.040.html', 'https://www.iso.org/ics/43.060.html', 'https://www.iso.org/ics/43.080.html', 'https://www.iso.org/ics/43.100.html', 'https://www.iso.org/ics/43.120.html', 'https://www.iso.org/ics/43.140.html', 'https://www.iso.org/ics/43.150.html', 'https://www.iso.org/ics/43.160.html', 'https://www.iso.org/ics/43.180.html', 'https://www.iso.org/ics/45.020.html', 'https://www.iso.org/ics/45.060.html', 'https://www.iso.org/ics/45.080.html', 'https://www.iso.org/ics/45.120.html', 'https://www.iso.org/ics/47.020.html', 'https://www.iso.org/ics/47.040.html', 'https://www.iso.org/ics/47.060.html', 'https://www.iso.org/ics/47.080.html', 'https://www.iso.org/ics/49.020.html', 'https://www.iso.org/ics/49.025.html', 'https://www.iso.org/ics/49.030.html', 'https://www.iso.org/ics/49.035.html', 'https://www.iso.org/ics/49.040.html', 'https://www.iso.org/ics/49.045.html', 'https://www.iso.org/ics/49.050.html', 'https://www.iso.org/ics/49.060.html', 'https://www.iso.org/ics/49.080.html', 'https://www.iso.org/ics/49.090.html', 'https://www.iso.org/ics/49.095.html', 'https://www.iso.org/ics/49.100.html', 'https://www.iso.org/ics/49.120.html', 'https://www.iso.org/ics/49.140.html', 'https://www.iso.org/ics/53.020.html', 'https://www.iso.org/ics/53.040.html', 'https://www.iso.org/ics/53.060.html', 'https://www.iso.org/ics/53.080.html', 'https://www.iso.org/ics/53.100.html', 'https://www.iso.org/ics/55.020.html', 'https://www.iso.org/ics/55.040.html', 'https://www.iso.org/ics/55.080.html', 'https://www.iso.org/ics/55.100.html', 'https://www.iso.org/ics/55.120.html', 'https://www.iso.org/ics/55.130.html', 'https://www.iso.org/ics/55.140.html', 'https://www.iso.org/ics/55.180.html', 'https://www.iso.org/ics/59.020.html', 'https://www.iso.org/ics/59.060.html', 'https://www.iso.org/ics/59.080.html', 'https://www.iso.org/ics/59.100.html', 'https://www.iso.org/ics/59.120.html', 'https://www.iso.org/ics/59.140.html', 'https://www.iso.org/ics/61.020.html', 'https://www.iso.org/ics/61.040.html', 'https://www.iso.org/ics/61.060.html', 'https://www.iso.org/ics/61.080.html', 'https://www.iso.org/ics/65.020.html', 'https://www.iso.org/ics/65.040.html', 'https://www.iso.org/ics/65.060.html', 'https://www.iso.org/ics/65.080.html', 'https://www.iso.org/ics/65.100.html', 'https://www.iso.org/ics/65.120.html', 'https://www.iso.org/ics/65.140.html', 'https://www.iso.org/ics/65.145.html', 'https://www.iso.org/ics/65.150.html', 'https://www.iso.org/ics/65.160.html', 'https://www.iso.org/ics/67.020.html', 'https://www.iso.org/ics/67.040.html', 'https://www.iso.org/ics/67.050.html', 'https://www.iso.org/ics/67.060.html', 'https://www.iso.org/ics/67.080.html', 'https://www.iso.org/ics/67.100.html', 'https://www.iso.org/ics/67.120.html', 'https://www.iso.org/ics/67.140.html', 'https://www.iso.org/ics/67.160.html', 'https://www.iso.org/ics/67.180.html', 'https://www.iso.org/ics/67.190.html', 'https://www.iso.org/ics/67.200.html', 'https://www.iso.org/ics/67.220.html', 'https://www.iso.org/ics/67.240.html', 'https://www.iso.org/ics/67.250.html', 'https://www.iso.org/ics/67.260.html', 'https://www.iso.org/ics/71.020.html', 'https://www.iso.org/ics/71.040.html', 'https://www.iso.org/ics/71.060.html', 'https://www.iso.org/ics/71.080.html', 'https://www.iso.org/ics/71.100.html', 'https://www.iso.org/ics/71.120.html', 'https://www.iso.org/ics/73.020.html', 'https://www.iso.org/ics/73.040.html', 'https://www.iso.org/ics/73.060.html', 'https://www.iso.org/ics/73.080.html', 'https://www.iso.org/ics/73.100.html', 'https://www.iso.org/ics/73.120.html', 'https://www.iso.org/ics/75.020.html', 'https://www.iso.org/ics/75.040.html', 'https://www.iso.org/ics/75.060.html', 'https://www.iso.org/ics/75.080.html', 'https://www.iso.org/ics/75.100.html', 'https://www.iso.org/ics/75.120.html', 'https://www.iso.org/ics/75.140.html', 'https://www.iso.org/ics/75.160.html', 'https://www.iso.org/ics/75.180.html', 'https://www.iso.org/ics/75.200.html', 'https://www.iso.org/ics/77.020.html', 'https://www.iso.org/ics/77.040.html', 'https://www.iso.org/ics/77.060.html', 'https://www.iso.org/ics/77.080.html', 'https://www.iso.org/ics/77.100.html', 'https://www.iso.org/ics/77.120.html', 'https://www.iso.org/ics/77.140.html', 'https://www.iso.org/ics/77.150.html', 'https://www.iso.org/ics/77.160.html', 'https://www.iso.org/ics/77.180.html', 'https://www.iso.org/ics/79.020.html', 'https://www.iso.org/ics/79.040.html', 'https://www.iso.org/ics/79.060.html', 'https://www.iso.org/ics/79.080.html', 'https://www.iso.org/ics/79.100.html', 'https://www.iso.org/ics/79.120.html', 'https://www.iso.org/ics/81.040.html', 'https://www.iso.org/ics/81.060.html', 'https://www.iso.org/ics/81.080.html', 'https://www.iso.org/ics/83.020.html', 'https://www.iso.org/ics/83.040.html', 'https://www.iso.org/ics/83.060.html', 'https://www.iso.org/ics/83.080.html', 'https://www.iso.org/ics/83.100.html', 'https://www.iso.org/ics/83.120.html', 'https://www.iso.org/ics/83.140.html', 'https://www.iso.org/ics/83.160.html', 'https://www.iso.org/ics/83.180.html', 'https://www.iso.org/ics/83.200.html', 'https://www.iso.org/ics/85.020.html', 'https://www.iso.org/ics/85.040.html', 'https://www.iso.org/ics/85.060.html', 'https://www.iso.org/ics/85.080.html', 'https://www.iso.org/ics/85.100.html', 'https://www.iso.org/ics/87.020.html', 'https://www.iso.org/ics/87.040.html', 'https://www.iso.org/ics/87.060.html', 'https://www.iso.org/ics/87.080.html', 'https://www.iso.org/ics/87.100.html', 'https://www.iso.org/ics/91.010.html', 'https://www.iso.org/ics/91.040.html', 'https://www.iso.org/ics/91.060.html', 'https://www.iso.org/ics/91.080.html', 'https://www.iso.org/ics/91.090.html', 'https://www.iso.org/ics/91.100.html', 'https://www.iso.org/ics/91.120.html', 'https://www.iso.org/ics/91.140.html', 'https://www.iso.org/ics/91.160.html', 'https://www.iso.org/ics/91.200.html', 'https://www.iso.org/ics/91.220.html', 'https://www.iso.org/ics/93.010.html', 'https://www.iso.org/ics/93.020.html', 'https://www.iso.org/ics/93.025.html', 'https://www.iso.org/ics/93.030.html', 'https://www.iso.org/ics/93.040.html', 'https://www.iso.org/ics/93.060.html', 'https://www.iso.org/ics/93.080.html', 'https://www.iso.org/ics/93.100.html', 'https://www.iso.org/ics/95.020.html', 'https://www.iso.org/ics/97.020.html', 'https://www.iso.org/ics/97.040.html', 'https://www.iso.org/ics/97.060.html', 'https://www.iso.org/ics/97.100.html', 'https://www.iso.org/ics/97.120.html', 'https://www.iso.org/ics/97.130.html', 'https://www.iso.org/ics/97.140.html', 'https://www.iso.org/ics/97.145.html', 'https://www.iso.org/ics/97.150.html', 'https://www.iso.org/ics/97.160.html', 'https://www.iso.org/ics/97.170.html', 'https://www.iso.org/ics/97.180.html', 'https://www.iso.org/ics/97.190.html', 'https://www.iso.org/ics/97.195.html', 'https://www.iso.org/ics/97.200.html', 'https://www.iso.org/ics/97.220.html']
    url = arr_link[page]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    second_arr_link =[]
    td_elements = soup.find_all('td', {'data-title': 'ICS'})
    for td in td_elements:
        if td.find('a') :
            second_arr_link.append('https://www.iso.org'+ td.find('a').get('href'))
    standard =[]
    link_standard =[]
    if len(second_arr_link)== 0 :
        div_link = soup.find_all('div', class_= "fw-semibold")
        for div in div_link :
            link_standard.append('https://www.iso.org'+ div.find('a').get('href'))
        for link in link_standard :
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')

            description = soup.find('div', itemprop='description')
            if description:
                description_text = description.get_text(strip=True)
            else:
                description_text = 'N/A'

            number = soup.find('span', class_='d-flex justify-content-between align-items-start')
            if number:
                inspan = number.find('span', class_='d-block mb-3')
                if inspan:
                    number_text = inspan.get_text(strip=True)
                else:
                    number_text = 'N/A'
            else:
                number_text = 'N/A'
            title_span = soup.find('span', class_ = "lead d-block mb-3")
            if title_span :
                title = title_span.get_text(strip=True )
            else :
                title = "N/A"
            link_sample = soup.find('a', class_='btn btn-sm btn-light')
            if link_sample:
                link_sample = link_sample.get('href')
            else:
                link_sample = 'N/A'
            span_tag= soup.find_all('span', class_= 'entry-name entry-block')
            arr_tree= []
            for span in range(1,len(span_tag)):
                arr_tree.append(span_tag[span].get_text(strip = True ))
            tree =convert_iso_tree(arr_tree)
            data = data_out(ten_tieng_anh=title, so_hieu=number_text, trees=tree, link_file= link_sample, duong_link=link, mo_ta=description_text)
            standard.append(data)
            return standard
    else :
        for secon_link in second_arr_link :
            response = requests.get(secon_link)
            soup = BeautifulSoup(response.content, 'html.parser')
            div_link = soup.find_all('div', class_= "fw-semibold")
            for div in div_link :
                link_standard.append('https://www.iso.org/'+div.find('a').get('href'))
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')

            description = soup.find('div', itemprop='description')
            if description:
                description_text = description.get_text(strip=True)
            else:
                description_text = 'N/A'

            number = soup.find('span', class_='d-flex justify-content-between align-items-start')
            if number:
                inspan = number.find('span', class_='d-block mb-3')
                if inspan:
                    number_text = inspan.get_text(strip=True)
                else:
                    number_text = 'N/A'
            else:
                number_text = 'N/A'
            title_span = soup.find('span', class_ = "lead d-block mb-3")
            if title_span :
                title = title_span.get_text(strip=True )
            else :
                title = "N/A"
            link_sample = soup.find('a', class_='btn btn-sm btn-light')
            if link_sample:
                link_sample = link_sample.get('href')
            else:
                link_sample = 'N/A'
            span_tag= soup.find_all('span', class_= 'entry-name entry-block')
            arr_tree= []
            for span in range(1,len(span_tag)):
                arr_tree.append(span_tag[span].get_text(strip = True ))
            tree =convert_iso_tree(arr_tree)
            data = data_out(ten_tieng_anh=title, so_hieu=number_text, trees=tree, link_file= link_sample, duong_link=link, mo_ta=description_text)
            standard.append(data)
            return standard
        
            

        
        

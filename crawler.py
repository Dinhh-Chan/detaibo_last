import json
import csv 
import requests
import logging
import datetime
from bs4 import BeautifulSoup 
import time 
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
_logger = logging.getLogger(__name__)

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

def data_out(duong_link = False , tac_gia = False , ten_tieng_anh=False, loai = 'kho',so_hieu=False,mo_ta= False , nam_ban_hanh= False , wki_id=False,linh_vuc= False , trang_thai = 'con_hieu_luc',  tu_khoa=False,  action_type=False, link_file=False, name_file=False):
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
        'tac_gia': tac_gia
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
        
            

        
        
#itu
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
#iec
def download_file_iec(url, output):
    try :
        response = requests.get(url)
        if response.status_code == 200:
            with open(output, 'wb') as file :
                file.write(response.content)
        else :
            print('error')
    except Exception as e : 
        print(e)
def fetch_excel_file_iec(path, tree):
    try:
        # Đọc tệp XML và phân tích cú pháp thành DataFrame của pandas
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Sử dụng BeautifulSoup để phân tích cú pháp nội dung XML
        soup = BeautifulSoup(content, 'xml')
        # print(soup)
        
        # Tìm tất cả các hàng dữ liệu
        rows = soup.find_all('Row')[2:]  # Bỏ qua hàng tiêu đề và hàng mô tả
        # print(rows)
        data = []
        for row in rows:
            cells = row.find_all('Cell')
            # print(cells)
            row_data = [cell.find('Data').get_text() if cell.find('Data') else False  for cell in cells]
            # print(row_data)
            data.append(row_data)

        # # Chuyển đổi dữ liệu thành DataFrame
        columns = ['Reference', 'Edition', 'Corrigenda/IS', 'Date', 'Title', 'Language', 'Description']
        df = pd.DataFrame(data, columns=columns)
        # print(df)
        # # Đổi tên các cột cho khớp với cấu trúc dữ liệu mong muốn
        columns_mapping = {
            "Reference": "so_hieu",
            "Edition": "edition",
            "Corrigenda/IS": "Corrigenda_IS",
            "Title": "ten_tieng_anh",
            "Language": "language",
            "Description": "mo_ta",
            "Date": "nam_ban_hanh"
        }
        df.rename(columns=columns_mapping, inplace=True)
        # print(df)
        standard = []

        # # Duyệt qua các hàng trong DataFrame và tạo đối tượng data_out
        for _, row in df.iterrows():
            print(row["so_hieu"] )
            datas = data_out(
                Corrigenda_IS=row["Corrigenda_IS"] if pd.notna(row["Corrigenda_IS"]) else False,
                language=row["language"] if pd.notna(row["language"]) else False,
                edition=row["edition"] if pd.notna(row["edition"]) else False,
                mo_ta=row["mo_ta"] if pd.notna(row["mo_ta"]) else False,
                ten_tieng_anh=row["ten_tieng_anh"] if pd.notna(row["ten_tieng_anh"]) else False,
                so_hieu=row["so_hieu"] if pd.notna(row["so_hieu"]) else False,
                nam_ban_hanh=row["nam_ban_hanh"] if pd.notna(row["nam_ban_hanh"]) else False,
                trees=tree
            )
            print(datas)
            standard.append(datas)
        # print(standard )
        # return standard

    except FileNotFoundError:
        print("Lỗi: Không tìm thấy tệp.")
    except ValueError as ve:
        print(f"Lỗi: {ve}")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

        print(f"Đã xảy ra lỗi: {e}")

def iec(page):
    all_link =[
    {
        "TC_1": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1231"
    },
    {
        "TC_2": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1221"
    },
    {
        "TC_3": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1222"
    },
    {
        "SC_3C": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1319"
    },
    {
        "SC_3D": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1345"
    },
    {
        "TC_4": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1228"
    },
    {
        "TC_5": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1226"
    },
    {
        "TC_7": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1230"
    },
    {
        "TC_8": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1240"
    },
    {
        "SC_8A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:10072"
    },
    {
        "SC_8B": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:20639"
    },
    {
        "SC_8C": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:25987"
    },
    {
        "TC_9": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1248"
    },
    {
        "TC_10": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1246"
    },
    {
        "TC_11": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1300"
    },
    {
        "TC_13": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1258"
    },
    {
        "TC_14": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1224"
    },
    {
        "TC_15": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1227"
    },
    {
        "TC_17": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1229"
    },
    {
        "SC_17A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1402"
    },
    {
        "SC_17C": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1405"
    },
    {
        "TC_18": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1284"
    },
    {
        "SC_18A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1407"
    },
    {
        "TC_20": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1214"
    },
    {
        "TC_21": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1290"
    },
    {
        "SC_21A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1410"
    },
    {
        "TC_22": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1293"
    },
    {
        "SC_22E": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1414"
    },
    {
        "SC_22F": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1415"
    },
    {
        "SC_22G": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1416"
    },
    {
        "SC_22H": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1441"
    },
    {
        "TC_23": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1299"
    },
    {
        "SC_23A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1417"
    },
    {
        "SC_23B": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1418"
    },
    {
        "SC_23E": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1421"
    },
    {
        "SC_23G": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1425"
    },
    {
        "SC_23H": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1426"
    },
    {
        "SC_23J": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1428"
    },
    {
        "SC_23K": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:10046"
    },
    {
        "TC_25": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1215"
    },
    {
        "TC_26": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1216"
    },
    {
        "TC_27": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1217"
    },
    {
        "TC_29": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1301"
    },
    {
        "TC_31": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1232"
    },
    {
        "SC_31G": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1331"
    },
    {
        "SC_31J": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1333"
    },
    {
        "SC_31M": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1453"
    },
    {
        "TC_32": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1234"
    },
    {
        "SC_32A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1337"
    },
    {
        "SC_32B": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1338"
    },
    {
        "SC_32C": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1339"
    },
    {
        "TC_33": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1220"
    },
    {
        "TC_34": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1235"
    },
    {
        "SC_34A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1340"
    },
    {
        "SC_34B": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1342"
    },
    {
        "SC_34C": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1343"
    },
    {
        "SC_34D": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1344"
    },
    {
        "TC_35": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1237"
    },
    {
        "TC_36": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1238"
    },
    {
        "SC_36A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1347"
    },
    {
        "TC_37": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1239"
    },
    {
        "SC_37A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1352"
    },
    {
        "SC_37B": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1353"
    },
    {
        "TC_38": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1241"
    },
    {
        "TC_40": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1219"
    },
    {
        "TC_42": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1243"
    },
    {
        "TC_44": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1302"
    },
    {
        "TC_45": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1244"
    },
    {
        "SC_45A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1358"
    },
    {
        "SC_45B": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1360"
    },
    {
        "TC_46": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1247"
    },
    {
        "SC_46A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1363"
    },
    {
        "SC_46C": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1366"
    },
    {
        "SC_46F": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1447"
    },
    {
        "TC_47": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1251"
    },
    {
        "SC_47A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1368"
    },
    {
        "SC_47D": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1372"
    },
    {
        "SC_47E": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1371"
    },
    {
        "SC_47F": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1449"
    },
    {
        "TC_48": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1252"
    },
    {
        "SC_48B": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1373"
    },
    {
        "SC_48D": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1374"
    },
    {
        "TC_49": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1257"
    },
    {
        "TC_51": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1266"
    },
    {
        "TC_55": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1272"
    },
    {
        "TC_56": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1270"
    },
    {
        "TC_57": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1273"
    },
    {
        "TC_59": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1275"
    },
    {
        "SC_59A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1389"
    },
    {
        "SC_59C": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1391"
    },
    {
        "SC_59D": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1392"
    },
    {
        "SC_59F": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1395"
    },
    {
        "SC_59K": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1440"
    },
    {
        "SC_59L": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1448"
    },
    {
        "SC_59M": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:4248"
    },
    {
        "SC_59N": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:27689"
    },
    {
        "TC_61": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1236"
    },
    {
        "SC_61B": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1346"
    },
    {
        "SC_61C": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1349"
    },
    {
        "SC_61D": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1351"
    },
    {
        "SC_61H": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1356"
    },
    {
        "SC_61J": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1357"
    },
    {
        "TC_62": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1245"
    },
    {
        "SC_62A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1359"
    },
    {
        "SC_62B": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1361"
    },
    {
        "SC_62C": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1362"
    },
    {
        "SC_62D": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1365"
    },
    {
        "TC_64": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1249"
    },
    {
        "TC_65": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1250"
    },
    {
        "SC_65A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1369"
    },
    {
        "SC_65B": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1375"
    },
    {
        "SC_65C": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1376"
    },
    {
        "SC_65E": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1452"
    },
    {
        "TC_66": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1253"
    },
    {
        "TC_68": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1254"
    },
    {
        "TC_69": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1255"
    },
    {
        "TC_70": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1256"
    },
    {
        "TC_72": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1259"
    },
    {
        "TC_73": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1261"
    },
    {
        "TC_76": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1264"
    },
    {
        "TC_77": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1265"
    },
    {
        "SC_77A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1384"
    },
    {
        "SC_77B": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1385"
    },
    {
        "SC_77C": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1387"
    },
    {
        "TC_78": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1267"
    },
    {
        "TC_79": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1269"
    },
    {
        "TC_80": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1271"
    },
    {
        "TC_81": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1274"
    },
    {
        "TC_82": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1276"
    },
    {
        "TC_85": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1278"
    },
    {
        "TC_86": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1279"
    },
    {
        "SC_86A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1398"
    },
    {
        "SC_86B": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1401"
    },
    {
        "SC_86C": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1403"
    },
    {
        "TC_87": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1281"
    },
    {
        "TC_88": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1282"
    },
    {
        "TC_89": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1283"
    },
    {
        "TC_90": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1285"
    },
    {
        "TC_91": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1286"
    },
    {
        "TC_94": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1289"
    },
    {
        "TC_95": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1291"
    },
    {
        "TC_96": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1292"
    },
    {
        "TC_97": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1294"
    },
    {
        "TC_99": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1296"
    },
    {
        "TC_100": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1297"
    },
    {
        "TA_1": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:1429"
    },
    {
        "TA_2": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:1432"
    },
    {
        "TA_4": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:1431"
    },
    {
        "TA_5": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:1433"
    },
    {
        "TA_6": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:1442"
    },
    {
        "TA_15": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:10039"
    },
    {
        "TA_16": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:11009"
    },
    {
        "TA_17": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:20051"
    },
    {
        "TA_18": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:22351"
    },
    {
        "TA_19": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:22359"
    },
    {
        "TA_20": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:22357"
    },
    {
        "TC_101": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1305"
    },
    {
        "TC_103": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1307"
    },
    {
        "TC_104": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1308"
    },
    {
        "TC_105": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1309"
    },
    {
        "TC_106": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1303"
    },
    {
        "TC_107": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1304"
    },
    {
        "TC_108": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1311"
    },
    {
        "TC_109": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1312"
    },
    {
        "TC_110": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1313"
    },
    {
        "TC_111": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1314"
    },
    {
        "TC_112": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1310"
    },
    {
        "TC_113": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1315"
    },
    {
        "TC_114": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1316"
    },
    {
        "TC_115": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:3988"
    },
    {
        "TC_116": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:4112"
    },
    {
        "TC_117": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:7851"
    },
    {
        "PC_118": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:8701"
    },
    {
        "TC_119": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:8679"
    },
    {
        "TC_120": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:9463"
    },
    {
        "TC_121": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:10607"
    },
    {
        "SC_121A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:10618"
    },
    {
        "SC_121B": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:10619"
    },
    {
        "TC_122": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:10557"
    },
    {
        "TC_124": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:20537"
    },
    {
        "TC_125": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:23165"
    },
    {
        "PC_126": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:23203"
    },
    {
        "CIS/A": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1327"
    },
    {
        "CIS/B": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1412"
    },
    {
        "CIS/D": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1419"
    },
    {
        "CIS/F": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1424"
    },
    {
        "CIS/H": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1439"
    },
    {
        "CIS/I": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1444"
    },
    {
        "SyC_AAL": "https://www.iec.ch/dyn/www/f?p=103:186:0::::FSP_ORG_ID:11827"
    },
    {
        "SyC_LVDC": "https://www.iec.ch/dyn/www/f?p=103:186:0::::FSP_ORG_ID:20447"
    },
    {
        "SyC_SM": "https://www.iec.ch/dyn/www/f?p=103:186:0::::FSP_ORG_ID:22328"
    },
    {
        "SyC_Smart_Cities": "https://www.iec.ch/dyn/www/f?p=103:186:0::::FSP_ORG_ID:13073"
    },
    {
        "SyC_Smart_Energy": "https://www.iec.ch/dyn/www/f?p=103:186:0::::FSP_ORG_ID:11825"
    },
    {
        "ISO/IEC_JTC_1": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:3387"
    },
    {
        "ISO/IEC_JTC_1/SC_2": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:3394"
    },
    {
        "ISO/IEC_JTC_1/SC_6": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:3411"
    },
    {
        "ISO/IEC_JTC_1/SC_7": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:3412"
    },
    {
        "ISO/IEC_JTC_1/SC_17": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:3392"
    },
    {
        "ISO/IEC_JTC_1/SC_22": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:3396"
    },
    {
        "ISO/IEC_JTC_1/SC_23": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:3397"
    },
    {
        "ISO/IEC_JTC_1/SC_24": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:3398"
    },
    {
        "ISO/IEC_JTC_1/SC_25": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:3399"
    },
    {
        "ISO/IEC_JTC_1/SC_27": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:3401"
    },
    {
        "ISO/IEC_JTC_1/SC_28": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:3402"
    },
    {
        "ISO/IEC_JTC_1/SC_29": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:3403"
    },
    {
        "ISO/IEC_JTC_1/SC_31": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:3405"
    },
    {
        "ISO/IEC_JTC_1/SC_32": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:3406"
    },
    {
        "ISO/IEC_JTC_1/SC_34": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:3408"
    },
    {
        "ISO/IEC_JTC_1/SC_35": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:3409"
    },
    {
        "ISO/IEC_JTC_1/SC_36": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:3410"
    },
    {
        "ISO/IEC_JTC_1/SC_37": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:5510"
    },
    {
        "ISO/IEC_JTC_1/SC_38": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:7608"
    },
    {
        "ISO/IEC_JTC_1/SC_39": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:8987"
    },
    {
        "ISO/IEC_JTC_1/SC_40": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:10582"
    },
    {
        "ISO/IEC_JTC_1/SC_41": "https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:20486"
    },
    {
        "ISO/IEC_JTC_1/SC_42": "https://www.iec.ch/dyn/www/f?p=103:7:0::::FSP_ORG_ID:21538"
    }
]   
    url_and_path = all_link[page]
    url = next(iter(url_and_path.values()))
    path = next(iter(url_and_path.keys()))
    response= requests.get(url)
    soup = BeautifulSoup(response.content , 'html.parser')
    div_tag = soup.find('div', class_='dash-thread')

# Nếu tìm thấy thẻ <div>, tìm thẻ <a> bên trong thẻ <div>
    if div_tag:
        a_tag = div_tag.find('a', href=True)
        if a_tag:
            # Lấy giá trị của thuộc tính href
            href_value = a_tag['href']
            # Trích xuất chuỗi cần thiết từ href_value
            start = href_value.find('f?p=')
            if start != -1:
                end = href_value.find("'", start)
                if end != -1:
                    extracted_value = href_value[start:end]
                else:
                    extracted_value = href_value[start:]
            else:
                extracted_value = None
        else:
            extracted_value = None
    else:
        extracted_value = None

    if extracted_value:
        download_url = "https://www.iec.ch/dyn/www/" + extracted_value
        print(path +".xlsx")
        download_file_iec(download_url, path + ".xlsx")
        standard = fetch_excel_file_iec(path + ".xlsx", "IEC[RIPT]" + path)
        return standard
    else:
        print("Lỗi: Không tìm thấy giá trị hợp lệ trong thẻ href.")
        return None
#ANSI
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
        standard.append(data_out(so_hieu= so_hieu, ten_tieng_anh=ten_tieng_anh,mo_ta=abstract, duong_link=duong_link, tac_gia= author))
    return standard
def Construction_Construction_Safety(page):
    url = "https://webstore.ansi.org/packages/construction"
    return standard(url)
def Occupational_Health_Safety (page):
    url = "https://webstore.ansi.org/packages/occupational"
    return standard(url)
def Machine_Safety(page):
    url = "https://webstore.ansi.org/packages/machine-safety"
    return standard(url)

def Risk_Management(page):
    url = "https://webstore.ansi.org/packages/risk-management"
    return standard(url)

def Laboratories(page):
    url = "https://webstore.ansi.org/packages/laboratories"
    return standard(url)

def Cloud_Security(page):
    url = "https://webstore.ansi.org/packages/cloud"
    return standard(url)

def Energy_Management(page):
    url = "https://webstore.ansi.org/packages/energy-management"
    return standard(url)

def Industrial_Robotics(page):
    url = "https://webstore.ansi.org/packages/industrial-robotics"
    return standard(url)

def IEC_Series(page):
    url = "https://webstore.ansi.org/packages/iec-series"
    return standard(url)

def IEC_Redlines(page):
    url = "https://webstore.ansi.org/packages/iec-redline"
    return standard(url)

def Identity_Theft(page):
    url = "https://webstore.ansi.org/packages/identity-theft"
    return standard(url)

def NSF_Standards_Collections(page):
    url = "https://webstore.ansi.org/packages/nsf-food"
    return standard(url)

def Radio_Frequency_Disturbance(page):
    url = "https://webstore.ansi.org/packages/radio"
    return standard(url)

def Electronic_Communications(page):
    url = "https://webstore.ansi.org/packages/electronic-communications"
    return standard(url)

def ISO_Handbooks(page):
    url = "https://webstore.ansi.org/packages/iso-handbook"
    return standard(url)

def Certification(page):
    url = "https://webstore.ansi.org/packages/certification"
    return standard(url)

def Medical_Devices(page):
    url = "https://webstore.ansi.org/packages/medical"
    return standard(url)

def IT_IT_Security(page):
    url = "https://webstore.ansi.org/packages/it-security"
    return standard(url)

def Quality_Management(page):
    url = "https://webstore.ansi.org/packages/quality-management"
    return standard(url)

def Regenerative_Medicine(page):
    url = "https://webstore.ansi.org/packages/regenerative-medicine"
    return standard(url)

def Road_Vehicles(page):
    url = "https://webstore.ansi.org/packages/road-vehicles"
    return standard(url)

def Environmental_Management(page):
    url = "https://webstore.ansi.org/packages/environmental-management"
    return standard(url)

def Management(page):
    url = "https://webstore.ansi.org/packages/management"
    return standard(url)

def ISO_Redlines(page):
    url = "https://webstore.ansi.org/packages/iso-redlines"
    return standard(url)

def X9_Standards_Collections(page):
    url = "https://webstore.ansi.org/packages/x9"
    return standard(url)

def Tolerances_Measurements(page):
    url = "https://webstore.ansi.org/packages/tolerances-measurements"
    return standard(url)

def SAE_Collections(page):
    url = "https://webstore.ansi.org/packages/sae-collections"
    return standard(url)

def Plastics(page):
    url = "https://webstore.ansi.org/packages/plastics"
    return standard(url)

def Lasers(page):
    url = "https://webstore.ansi.org/packages/lasers"
    return standard(url)

def Societal_Security(page):
    url = "https://webstore.ansi.org/packages/societal"
    return standard(url)

def ISO_26000(page):
    url = "https://webstore.ansi.org/packages/iso-26000"
    return standard(url)

def Other_Packages(page):
    url = "https://webstore.ansi.org/packages/other"
    return standard(url)

#EN
def get_all_level_1(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return [element.get('href') for element in soup.find_all('a', class_='kat level1 selected open0')]
    except requests.RequestException as e:
        print(f"Error fetching level 1 links: {e}")
        return []

def check_level_and_get_standard(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        level_2 = [element.get('href') for element in soup.find_all('a', class_='kat level2 selected open0')]

        standards = []
        if level_2:
            for level in level_2:
                standards += process_level(level)
        else:
            standards += fetch_standard_data(url)
        
        return standards
    except requests.RequestException as e:
        print(f"Error checking level: {e}")
        return []

def process_level(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        level_3 = [element.get('href') for element in soup.find_all('a', class_='kat level3 selected open0')]

        standards = []
        if level_3:
            for lev in level_3:
                standards += fetch_standard_data(lev)
        else:
            standards += fetch_standard_data(url)
        
        return standards
    except requests.RequestException as e:
        print(f"Error processing level: {e}")
        return []

def get_page_count(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        pages_span = soup.find('span', class_='pages')
        links = pages_span.find_all('a') if pages_span else []
        return len(links) - 1  # Adjust as needed
    except requests.RequestException as e:
        print(f"Error getting page count: {e}")
        return 0

def fetch_standard(page, url):
    if page <= 0:
        return fetch_standard_data(url)
    else:
        url = url[:-1]
        new_url = f"{url}-page-{page}/"
        return fetch_standard_data(new_url)

def fetch_standard_data(url):
    standards = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        all_links = [link['href'] for link in soup.select('a.katalogProduct__name')]

        for link in all_links:
            try:
                response = requests.get(link)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                title = soup.select_one('div.fleft.detail_right_side').get_text(strip=True)
                description = soup.find_all('div', class_='textFormat')
                descriptions = description[2].get_text(strip=True) if len(description) > 2 else 'n/a'
                date_pub = soup.select_one('.released').get_text(strip=True)
                
                standards.append(data_out(ten_tieng_anh=title, mo_ta=descriptions))
                time.sleep(3)
            except requests.RequestException as e:
                print(f"Error fetching standard data for link {link}: {e}")
    except requests.RequestException as e:
        print(f"Error fetching standard data: {e}")
    
    return standards

def aiag_standard(page):
    url = "https://www.en-standard.eu/qs-9000/?mena=1"
    return fetch_standard_data(url)

def atsm(page):
    pages = get_all_level_1('https://www.en-standard.eu/astm-standards/')
    return check_level_and_get_standard(pages[page] if page < len(pages) else "")

def csn(page):
    pages = get_all_level_1('https://www.en-standard.eu/csn-standards/')
    return check_level_and_get_standard(pages[page] if page < len(pages) else "")

def bs(page):
    pages = get_all_level_1('https://www.en-standard.eu/bs-standards/')
    return check_level_and_get_standard(pages[page] if page < len(pages) else "")

def eurocode(page):
    pages = get_all_level_1('https://www.en-standard.eu/eurocodes/')
    return check_level_and_get_standard(pages[page] if page < len(pages) else "")

def CQI(page):
    url = 'https://www.en-standard.eu/cqi/'
    return fetch_standard(page, url)

def DIN(page):
    url = 'https://www.en-standard.eu/din-standards/'
    return fetch_standard(page, url)

def IEC(page):
    url = 'https://www.en-standard.eu/iec-standards/'
    return fetch_standard(page, url)

def ISO(page):
    url = 'https://www.en-standard.eu/iso-standards/'
    return fetch_standard(page, url)

def UNE(page):
    url = 'https://www.en-standard.eu/une-standards/'
    return fetch_standard(page, url)

def VDA(page):
    url = 'https://www.en-standard.eu/automotive-quality-standards-qs-9000/'
    return fetch_standard(page, url)

def set_of_en(page):
    url = 'https://www.en-standard.eu/sets-of-en-standards/'
    return fetch_standard(page, url)
def ieee(page):
    url ='https://www.en-standard.eu/ieee-standards/'
    return fetch_standard(page, url)
#ETSI

def download_pdf(url, file_name):
    pass
    response = requests.get(url)
    with open(file_name, 'wb') as file:
        file.write(response.content)

def fetch_standards_etsi(page, url_template):
  
    standard = []
    url = url_template.format(page=page)
    try:
       
        response = requests.get(url)
        
        if response.status_code == 200:
            datas = response.json()
            for data in datas:
                link_data = "https://www.etsi.org/deliver/" + data["EDSpathname"].replace('\\', '') + data["EDSPDFfilename"]
                # download_pdf(link_data, data["ETSI_DELIVERABLE"])
                standard.append(data_out(
                    ten_tieng_anh=data["TITLE"],
                    so_hieu=data["ETSI_DELIVERABLE"], 
                    linh_vuc=data["TB"],
                    tu_khoa=data["Keywords"],
                    action_type=data["ACTION_TYPE"],
                    link_file=link_data,
                    name_file=data["EDSPDFfilename"]
                ))
                
            return standard
        else :
            return []
    except Exception as e:
        print(e)
        return standard

def ITS(page):
    url_template = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-24&harmonized=0&keyword=&TB=620,,702,,707,,708,,709,,710,,711&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url_template)

def Broad_Cable_Access(page):
    url_template = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=733,,786&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url_template)

def Broadband_Wireless_Access(page):
    url_template = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=287&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url_template)

def DECT(page):
    url_template = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=19,,276,,277,,278,,279,,280,,281,,515,,392,,672,,752,,855&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url_template)

def Fixed_line_Access(page):
    url_template = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=516,,518,,519,,517,,638,,602,,2,,494,,3,,4,,5,,689,,693,,733,,694,,695&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url_template)

def Mobile_and_Private_Mobile_Radio(page):
    url_template = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=Digital&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=dPMR,,PMR&TB=&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url_template)

def xDSL(page):
    url_template = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=xdsl&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=695&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url_template)

def Codes(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=387,,181&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def eHEALTH(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=696,,586&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)

def Energy_efficiency_and_environmental_aspects(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=energy&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=689,,635,,773&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page,url)

def Human_factor_and_accessibility(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=80,,81,,82,,83&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)

def Lawful_Interception_for_Mobile(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=lawful%2Binterception&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=386,,180&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)

def Quality_of_Service(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=QoS&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Safety(page): 
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=362,,432&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Smart_cities(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=smart%2Bcit&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Smart_Grids(page):
    url ="https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=Smart&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=787,,765,,470,,726&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Smart_Metering(page):
    url ="https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=smart%2Bmetering&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Broadcast(page): 
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=92&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def ENI(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=857&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url )
def F5G(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=885&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Fixed_Radio_links(page):
    url= "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=694,,235,,236,,237,,274&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page,url)
def IPE(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=892&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page,url)
def MEC(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=826,,835&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Network_functions_Virtualisation(page):
    url ="https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=826,,835,,833,,789,,832,,831,,795,,796,,800,,798,,799,,848,,797,,828&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page,url)
def NIN(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=844,,887&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Reconfigurable_Intelegnt_Surfaces(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=900&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page,url)
def Smart_Body_Area_Networks(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=804&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def ZSM(page):
    url ="https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=862&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Broadband_Statelite_Multimedia(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=Broadband%2BSatellite%2BMultimedia&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def DVB(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=satellite&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=92&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Electro_Magnetic_Compatibilty(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=EMC&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Galilieo(page):
    url ="https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=Galileo&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url )
def Maritime(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=582&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Medical_device(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=696,,586&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Mobile_communications(page):
    url ="https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=372,,376,,377,,378,,513,,496,,439,,649,,651,,653,,654,,655,,656,,535,,536,,537,,538,,622,,539,,575,,373,,379,,380,,3&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Radio(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=286,,807,,544,,442,,526,,552,,584,,586,,596,,620,,811,,846,,624,,582,,598,,729,,304,,305&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def  Radio_LAN (page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=LAN&TB=4,,287,,336,,286,,326,,329,,330,,327,,331,,328,,442,,356,,371,,304,,305&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def RT(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=549,,736,,841&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Reconfigurable_Radio(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=Reconfigurable%2Bradio&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=146,,713,,718,,719,,720,,721&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Satellite_Communication(page):
    url ="https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=162,,164,,165,,166,,167,,483,,569,,540,,482,,479,,478,,476,,477,,600,,481,,704,,676,,757,,650,,480&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Satellite_for_UMTS(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=UMTS%2FIMT-2000&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Secure_Elements(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=534,,639,,640,,714&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Short_Range_Devices(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=SRD&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page,url) 
def SIM(page):
    url ="https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=656,,534,,639,,640,,714&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)

def THz(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=908&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page,url)
def TETRA(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=218,,244,,245,,246,,543,,248,,249,,250,,441,,247&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page,url)
def Ultra_Wide_Band(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=UWB&TB=&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def IoT(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=IoT&TB=&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page,url)
def Cybersecurity(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=824,,755&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page,url )
def Digital_Signature(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=607&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def LI(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=608&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def QKD(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=723&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def QSC(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=856,,836&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def SAI(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=877&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)
def Security(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=824,,784,,607,,755,,608,,160,,161,,504,,503,,534,,639,,640,,714&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url )
def Security_algorithms(page):
    url = "https://www.etsi.org/?option=com_standardssearch&view=data&format=json&page={page}&search=algorithm&title=1&etsiNumber=1&content=0&version=0&onApproval=1&published=1&withdrawn=1&historical=1&isCurrent=1&superseded=1&startDate=1988-01-15&endDate=2024-05-25&harmonized=0&keyword=&TB=&stdType=&frequency=&mandate=&collection=&sort=1"
    return fetch_standards_etsi(page, url)


#NIST
def NIST(page):
    a =page
    url ="https://csrc.nist.gov/publications/fips"
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
    for link in link_arr_standard: 
        resonpse = requests.get(link)
        soup = BeautifulSoup(resonpse.text, 'html.parser')
        header_text = soup.find(id ='pub-header-display-container').get_text(strip= True )
        date_pub = soup.find(id ='pub-release-date').get_text(strip = True )
        abstract = soup.find(id='pub-detail-abstract-info').get_text(strip= True )
        keyword = soup.find(id = 'pub-keywords-container').get_text(strip= True)
        statuss = soup.find_all('small')
        status = statuss[len(statuss)-1].get_text(strip = True)
        links_download = soup.find(id = 'pub-local-download-link').get('href')
        author = soup.find(id = 'pub-authors-container').get_text(strip=True)
        tenfile = links_download.split('/')[-1]
        standard.append(data_out(ten_tieng_anh= header_text , so_hieu= False , link_file= links_download , name_file= tenfile,tac_gia= author, nam_ban_hanh=date_pub, tu_khoa=keyword, mo_ta=abstract))
    return standard


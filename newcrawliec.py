from bs4 import BeautifulSoup 
import requests
import datetime
import openpyxl
from openpyxl import load_workbook
from collections import namedtuple
import json
import pandas as pd 
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
print(iec(62))
    
    

        
        
        
        
        
        
        

        
        
        
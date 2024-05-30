import json
import csv 
import requests
import logging
import datetime
from bs4 import BeautifulSoup 
import time 

_logger = logging.getLogger(__name__)

def format_datetime(input_datetime_str):
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

def data_out(duong_link = False , tac_gia = False , tieu_de=False, loai = 'kho',so_hieu=False,mo_ta= False , nam_ban_hanh= False , wki_id=False,linh_vuc= False , trang_thai = 'con_hieu_luc', lih_vuc=False, tu_khoa=False, status_code=False, action_type=False, link_file=False, name_file=False):
    data = {
        "tiêu đề": tieu_de,
        "số hiệu": so_hieu,
        "nam_ban_hanh": nam_ban_hanh,
        "wki_id": wki_id,
        "lĩnh vực": lih_vuc,
        "từ khóa": tu_khoa,
        "trang_thai": trang_thai,
        "status_code": status_code,
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
def iso(page):
    URL = "https://jcl49wv5ar-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.22.1)%3B%20Browser%20(lite)%3B%20instantsearch.js%20(4.64.3)%3B%20JS%20Helper%20(3.16.2)&x-algolia-api-key=MzcxYjJlODU3ZmEwYmRhZTc0NTZlODNlZmUwYzVjNDRiZDEzMzRjMjYwNTAwODU3YmIzNjEwZmNjNDFlOTBjYXJlc3RyaWN0SW5kaWNlcz1QUk9EX2lzb29yZ19lbiUyQ1BST0RfaXNvb3JnX2VuX2F1dG9jb21wbGV0ZQ%3D%3D&x-algolia-application-id=JCL49WV5AR"
    data = []
    if page == 0 :
        return []
    links=[]
    json_data = {
                    "requests": [
                        {
                            "indexName": "PROD_isoorg_en",
                            "params": f"clickAnalytics=true&facetFilters=%5B%5B%22facet%3Astandard%22%5D%5D&facets=%5B%22facet%22%5D&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&maxValuesPerFacet=10&page={page}&query=iec&tagFilters=&userToken=anonymous-091345c9-5a26-40a9-b501-3bcf5177ba7d"
                        }
                    ]
                }
    r = requests.post(url=URL, json=json_data)

                # extracting data in json format
    data = r.json()['results'][0]['hits']
    for i in data:
        # standard = {
        #         "so_hieu": i['reference'],
        #         "Ten tieu chuan" : i["title"],
        #         "nam_ban_hanh": i['lastIndexation'],
        #         "duong_link": "https://www.iso.org/"+ i['seoURL'],
        #         "Trang thai":i['statusKey'],
        #         "File tieu chuan": "N/A",
        #         "Hieu luc": "con_hieu_luc",
            
        #         }
        standard = data_out(so_hieu=i['reference'], ten_tieng_anh=i["title"], nam_ban_hanh= i['lastIndexation'], duong_link="https://www.iso.org/"+ i['seoURL'], mo_ta= i.get('text') if 'text' in i else False ,linh_vuc=False )
        links.append(standard)
    return links
def publication(page):
    url = "https://www.itu.int/net4/ITU-T/search/GlobalSearch/RunSearch"
    arr_standard = []
    rows_per_page = 10  # Number of results per page

    while True:
        payload = {
            "Input": "iec",
            "Start": page,
            "Rows": 10,
            "SortBy": "RELEVANCE",
            "ExactPhrase": False,
            "CollectionName": "ITU-T Publications",
            "CollectionGroup": "Publications",
            "Sector": "t",
            "Criterias": [
                {
                    "Name": "Search in",
                    "Criterias": [
                        {"Selected": False, "Value": "", "Label": "Name", "Target": "/name_s", "TypeName": "CHECKBOX"},
                        {"Selected": False, "Value": "", "Label": "Short description", "Target": "/short_description_s", "TypeName": "CHECKBOX"},
                        {"Selected": False, "Value": "", "Label": "File content", "Target": "/file", "TypeName": "CHECKBOX"}
                    ],
                    "ShowCheckbox": True
                }
            ],
            "Topics": "",
            "ClientData": {
                "as": "AS45899 VNPT Corp",
                "city": "Hanoi",
                "country": "Vietnam",
                "countryCode": "VN",
                "isp": "VNPT",
                "lat": 21.0292,
                "lon": 105.8526,
                "org": "Vietnam Posts and Telecommunications Group",
                "query": "14.177.225.128",
                "region": "HN",
                "regionName": "Hanoi",
                "status": "success",
                "timezone": "Asia/Bangkok",
                "zip": ""
            },
            "Language": "en",
            "IP": "14.177.225.128",
            "SearchType": "All"
        }

        json_data = json.dumps(payload)
        form_data = {'json': json_data}
        response = requests.post(url, data=form_data)

        if response.status_code == 200:
            data = response.json()
            with open ('pub_api.json', 'w') as file :
                json.dump(data, file, indent=4)
            if not data['results']:
                break  # No more results, exit the loop
            for i in data['results']:
                tt = i['Title'].split(':')
                publication_date = None
                type_value = False

                for prop in i['Properties']:
                    if prop['Title'] == 'Publication date':
                        publication_date = prop['Value']
                    if prop['Title'] == 'Type':
                        type_value = prop['Value']

                new_data = data_out(
                    so_hieu=tt[0],
                    ten_tieng_anh=i['Title'],
                    nam_ban_hanh=publication_date if publication_date else False,
                    duong_link='https://www.itu.int' + i["Redirection"],
                    mo_ta=i["ExtractFileContent"] if "ExtractFileContent" in i else False,
                    linh_vuc=type_value if type_value else False
                )
                arr_standard.append(new_data)
        else:
            print("Failed to retrieve data:", response.status_code)
            break
    return arr_standard

def meeting_meeting(page):
                    url = "https://www.itu.int/net4/ITU-T/search/GlobalSearch/RunSearch"
                    arr_standard = []
                    if page == 0:
                        return []
                    rows_per_page = 10  # Number of results per page

                    while True:
                        payload = {
                            "Input": "iec",
                            "Start": page,  # Dynamically set the start index
                            "Rows": rows_per_page,
                            "SortBy": "RELEVANCE",
                            "ExactPhrase": False,
                            "CollectionName": "ITU-T Meeting Documents",
                            "CollectionGroup": "Meeting Documents",
                            "Sector": "t",
                            "Criterias": [
                                {
                                    "Name": "Search in ITU-T Meeting Documents",
                                    "Criterias": [
                                        {"Selected": False, "Value": "", "Label": "Persistent ID", "Target": "\/persistent_identifier_s",
                                        "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:108"},
                                        {"Selected": False, "Value": "", "Label": "Name", "Target": "\/name_s", "TypeName": "CHECKBOX",
                                        "GetCriteriaType": 0, "$$hashKey": "object:109"},
                                        {"Selected": False, "Value": "", "Label": "Title", "Target": "\/subject_s", "TypeName": "CHECKBOX",
                                        "GetCriteriaType": 0, "$$hashKey": "object:110"},
                                        {"Selected": False, "Value": "", "Label": "Content", "Target": "\/file", "TypeName": "CHECKBOX",
                                        "GetCriteriaType": 0, "$$hashKey": "object:111"}
                                    ],
                                    "ShowCheckbox": True,
                                    "Selected": False,
                                    "$$hashKey": "object:49"
                                },
                                {
                                    "Name": "Type",
                                    "Criterias": [
                                        {"Selected": False, "Value": "Administrative Document", "Label": "Administrative Document",
                                        "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0,
                                        "$$hashKey": "object:140"},
                                        {"Selected": False, "Value": "Circular", "Label": "Circular", "Target": "\/object_type_s",
                                        "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:141"},
                                        {"Selected": False, "Value": "Collective letter", "Label": "Collective letter",
                                        "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0,
                                        "$$hashKey": "object:142"},
                                        {"Selected": False, "Value": "Contribution", "Label": "Contribution", "Target": "\/object_type_s",
                                        "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:143"},
                                        {"Selected": False, "Value": "Information Document", "Label": "Information Document",
                                        "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0,
                                        "$$hashKey": "object:144"},
                                        {"Selected": False, "Value": "Report", "Label": "Report", "Target": "\/object_type_s",
                                        "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:145"},
                                        {"Selected": False, "Value": "Temporary Document", "Label": "Temporary Document",
                                        "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0,
                                        "$$hashKey": "object:146"},
                                        {"Selected": False, "Value": "Other", "Label": "Other", "Target": "\/object_type_s",
                                        "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:147"}
                                    ],
                                    "ShowCheckbox": True,
                                    "Selected": False,
                                    "$$hashKey": "object:50"
                                },
                                {
                                    "Name": "Date",
                                    "Criterias": [
                                        {"FromDateString": "1900-01-01T00:00:00Z", "ToDateString": "2024-04-13T10:47:15Z", "Label": None,
                                        "Target": "\/object_date_d", "TypeName": "DATERANGE", "GetCriteriaType": 2,
                                        "From": "1900-01-01T00:00:00.000Z", "To": "2024-04-13T10:46:54.000Z", "$$hashKey": "object:196"}
                                    ],
                                    "ShowCheckbox": False,
                                    "Selected": False,
                                    "$$hashKey": "object:51"
                                }
                            ],
                            "Topics": "",
                            "ClientData": {"as": "AS45899 VNPT Corp", "city": "Hanoi", "country": "Vietnam", "countryCode": "VN",
                                        "isp": "VNPT", "lat": 21.0292, "lon": 105.8526, "org": "Vietnam Posts and Telecommunications Group",
                                        "query": "14.177.225.128", "region": "HN", "regionName": "Hanoi", "status": "success",
                                        "timezone": "Asia/Bangkok", "zip": ""},
                            "Language": "en",
                            "IP": "14.177.225.128",
                            "SearchType": "All"
                        }

                        json_data = json.dumps(payload)
                        form_data = {'json': json_data}
                        response = requests.post(url, data=form_data)

                        if response.status_code == 200:
                            data = response.json()
                            if not data['results']:
                                break  # No more results, exit the loop
                            for i in data['results']:
                                
                                    tt = i['Title'].split(':')
                                    publication_date = None
                                    type_value = None
                                    
                                    for prop in i['Properties']:
                                        if prop['Title'] == 'Publication date':
                                            publication_date = prop['Value']
                                        if prop['Title'] == 'Type':
                                            type_value = prop['Value']
                                    # new_data = {
                                    #     "so_hieu": tt[0],
                                    #     "Ten tieu chuan(Tieng Anh)": i['Title'],
                                    #     "Ten tieu chuan(Tieng quoc gia ban hanh)": i['Title'],
                                    #     "nam_ban_hanh": i["Properties"][0]['Value'],
                                    #     "duong_link": 'https://www.itu.int' + i["Redirection"],
                                    #     "File tieu chuan": "N/A",
                                    #     "Hieu luc": "con_hieu_luc",
                                        
                                    # }
                                    new_data= data_out(so_hieu=tt[0], ten_tieng_anh= i['Title'], nam_ban_hanh=i["Properties"][0]['Value'], duong_link= 'https://www.itu.int' + i["Redirection"],mo_ta='N/A', linh_vuc=type_value if type_value else "N/A")
                                    arr_standard.append(new_data)
                        else:
                            print("Failed to retrieve data:", response.status_code)
                            break 
                        page -= rows_per_page
                        return arr_standard
def meeting_laision(page):
    arr_standard=[]
    url = "https://www.itu.int/net4/ITU-T/search/GlobalSearch/RunSearch"
    if page == 0 :
        return []
    rows_per_page = 10  # Number of results per page

    while True:
        payload = {
            "Input": "iec",
            "Start": page,
            "Rows": rows_per_page,
            "SortBy": "RELEVANCE",
            "ExactPhrase": False,
            "CollectionName": "ITU-T Meeting Documents",
            "CollectionGroup": "ITU-T Liaison Statement",
            "Sector": "t",
            "Criterias": [
                {
                    "Name": "Search in ITU-T Meeting Documents",
                    "Criterias": [
                        {"Selected": False, "Value": "", "Label": "Persistent ID", "Target": "\/persistent_identifier_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:108"},
                        {"Selected": False, "Value": "", "Label": "Name", "Target": "\/name_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:109"},
                        {"Selected": False, "Value": "", "Label": "Title", "Target": "\/subject_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:110"},
                        {"Selected": False, "Value": "", "Label": "Content", "Target": "\/file", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:111"}
                    ],
                    "ShowCheckbox": True,
                    "Selected": False,
                    "$$hashKey": "object:49"
                },
                {
                    "Name": "Type",
                    "Criterias": [
                        {"Selected": False, "Value": "Administrative Document", "Label": "Administrative Document", "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:140"},
                        {"Selected": False, "Value": "Circular", "Label": "Circular", "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:141"},
                        {"Selected": False, "Value": "Collective letter", "Label": "Collective letter", "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:142"},
                        {"Selected": False, "Value": "Contribution", "Label": "Contribution", "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:143"},
                        {"Selected": False, "Value": "Information Document", "Label": "Information Document", "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:144"},
                        {"Selected": False, "Value": "Report", "Label": "Report", "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:145"},
                        {"Selected": False, "Value": "Temporary Document", "Label": "Temporary Document", "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:146"},
                        {"Selected": False, "Value": "Other", "Label": "Other", "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:147"}
                    ],
                    "ShowCheckbox": True,
                    "Selected": False,
                    "$$hashKey": "object:50"
                },
                {
                    "Name": "Date",
                    "Criterias": [
                        {"FromDateString": "1900-01-01T00:00:00Z", "ToDateString": "2024-04-13T10:47:15Z", "Label": None, "Target": "\/object_date_d", "TypeName": "DATERANGE", "GetCriteriaType": 2, "From": "1900-01-01T00:00:00.000Z", "To": "2024-04-13T10:46:54.000Z", "$$hashKey": "object:196"}
                    ],
                    "ShowCheckbox": False,
                    "Selected": False,
                    "$$hashKey": "object:51"
                }
            ],
            "Topics": "",
            "ClientData": {"as": "AS45899 VNPT Corp", "city": "Hanoi", "country": "Vietnam", "countryCode": "VN", "isp": "VNPT", "lat": 21.0292, "lon": 105.8526, "org": "Vietnam Posts and Telecommunications Group", "query": "14.177.225.128", "region": "HN", "regionName": "Hanoi", "status": "success", "timezone": "Asia/Bangkok", "zip": ""},
            "Language": "en",
            "IP": "14.177.225.128",
            "SearchType": "All"
        }

        json_data = json.dumps(payload)
        form_data = {'json': json_data}

        response = requests.post(url, data=form_data)
        if response.status_code == 200:
            data = response.json()
            if not data['results']:
                return []  # No more results, exit the loop
            for i in data['results']:
                tt = i['Title'].split(':')
                # new_data = {
                #         "so_hieu": tt[0],
                #         "Ten tieu chuan(Tieng Anh)": i['Title'],
                #         "Ten tieu chuan(Tieng quoc gia ban hanh)": i['Title'],
                #         "nam_ban_hanh": i["Properties"][0]['Value'],
                #         "duong_link": 'https://www.itu.int/' + i["Redirection"],
                #         "File tieu chuan": "N/A",
                #         "Hieu luc": "con_hieu_luc"
                #     }
                publication_date = None
                type_value = None
                
                for prop in i['Properties']:
                    if prop['Title'] == 'Publication date':
                        publication_date = prop['Value']
                    if prop['Title'] == 'Type':
                        type_value = prop['Value']
                new_data= data_out(so_hieu=tt[0], ten_tieng_anh= i['Title'], nam_ban_hanh=i["Properties"][0]['Value'], duong_link= 'https://www.itu.int' + i["Redirection"],mo_ta='N/A', linh_vuc=type_value if type_value else "N/A")
                arr_standard.append(new_data)  # Print each new data entry for debugging
            return arr_standard
        else:
            print("Failed to retrieve data:", response.status_code)
            return []
            break 
def recommendation(page):
                    url = "https://www.itu.int/net4/ITU-T/search/GlobalSearch/RunSearch"
                    if page == 0 :
                        return []
                    arr_standard = []

                    while True:
                        payload = {
                            "Input": "iec",
                            "Start": page,
                            "Rows": 10,
                            "SortBy": "RELEVANCE",
                            "ExactPhrase": False,
                            "CollectionName": "ITU-T Recommendations",
                            "CollectionGroup": "Recommendations",
                            "Sector": "t",
                            "Criterias": [
                                {
                                    "Name": "Search in ITU-T Recommendations",
                                    "Criterias": [
                                        {"Selected": False, "Value": "", "Label": "Persistent ID", "Target": "\/persistent_identifier_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:108"},
                                        {"Selected": False, "Value": "", "Label": "Name", "Target": "\/name_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:109"},
                                        {"Selected": False, "Value": "", "Label": "Title", "Target": "\/subject_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:110"},
                                        {"Selected": False, "Value": "", "Label": "Content", "Target": "\/file", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:111"}
                                    ],
                                    "ShowCheckbox": True,
                                    "Selected": False,
                                    "$$hashKey": "object:49"
                                },
                                {
                                    "Name": "Type",
                                    "Criterias": [
                                        {"Selected": False, "Value": "Administrative Document", "Label": "Administrative Document", "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:140"},
                                        {"Selected": False, "Value": "Circular", "Label": "Circular", "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:141"},
                                        {"Selected": False, "Value": "Collective letter", "Label": "Collective letter", "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:142"},
                                        {"Selected": False, "Value": "Contribution", "Label": "Contribution", "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:143"},
                                        {"Selected": False, "Value": "Information Document", "Label": "Information Document", "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:144"},
                                        {"Selected": False, "Value": "Report", "Label": "Report", "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:145"},
                                        {"Selected": False, "Value": "Temporary Document", "Label": "Temporary Document", "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:146"},
                                        {"Selected": False, "Value": "Other", "Label": "Other", "Target": "\/object_type_s", "TypeName": "CHECKBOX", "GetCriteriaType": 0, "$$hashKey": "object:147"}
                                    ],
                                    "ShowCheckbox": True,
                                    "Selected": False,
                                    "$$hashKey": "object:50"
                                },
                                {
                                    "Name": "Date",
                                    "Criterias": [
                                        {"FromDateString": "1900-01-01T00:00:00Z", "ToDateString": "2024-04-13T10:50:37Z", "Label": None, "Target": "\/object_date_d", "TypeName": "DATERANGE", "GetCriteriaType": 2, "From": "1900-01-01T00:00:00.000Z", "To": "2024-04-13T10:50:12.000Z", "$$hashKey": "object:196"}
                                    ],
                                    "ShowCheckbox": False,
                                    "Selected": False,
                                    "$$hashKey": "object:51"
                                }
                            ],
                            "Topics": "",
                            "ClientData": {"as": "AS45899 VNPT Corp", "city": "Hanoi", "country": "Vietnam", "countryCode": "VN", "isp": "VNPT", "lat": 21.0292, "lon": 105.8526, "org": "Vietnam Posts and Telecommunications Group", "query": "14.177.225.128", "region": "HN", "regionName": "Hanoi", "status": "success", "timezone": "Asia/Bangkok", "zip": ""},
                            "Language": "en",
                            "IP": "14.177.225.128",
                            "SearchType": "All"
                        }

                        json_data = json.dumps(payload)
                        form_data = {'json': json_data}

                        response = requests.post(url, data=form_data)

                        if response.status_code == 200:
                            data = response.json()
                            if not data['results']:
                                break  # No more results, exit the loop
                            for i in data['results']:
                                
                                    tt = i['Title'].split('|')
                                    # new_data = {
                                    #     "so_hieu": tt[0],
                                    #     "Tên tiêu chuẩn": i['Title'],
                                    #     "Tên tiểu chuẩn(Tiếng quốc gia ban hành)": i['Title'],
                                    #     "nam_ban_hanh": i["Properties"][0]['Value'],
                                    #     "duong_link": 'https://www.itu.int/rec/T-REC-' + tt[0].split()[1],
                                    #     "File tieu chuan": "N/A",
                                    #     "Hieu luc": "con_hieu_luc"
                                    # }
                                    publication_date = None
                                    type_value = None
                                    
                                    for prop in i['Properties']:
                                        if prop['Title'] == 'Publication date':
                                            publication_date = prop['Value']
                                        if prop['Title'] == 'Type':
                                            type_value = prop['Value']
                                    new_data= data_out(so_hieu=tt[0], ten_tieng_anh= i['Title'], nam_ban_hanh=i["Properties"][0]['Value'], duong_link= 'https://www.itu.int' + i["Redirection"],mo_ta='N/A', linh_vuc=type_value if type_value else "N/A")
                                    
                                    
                                    arr_standard.append(new_data)
                        else:
                            print("Failed to retrieve data:", response.status_code)
                            break
                        return arr_standard
def iec():
            import requests
            from bs4 import BeautifulSoup
            url = "https://www.iec.ch/technical-committees-and-subcommittees#tclist"
            response = requests.get(url)
            arr_standard = []
                # Kiểm tra xem yêu cầu thành công hay không
            if response.status_code == 200:
                    # Parse HTML content
                soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Tìm tất cả các thẻ <td> có class là "datatable-column-publications"
                td_tags = soup.find_all('td', class_='datatable-column-publications')
                    
                    # Lấy các liên kết từ các thẻ <a> bên trong các thẻ <td>
                links = ['https://www.iec.ch'+ td.find('a')['href'] for td in td_tags if td.find('a')]
                for i in links :
                    response= requests.get(i)
                    soup =  BeautifulSoup(response.content, 'html.parser')
                    div_tag =soup.find_all('div', class_='pad10')
                    standard = [div.find('a')['href'] for div in div_tag if div.find('a')]
                    for j in standard :
                        response= requests.get(j)
                        soup =  BeautifulSoup(response.content, 'html.parser')
                        id = soup.find('h1', class_='reference')
                        title = soup.find('h2', class_='title')
                        pub_date = soup.find(id="view:inputText3")
                        abstract = soup.find(id="view:computedField3")
                        data = {
                                "so_hieu": id.text.strip(),
                                "Tên tiêu chuẩn": title.text.strip(),
                                "Tên tiêu chuẩn (tiếng quốc gia ban hành)": title.text.strip(),
                                "nam_ban_hanh": pub_date.text.strip(),
                                "duong_link" : j,
                                "File tieu chuan": "N/A",
                                "Tom tat": abstract.text.strip(),
                                "Hieu luc": "con_hieu_luc"
                            }
                        arr_standard.append(data)

            else:
                print("Yêu cầu không thành công!")
            return  arr_standard
        
        
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
        standard.append(data_out(so_hieu= so_hieu, ten_tieng_anh=ten_tieng_anh,gia = price,mo_ta=abstract, duong_link=duong_link, tac_gia= author))
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
                
                standards.append(data_out(ten_tieng_anh=title, mo_ta=descriptions, nam_ban_hanh=date_pub))
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
                # print(link_data)
                download_pdf(link_data, data["ETSI_DELIVERABLE"])
                standard.append(data_out(
                    tieu_de=data["TITLE"],
                    so_hieu=data["ETSI_DELIVERABLE"],
                    wki_id=data["wki_id"],
                    linh_vuc=["TB"],
                    tu_khoa=["Keywords"],
                    status_code=["STATUS_CODE"],
                    action_type=["ACTION_TYPE"],
                    link_file=link_data,
                    name_file=data["EDSPDFfilename"]
                ))
                
            return standard
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


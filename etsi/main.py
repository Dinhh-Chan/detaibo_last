import json
import crawler
import requests
import logging 
_logger = logging.getLogger(__name__)
json_path = 'total.json'
def get():
    try:
        result = []
        data = json.loads(open(json_path,'r').read())
        for key, value in data.items():
            if value["total_count"]> 0 :
                result += getattr(crawler,key)(value["total_count"])
                data[key]["total_count"]-=1
                with open(json_path, 'w') as file:
                    json.dump(data, file, indent=4)
                return result 
    except Exception as e :
        _logger.error('LỖI HÀM CRAW DATA')
        _logger.warning(e)
print(len(get()))
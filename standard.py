import json
import crawler
import logging

_logger = logging.getLogger(__name__)

JSON_PATH ='check_json_template.json'

def get():
    try:
        result = []
        data = json.loads(open(JSON_PATH,'r').read())
        check = True
        for key,value in data.items():
            if value > 0:
                if key != "meeting_laision" and key!= 'meeting_meeting' and key != 'publication' and key !="recommendation" :
                    if value !=0:
                        result = result + (getattr(crawler,key)(value))
                        data[key] = value - 1
                        open(JSON_PATH,'w').write(json.dumps(data))
                        return result
                else :
                    result = result + (getattr(crawler,key)(value))
                    data[key] = value - 10
                    open(JSON_PATH,'w').write(json.dumps(data))
                    return result
                check = False
        if check:
            open(JSON_PATH,'w').write(json.dumps({"iso": 2, "meeting_laision": 20, "meeting_meeting": 20, "publication": 20, "recommendation": 20}))
        return result
    except Exception as e:
        _logger.error('LỖI HÀM CRAW DATA')
        _logger.warning(e)
print(get())
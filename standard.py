import json
import crawler
import logging

_logger = logging.getLogger(__name__)

JSON_PATH ='check_json.json'

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
            open(JSON_PATH,'w').write(json.dumps({"iso":2,  "meeting_laision": 20, "meeting_meeting": 20, "publication": 20, "recommendation": 20, "ITS": 1, "Broad_Cable_Access":1, "Broadband_Wireless_Access": 1, "DECT": 5, "Fixed_line_Access": 7, "Mobile_and_Private_Mobile_Radio": 1, "xDSL": 1, "Codes": 1, "eHEALTH": 1, "Energy_efficiency_and_environmental_aspects": 1, "Human_factor_and_accessibility": 3, "Lawful_Interception_for_Mobile": 2, "Quality_of_Service": 1, "Safety": 1, "Smart_cities": 1, "Smart_Grids": 2, "Smart_Metering": 1, "Broadcast": 2, "ENI": 1, "F5G": 1, "Fixed_Radio_links": 2, "IPE": 1, "MEC": 2, "Network_functions_Virtualisation": 2, "NIN": 1, "Reconfigurable_Intelegnt_Surfaces": 1, "Smart_Body_Area_Networks": 1, "ZSM": 1, "Broadband_Statelite_Multimedia": 1, "DVB": 1, "Electro_Magnetic_Compatibilty": 2, "Galilieo": 1, "Maritime": 2, "Medical_device": 1, "Mobile_communications": 2, "Radio": 2, "Radio_LAN": 1, "RT": 1, "Reconfigurable_Radio": 2, "Satellite_Communication": 2, "Satellite_for_UMTS": 1, "NIST": 1, "Construction_and_Construction_Safety": 1, "Occupational_Health_Safety": 1, "Machine_Safety": 1, "Risk_Management": 1, "Laboratories": 1, "Cloud_Security": 1, "Energy_Management": 1, "Industrial_Robotics": 1, "IEC_Series": 1, "IEC_Redlines": 1, "Identity_Theft": 1, "NSF_Standards_Collections": 1, "Radio_Frequency_Disturbance": 1, "Electronic_Communications": 1, "ISO_Handbooks": 1, "Certification": 1, "Medical_Devices": 1, "IT_IT_Security": 1, "Quality_Management": 1, "Regenerative_Medicine": 1, "Road_Vehicles": 1, "Environmental_Management": 1, "Management": 1, "ISO_Redlines": 1, "X9_Standards_Collections": 1, "Tolerances_Measurements": 1, "SAE_Collections": 1, "Plastics": 1, "Lasers": 1, "Societal_Security": 1, "ISO_26000": 1, "Other_Packages": 1, "aiag_standard": 1, "atsm": 2, "bs": 2, "csn": 2, "CQI": 2, "DIN": 2, "IEC": 2, "ISO": 2, "UNE": 2, "VDA": 2, "eurocode": 2, "ieee": 2}))
        return result
    except Exception as e:
        _logger.error('LỖI HÀM CRAW DATA')
        _logger.warning(e)
print(get())
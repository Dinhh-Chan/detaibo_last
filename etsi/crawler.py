import requests
import json

def data_out(tieu_de=False, so_hieu=False, wki_id=False, lih_vuc=False, tu_khoa=False, status_code=False, action_type=False, link_file=False, name_file=False):
    data = {
        "tiêu đề": tieu_de,
        "số hiệu": so_hieu,
        "wki_id": wki_id,
        "lĩnh vực": lih_vuc,
        "từ khóa": tu_khoa,
        "status_code": status_code,
        "action_type": action_type,
        "đường link file": link_file,
        "tên file": name_file
    }
    return data

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


'''mongodb client'''
import json
import pymongo

try:
    with open("./config/appconfig.json", 'r') as json_file:
        APP_CONF = json.load(json_file)
except FileNotFoundError:
    print('appconfig.json not found DB')

class Client():
    def __init__(self):
        client = pymongo.MongoClient(APP_CONF['mongo-uri'])
        db = client["licenseTool"]
        self.data = db['licenses']

    def write_to_db(self, license_data):
        if license_data['EXP'] == False:
            pass
        else:
            write_db = self.data.insert_one(license_data)

    def check_if_in_db(self, license_data):
        license_check = self.data.find_one(license_data)
        return license_check
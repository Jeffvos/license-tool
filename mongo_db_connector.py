'''mongodb module'''
import json
import pymongo

with open('appconfig.json', 'r') as json_file:
    APP_CONF = json.load(json_file)


class Client:
    def __init__(self):
        ''' init mongo '''
        db_runner = pymongo.MongoClient(APP_CONF['mongo-uri'])
        data_collection = db_runner['license-check']
        self.data = data_collection['licenses']

    def write_to_db(self, data):
        ''' write to collection '''
        write_db = self.data.insert_one(data)
        return write_db.acknowledged

    def check_if_in_db(self, data):
        ''' check if exist in the mongo collection'''
        return self.data.find_one(data)

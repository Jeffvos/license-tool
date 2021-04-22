import json
from datetime import datetime
from clients import database

try:
    with open("./config/appconfig.json", 'r') as json_file:
        APP_CONF = json.load(json_file)
except FileNotFoundError:
    print('appconfig.json not found Validation')

database = database.Client()

class Validate:
    def __init__(self):
        pass

    def check_validity(self, json_data):
        current_time = datetime.now()
        sen = json_data['SEN']
        if not json_data['expiresAt']:
            date_valid = False
        else:
            try :
                date_valid = datetime.strptime(json_data['expiresAt'], '%d/%b/%y')
            except ValueError:
                date_valid = datetime.strptime(json_data['expiresAt'], '%b %d, %Y')
            days=date_valid - current_time
        if date_valid is False or days.days < 30:
            to_db = {'INSTANCE': json_data['INSTANCE'],
                     'SEN': sen, 'EXP': date_valid}
            database.write_to_db(to_db)

    def check_sen(self, json_data, instance):
        try:
            sen = json_data['supportEntitlementNumber']
        except KeyError:
            sen = json_data['pluginKey']
        try:
            expiresAt = json_data['maintenanceExpiryDateString']
        except KeyError:
            expiresAt = json_data['active']

        check_sen = database.check_if_in_db({'SEN': sen})
        if not check_sen:
            return_data = {'INSTANCE': instance,
                           'expiresAt': expiresAt,
                           'SEN': sen}
            self.check_validity(return_data)
        else:
            pass

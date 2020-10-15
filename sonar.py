'''Check license of SonarQube instance'''
import json
import requests
from datetime import datetime

import mongo_db_connector

with open('appconfig.json', 'r') as json_file:
    APP_CONF = json.load(json_file)


class Check:

    def __init__(self):
        user = APP_CONF['sonar']['user']
        password = APP_CONF['sonar']['pass']
        self._license_url = APP_CONF['sonar']['license_url']
        self._auth_user = (user, password)

    def _create_request(self):
        url = self._license_url
        req = requests.request("GET", url, auth=self._auth_user, verify=False)
        json_data = req.json()
        return self._check_license(json_data)

    def _check_license(self, json_data):
        license_data = json_data['isExpired']
        if not license_data:
            self._check_validity(json_data)
        else:
            print('Expired')

    def _check_validity(self, json_data):
        current_time = datetime.now()
        date_valid = datetime.strptime(json_data['expiresAt'], "%Y-%m-%d")
        days_exp = date_valid - current_time
        server_id = json_data['serverId']
        if days_exp.days < 30:
            data_insert = {'INSTANCE': 'SONAR', 'SERVER_ID': server_id, 'EXP': date_valid}
            mongo_db_connector.Client().write_to_db(data_insert)

        else:
            print(json_data['serverId'])
            print(days_exp.days, "days until exp")

    def run(self):
        return self._create_request()

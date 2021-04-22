'''Sonar license plugin work in porgress'''
import json
import requests
from clients.validation import Validate

try:
    with open("./config/appconfig.json", 'r') as json_file:
        APP_CONF = json.load(json_file)
except FileNotFoundError:
    print('appconfig.json not found')
    
class CheckSonar:
    def __init__(self):
        user = APP_CONF['sonar']['user']
        passw = APP_CONF['sonar']['pass']
        self._license_url = APP_CONF['sonar']['license_url']
        self._auth_user = (user, passw)

    def _create_request(self):
        url = self._license_url
        req = requests.request("GET", url, auth=self._auth_user, verify=False)
        json_data = req.json()
        return Validate.check_validity(json_data)

    def _check_license(self, json_data):
        license_data = json_data['isExpired']
        if not license_data:
            Validate.check_validity(json_data)
        else:
            print('Expired')

    def call(self):
        return self._create_request()

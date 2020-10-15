'''Jira apps module for checking apps/plugin licenses'''
import json
import requests
from datetime import datetime

import mongo_db_connector

with open('appconfig.json', 'r') as json_file:
    APP_CONF = json.load(json_file)


class Check():
    '''jira apps/plugins license checker'''
    def __init__(self):
        user = APP_CONF['jira']['user']
        password = APP_CONF['jira']['pass']
        self._api_url = APP_CONF['jira']['url']
        self._base_url = APP_CONF['jira']['base-url']
        self._jira_headers = APP_CONF['jira']['headers']
        self._jira_auth = (user, password)
        self._plugins = {}

    def _compose_url(self):
        '''compose request url'''
        url = self._api_url + "/rest/plugins/1.0/"
        return self._request(url)

    def _return_request(self, return_url):
        url = self._base_url + return_url
        req = requests.request("GET", url, auth=self._jira_auth)
        json_data = req.json()
        sen = {'SEN': json_data['supportEntitlementNumber']}
        check_sen = mongo_db_connector.Client().check_if_in_db(sen)
        if not check_sen:
            return self._check_validity(json_data['supportEntitlementNumber'],
                                        json_data['maintenanceExpiryDateString'])

    def _request(self, url):
        req = requests.request("GET", url, auth=self._jira_auth)
        json_req = req.json()
        plugin_count = 0
        while plugin_count < len(json_req['plugins']):
            if json_req['plugins'][plugin_count]['usesLicensing']:
                self._plugins[json_req['plugins'][plugin_count]
                              ['name']] = json_req['plugins'][plugin_count]
            plugin_count += 1
        return self._check_all()

    def _check_all(self):
        for plugin in self._plugins:
            return_url = self._plugins[plugin]['links']['self'] + "/license"
            return self._return_request(return_url)

    def _check_validity(self, sen, expiry_date):
        now = datetime.now()
        plugin_expiry = datetime.strptime(expiry_date, "%d/%b/%y")
        days_exp = plugin_expiry - now
        to_db = {'INSTANCE': 'JIRA', 'SEN': sen, 'EXP': plugin_expiry}
        if days_exp.days < 30:
            print(sen, " plugin will or is expired in\n", days_exp.days, "days")
            mongo_db_connector.Client().write_to_db(to_db)
        else:
            print(sen, "still valid", days_exp.days)

    def run(self):
        '''init call'''
        return self._compose_url()

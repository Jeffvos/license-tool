'''atlassian (jira & confluence) apps module for checking apps/plugin licenses'''
import json
import requests
from clients import database
from clients.validation import Validate

try:
    with open("./config/appconfig.json", 'r') as json_file:
        APP_CONF = json.load(json_file)
except FileNotFoundError:
    print('appconfig.json not found')

validation = Validate()

class CheckAtlassian:
    def __init__(self):
        user = APP_CONF['instances']['jira']['user']
        passw = APP_CONF['instances']['jira']['pass']
        self._base_url = ""
        self._jira_headers = {"content-type": "application/json"}
        self._jira_auth = (user, passw)
        self._plugins = {}

    def _compose_url(self):
        for i in APP_CONF['instances']:
            self._base_url = APP_CONF['instances'][i]['baseUrl']
            url = APP_CONF['instances'][i]['baseUrl'] + "/rest/plugins/1.0/"
            instance = APP_CONF['instances'][i]["name"]
            self._request(url, instance)
        return

    def _return_request(self, return_url, instance):
        url = self._base_url + return_url
        req = requests.request("GET", url, auth=self._jira_auth)
        jsondata = req.json()
        return validation.check_sen(jsondata, instance)

    def _request(self, url, instance):
        req = requests.request("GET", url, auth=self._jira_auth)
        json_req = req.json()
        plugin_count = 0
        while plugin_count < len(json_req['plugins']):
            if json_req['plugins'][plugin_count]['usesLicensing']:
                self._plugins[json_req['plugins'][plugin_count]
                              ['name']] = json_req['plugins'][plugin_count]
            plugin_count += 1
        return self._check_all(instance)

    def _check_all(self, instance):
        for plugin in self._plugins:
            return_url = self._plugins[plugin]['links']['self'] + "/license"
            check_license = self._return_request(return_url, instance)
        print('Done')

    def call(self):
        print("Checking Atlassian plugin licenses..")
        return self._compose_url()


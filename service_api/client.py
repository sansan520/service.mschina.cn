# coding:utf8

import requests
import json

# sudo pip install requests


class JsonTest(object):

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {}
        self.token = None

    def ho_login(self, ho_account, ho_password, path = "/api/v1.0/ho_login"):
        entity = {"ho_account": ho_account, "ho_password": ho_password}
        self.headers ={"content-type": "application/json"}
        response = requests.post(url=self.base_url+path,
                                 data = json.dumps(entity),
                                 headers = self.headers)
        response_data = json.loads(response.content.decode('utf-8'))
        self.token = response_data.get("token")
        return response_data

    def get_ho_by_token(self, path = "/api/v1.0/get_ho_by_token"):
        self.headers = {"token": self.token}
        response = requests.get(url=self.base_url+path, headers =self.headers)
        response_data = json.load(response.content)
        return  response_data

    def logout(self, path = "/api/v1.0/logout"):
        self.headers = {"token": self.token}
        response = requests.get(url=self.base_url + path, headers=self.headers)
        response_data = json.load(response.content)
        return response_data


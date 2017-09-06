import requests
import json
import xlsxwriter

# setting domain url, login and set header of requests
domain_config='localhost:8000'
base_url = 'http://' + domain_config
header_content = {'Content-Type': 'application/json'}

def login (username, password):
    url_login = base_url + '/api/v1/authentication/login'
    data_login = {'username': username, 'password': password}
    return requests.post(url_login, data = json.dumps(data_login), headers=header_content).json()

def get_headers(login_data):
    return {'Authorization': 'ApiKey ' + login_data['username'] + ':' + login_data['api_key'], \
            'Organization': login_data['user_in_organization'][1]['organization'], \
            'Role': login_data['user_in_organization'][1]['role']}
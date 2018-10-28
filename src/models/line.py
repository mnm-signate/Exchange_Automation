# coding=utf-8
import requests

def execute(body, token, api):
    payload = {'message': body}
    headers = {'Authorization': 'Bearer ' + token}
    line_notify = requests.post(api, data=payload, headers=headers)

# coding=utf-8
import requests

def execute(body):
    line_notify_token = '自分のline_notifyのtoken'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    message = body

    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)

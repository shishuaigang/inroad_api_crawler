# -*- coding: utf-8 -*-
import json


class response_status:
    def __init__(self, length):
        self.length = length

    def res_status(self, response):
        respon_status = []
        for i in range(self.length):
            try:
                s = json.loads(str(response[i].text))
                respon_status.append(s['status'])
            except Exception:
                respon_status.append('-1')
        return respon_status


class error_message:
    def __init__(self, length):
        self.length = length

    def error_mes(self, response):
        error_message = []
        for i in range(self.length):
            try:
                s = json.loads(str(response[i].text))
                error_message.append(s['error']['message'])
            except Exception:
                error_message.append('response中无返回，请确认')
        return error_message

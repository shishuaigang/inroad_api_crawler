# -*- coding: utf-8 -*-
import os
import codecs
import json
import sys
import copy
from more_itertools import chunked
reload(sys)
sys.setdefaultencoding('utf8')


class api_num:
    def __init__(self, path):
        self.path = path

    @property
    def json_data(self):
        for files in os.walk(self.path):
            json_file = files[2]
        return json_file

    def every_json_api_number(self):  # 每个json文件下有多少个API，存入list
        os.chdir(self.path)
        return [len((json.loads(codecs.open(self.json_data[i], encoding='utf-8').read()))["apis"])
                for i in range(len(self.json_data))]


class api_url(api_num):
    def api_url(self):
        count = self.every_json_api_number()
        url = []
        for m in range(len(self.json_data)):
            f = codecs.open(self.json_data[m], encoding='utf-8')
            dict_json = json.loads(f.read())
            if "NoNeed" not in dict_json.keys() or dict_json["NoNeed"] == str(0):
                for n in range(count[m]):
                    if "NoNeed" not in dict_json["apis"][n] or dict_json["apis"][n]["NoNeed"] == str(0):
                        url.append(dict_json["apis"][n]["url"])
        return url


class api_cn_name(api_num):
    def api_chinese_name(self):
        count = self.every_json_api_number()
        api_chinese_name = []
        for m in range(len(self.json_data)):
            f = codecs.open(self.json_data[m], encoding='utf-8')
            dict_json = json.loads(f.read())
            if "NoNeed" not in dict_json.keys() or dict_json["NoNeed"] == str(0):
                for n in range(count[m]):
                    if "NoNeed" not in dict_json["apis"][n] or dict_json["apis"][n]["NoNeed"] == str(0):
                        api_chinese_name.append(dict_json["apis"][n]["summary"])  # api的中文名字
        return api_chinese_name


class api_cor_params(api_url):
    def api_details(self):
        count = self.every_json_api_number()
        param_all_details = []
        for m in range(len(self.json_data)):
            f = codecs.open(self.json_data[m], encoding='utf-8')
            dict_json = json.loads(f.read())
            if "NoNeed" not in dict_json.keys() or dict_json["NoNeed"] == str(0):
                for n in range(count[m]):
                    if "NoNeed" not in dict_json["apis"][n] or dict_json["apis"][n]["NoNeed"] == str(0):
                        param_all_details.append(dict_json["apis"][n]["params"])
        return param_all_details

    def api_correct_params(self):
        params = []
        api_param_details = self.api_details()
        for i in range(len(self.api_url())):
            params_keys = []
            params_values = []
            for j in range(len(api_param_details[i].keys())):
                params_keys.append(api_param_details[i].keys()[j])
                params_values.append(str(api_param_details[i].values()[j]["default"]))
            params.append(dict(zip(params_keys, params_values)))
        return params


class api_err_params(api_cor_params):
    def api_error_params(self, error_list):
        p_c = self.api_correct_params()
        total_keys = []
        total_values = []
        error_keys = []
        error_values = []
        for i in range(len(p_c)):
            total_keys.append((copy.deepcopy(p_c[i].keys())) * len(error_list) * len(p_c[i].keys()))
            total_values.append((copy.deepcopy(p_c[i].values())) * len(error_list) * len(p_c[i].keys()))
            KEY = list(chunked(total_keys[i], (len(p_c[i].keys()) * len(error_list))))
            VALUE = list(chunked(total_values[i], (len(p_c[i].keys()) * len(error_list))))
            error_keys.append(copy.deepcopy(KEY))
            error_values.append(copy.deepcopy(VALUE))
            for j in range(len(p_c[i].keys())):
                for k in range(len(error_list)):
                    error_values[i][j][len(p_c[i].keys())*k+j] = error_list[k]
        return [error_keys, error_values]

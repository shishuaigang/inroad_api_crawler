import os
import codecs
import json

'''
读取json文件
解决原始文件带boom头的问题
排除原始文件内不是api param的json文件
produce.json为nobel专用文件，不读取
'''


class ReadJson:
    def __init__(self, path):
        self.path = path

    @property
    # @property可以将python定义的函数“当做”属性访问(只读)
    def json_data(self):
        json_file = None
        for files in os.walk(self.path):
            json_file = files[2]
        return [json_file[i] for i in range(len(json_file)) if
                json_file[i].endswith(".json") and not json_file[i].startswith("produce")]  # 粗略判断文件是否以.json结尾

    def json_rm_boom(self):  # 解决原始文件带boom头的问题，排除原始文件内不是api param的json文件,直接返回dict
        os.chdir(self.path)
        temp = []
        for i in range(len(self.json_data)):
            data = codecs.open(self.json_data[i], encoding='utf-8-sig').read()
            if data[:3] == codecs.BOM_UTF8:
                tem = data[3:]
            else:
                tem = data
            try:
                if json.loads(tem)['section']:
                    temp.append(json.loads(tem))
            except Exception:
                pass
        return temp

    def read_section(self):  # 返回每个section下value的值
        os.chdir(self.path)
        rm_boom_data = self.json_rm_boom()
        re = []
        temp = [rm_boom_data[i]['section'] for i in range(len(rm_boom_data))]
        for i in range(len(temp)):
            result = []
            for j in range(len(temp[i])):
                result.append(temp[i][j]['value'])  # i=0时，result的第一个元素插入了temp[i]下面的所有value的值
            re.append(result)
        return re

    def every_json_api_number(self):  # 每个json文件下有多少个API，存入list
        # 返回格式[[15], [27, 6, 4, 3, 6, 5, 3, 8, 4, 3, 18, 6, 6], [63], [38]]
        os.chdir(self.path)
        rm_boom_data = self.json_rm_boom()
        sec = self.read_section()
        re = []
        for i in range(len(rm_boom_data)):
            result = []
            for j in range(len(sec[i])):
                result.append(len(rm_boom_data[i][sec[i][j]]))
            re.append(result)
        return re

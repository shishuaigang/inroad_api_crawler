from Test_scripts.readjson import ReadJson


class AllAPI(object):
    RJ = ReadJson("/Volumes/ApiForTest")
    num = RJ.every_json_api_number()
    array_name = RJ.read_section()
    rm_boom_data = RJ.json_rm_boom()

    def all_api(self):
        api = []
        for m in range(len(self.rm_boom_data)):
            dict_json = self.rm_boom_data[m]
            for n in range(len(self.num[m])):  # num[m]是一个list
                for k in range(self.num[m][n]):
                    api.append(dict_json[self.array_name[m][n]][k])
        return api

    def api_url(self):
        url = []
        for m in range(len(self.rm_boom_data)):
            dict_json = self.rm_boom_data[m]
            for n in range(len(self.num[m])):  # num[m]是一个list
                for k in range(self.num[m][n]):
                    url.append(dict_json[self.array_name[m][n]][k]["url"])
        return url

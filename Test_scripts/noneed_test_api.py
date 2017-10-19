from Test_scripts.readjson import ReadJson

'''
计算本地noneed的api
再利用差集来算需要测试的api
'''

'''
class ApiUrlWithoutNoneed(ReadJson):
    def api_url(self):
        num = self.every_json_api_number()
        array_name = self.read_section()
        rm_boom_data = self.json_rm_boom()
        url = []
        for m in range(len(rm_boom_data)):
            dict_json = rm_boom_data[m]
            if "NoNeed" not in dict_json.keys() or dict_json["NoNeed"] == str(0):
                for n in range(len(num[m])):  # num[m]是一个list
                    for k in range(num[m][n]):
                        if "NoNeed" not in dict_json[array_name[m][n]][k] or dict_json[array_name[m][n]][k][
                            "NoNeed"] == str(0):
                            url.append(dict_json[array_name[m][n]][k]["url"])
        return url

    def reg_api_loc(self):  # register这个api的位置
        url = self.api_url()
        for i in range(len(url)):
            if url[i] == "API/Account/Register":
                return i

    def getmobcode_api_loc(self):  # register这个api的位置
        url = self.api_url()
        for i in range(len(url)):
            if url[i] == "API/Account/GetMobCode":
                return i


class ApiCNnameWithoutNoneed(ReadJson):
    def api_chinese_name(self):
        num = self.every_json_api_number()
        array_name = self.read_section()
        rm_boom_data = self.json_rm_boom()
        api_chinese_name = []
        for m in range(len(rm_boom_data)):
            dict_json = rm_boom_data[m]
            if "NoNeed" not in dict_json.keys() or dict_json["NoNeed"] == str(0):
                for n in range(len(num[m])):
                    for k in range(num[m][n]):
                        if "NoNeed" not in dict_json[array_name[m][n]][k] or dict_json[array_name[m][n]][k][
                            "NoNeed"] == str(0):
                            api_chinese_name.append(dict_json[array_name[m][n]][k]["summary"])  # api的中文名字
        return api_chinese_name


class api_cor_params(ApiUrlWithoutNoneed):
    def api_details(self):
        num = self.every_json_api_number()
        array_name = self.read_section()
        rm_boom_data = self.json_rm_boom()
        param_all_details = []
        for m in range(len(rm_boom_data)):
            dict_json = rm_boom_data[m]
            if "NoNeed" not in dict_json.keys() or dict_json["NoNeed"] == str(0):
                for n in range(len(num[m])):
                    for k in range(num[m][n]):
                        if "NoNeed" not in dict_json[array_name[m][n]][k] or dict_json[array_name[m][n]][k][
                            "NoNeed"] == str(0):
                            param_all_details.append(dict_json[array_name[m][n]][k]["params"])
        return param_all_details

    def api_correct_params(self):
        params = []
        api_param_details = self.api_details()
        for i in range(len(self.api_url())):
            params_keys = []
            params_values = []
            for j in range(len(api_param_details[i].keys())):
                params_keys.append(list(api_param_details[i].keys())[j])
                params_values.append(str(list(api_param_details[i].values())[j]["default"]))
            params_keys.append("APIVersion")
            params_values.append("999999999")
            params.append(dict(zip(params_keys, params_values)))
        return params

    def api_modify_params(self):
        i = self.reg_api_loc()
        prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                   "153", "155", "156", "157", "158", "159", "177", "180", "181", "182", "183", "186", "187", "188",
                   "189"]
        params = self.api_correct_params()
        params[i]['phonenumber'] = random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))
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
                    error_values[i][j][len(p_c[i].keys()) * k + j] = error_list[k]
        return [error_keys, error_values]

'''


class ApiWithNoneed(object):
    RJ = ReadJson("E:\\Original_code\\inroad_api_crawler\\APIcrawler_json_data")
    num = RJ.every_json_api_number()
    array_name = RJ.read_section()
    rm_boom_data = RJ.json_rm_boom()

    def api_url(self):
        url = []
        for m in range(len(self.rm_boom_data)):
            if "NoNeed" not in self.rm_boom_data[m].keys():
                for n in range(len(self.num[m])):  # num[m]是一个list
                    for k in range(self.num[m][n]):
                        if "NoNeed" in self.rm_boom_data[m][self.array_name[m][n]][k]:
                            url.append(self.rm_boom_data[m][self.array_name[m][n]][k]["url"])
            else:
                for n in range(len(self.num[m])):  # num[m]是一个list
                    for k in range(self.num[m][n]):
                        url.append(self.rm_boom_data[m][self.array_name[m][n]][k]["url"])
        return url

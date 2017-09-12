import random

from Test_scripts.need_test_api import NeedTestApi


class APIparam(object):
    nta = NeedTestApi.need_test_api()
    length = len(nta)

    def url(self):
        return [self.nta[i]['url'] for i in range(self.length)]

    def cn_name(self):
        return [self.nta[i]['summary'] for i in range(self.length)]

    def params(self):
        prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                   "153", "155", "156", "157", "158", "159", "177", "180", "181", "182", "183", "186", "187", "188",
                   "189"]
        temp = [self.nta[i]['params'] for i in range(self.length)]
        params = []
        for i in range(self.length):
            params_keys = []
            params_values = []
            for j in range(len(temp[i].keys())):
                params_keys.append(list(temp[i].keys())[j])
                params_values.append(str(list(temp[i].values())[j]["default"]))
            params_keys.append("APIVersion")
            params_values.append("999999999")
            params.append(dict(zip(params_keys, params_values)))
        for index in range(self.length):
            if self.nta[index]['url'] == "API/Account/Register":
                params[index]['phonenumber'] = random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))
        return params

from Test_scripts.all_api import AllAPI
from Test_scripts.noneed_test_api import ApiWithNoneed


class NeedTestApi(object):
    @staticmethod
    def need_test_api():
        # 第一步，获取所有API
        all_url = AllAPI().api_url()
        # 第二步，获取 noneed的 api
        noneed = ApiWithNoneed().api_url()
        url = list(set(all_url) - set(noneed))
        # url.sort(key=all_url.index)
        all_api = AllAPI().all_api()
        return [all_api[i] for i in range(len(all_api)) if all_api[i]['url'] in url]

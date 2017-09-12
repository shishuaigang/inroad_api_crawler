from Test_scripts.get_api_param import APIparam
import requests


class ApiResponse(object):
    def __init__(self, url, param):
        self.url = url
        self.params = param

    def res_results(self, cookie, api_version, header):
        """
        :param cookie: value参数为cookie的值
        :param api_version: apiversion
        :return: 返回response
        """
        response_result = []
        for i in range(APIparam.length):
            results = requests.post("http://192.168.31.99:8088/" + self.url[i],
                                    data=self.params[i],
                                    cookies=cookie,
                                    headers=header
                                    )
            response_result.append(results)
        return response_result


'''
class api_err_res(error):
    def res_results(self, cookie, api_version, error_list, headers):
        """
        发送带有错误参数的请求
        :param cookie: value参数为cookie的值
        :param api_version: apiversion
        :param error_list: 自定义的错误参数类型
        :return: 返回response的status_code,text
        """
        response_result = []
        api_url = self.api_url()
        p_e = self.api_error_params(error_list)
        for i in range(len(p_e[0])):
            result = []
            for j in range(len(p_e[0][i])):
                _KEY = list(chunked(p_e[0][i][j], len(p_e[0][i])))
                _VALUE = list(chunked(p_e[1][i][j], len(p_e[0][i])))
                _result_min = []
                for k in range(len(error_list)):
                    results = requests.post("http://192.168.31.99:8088/" + api_url[i],
                                            data=dict(zip(_KEY[k], _VALUE[k])), cookies=cookie, headers=headers)
                    _result_min.append(results)
                result.append(_result_min)
            response_result.append(result)
        return response_result
'''

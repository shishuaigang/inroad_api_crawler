# -*- coding: utf-8 -*-
import json
import csv


class gen_result:
    def __init__(self, conf, path, inroad_url, api_len, cn_name, response, response_code, response_time, response_staus):
        """
        初始化
        :param conf: config.json
        :param path: script directory
        :param inroad_url: inroad api url
        :param api_len: api length
        :param cn_name: api chinese name
        :param response: api response
        :param response_code: api response_code
        :param response_time: api response_time
        :param response_staus: api response_staus
        """
        self.conf = conf
        self.path = path
        self.url = inroad_url
        self.api_len = api_len
        self.cn_name = cn_name
        self.res = response
        self.res_code = response_code
        self.res_time = response_time
        self.res_status = response_staus

    # 生成temp.html
    def create_html(self, passrate):
        f = open(self.path + r'\\temp.html', 'wb')
        message = """
            <html>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <head>
            <title>Inroad API遍历测试</title>
            </head>
            <body>
            <h1 align="center" style="color:black">Inroad_All_API_test </h1>
            <table border="1" cellspacing="0">
            <tr>
                <td align="center">总数</td>
                <td align="center">成功数</td>
                <td align="center">失败数</td>
                <td align="center">成功率</td>
            </tr>
                    """
        f.write(message)
        f.close()
        f1 = open(self.path + r'\\temp.html', 'a')
        f1.write('<tr>')
        f1.write('<td align="center">' + str(self.api_len) + '</td>')
        f1.write('<td align="center" bgcolor="lightgreen">' + str(passrate[0]) + '</td>')
        f1.write('<td align="center" bgcolor="red">' + str(passrate[1]) + '</td>')
        f1.write('<td align="center">' + str(passrate[2]) + '</td>')  # 以百分比显示成功率，2位小数
        f1.write('</table>')
        f1.write('<h2 align="center" style="color:black">详细信息</h2>')
        f1.write('<table style="TABLE-LAYOUT:fixed" border="1" cellspacing="0">')
        f1.write('<tr>')
        f1.write('<td align="center">序号</td>')
        f1.write('<td align="center">API_URL</td>')
        f1.write('<td align="center">API_Chinese_name</td>')
        f1.write('<td align="center">Response_Time</td>')
        f1.write('<td align="center">Response_Code</td>')
        f1.write('<td align="center">Status</td>')
        f1.write('<td style="WORD-WRAP: break-word;word-break:break-all" align="center">Error message</td>')
        f1.write('</tr>')
        for i in range(self.api_len):
            f1.write('<tr>')
            f1.write('<td align="center">' + str(i + 1) + '</td>')
            f1.write('<td align="center">' + self.url[i] + '</td>')
            f1.write('<td align="center">' + self.cn_name[i] + '</td>')
            f1.write('<td align="center">' + str(self.res_time[i]) + 'ms</td>')
            # response code为200且status为1，code和status颜色为绿色，error message N/A
            if self.res_code[i] == 200 and self.res_status[i] == 1:
                f1.write('<td align="center" bgcolor="lightgreen">' + str(self.res_code[i]) + '</td>')
                f1.write('<td align="center" bgcolor="lightgreen">' + str(1) + '</td>')
                f1.write('<td style="WORD-WRAP: break-word;word-break:break-all" align="center">' + 'N/A' + '</td>')
            # response code为200且status为0，code颜色为绿色，status为红色，填入error message
            elif self.res_code[i] == 200 and self.res_status[i] == 0:
                f1.write('<td align="center" bgcolor="lightgreen">' + str(self.res_code[i]) + '</td>')
                f1.write('<td align="center" bgcolor="red">' + str(0) + '</td>')
                f1.write('<td style="WORD-WRAP: break-word;word-break:break-all" align="center">' + (json.loads(str(self.res[i].text)))['error']['message'] + '</td>')
            # response code为500，颜色为红色，填入Response code : 500, Sever Error
            elif self.res_code[i] == 500:
                f1.write('<td align="center" bgcolor="purple">' + str(self.res_code[i]) + '</td>')
                f1.write('<td align="center" bgcolor="purple">''</td>')
                f1.write('<td style="WORD-WRAP: break-word;word-break:break-all" align="center">Response code : 500, Sever Error</td>')
            else:
                f1.write('<td align="center" bgcolor="red">' + str(self.res_code[i]) + '</td>')
                f1.write('<td align="center" bgcolor="red">''</td>')
                f1.write('<td style="WORD-WRAP: break-word;word-break:break-all" align="center">' + self.res[i].text + '</td>')
            f1.write('</tr>')
        f1.write('</table>')
        f1.write('</body>')
        f1.write('</html>')
        f1.close()

    def create_csv(self):
        with open(self.path + r'\\temp.csv', 'wb') as csvfile:
            a = csv.writer(csvfile, dialect='excel')
            a.writerow(['API_URL', 'API_ChineseName', 'Response_code', 'Response_time', 'Response_status', 'Error_Message'])
            for i in range(self.api_len):
                if self.res_code[i] == 200 and self.res_status[i] == 1:
                    a.writerow([str(self.url[i]), str(self.cn_name[i]).replace('\'', '#'), str(self.res_code[i]), str(self.res_time[i]) + 'ms', str(self.res_status[i]), 'N/A'])
                elif self.res_code[i] == 200 and self.res_status[i] == 0:
                    a.writerow([str(self.url[i]), str(self.cn_name[i]).replace('\'', '#'), str(self.res_code[i]), str(self.res_time[i]) + 'ms', str(self.res_status[i]), str((json.loads(str(self.res[i].text)))['error']['message']).replace('\'', '#')])
                else:
                    a.writerow([str(self.url[i]), str(self.cn_name[i]).replace('\'', '#'), str(self.res_code[i]), str(self.res_time[i]) + 'ms', str(self.res_status[i]), 'Please check the testreport'])

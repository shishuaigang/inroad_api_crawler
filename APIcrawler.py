import os
import json
import codecs
import time
import platform
import yaml
from Test_scripts import api_response, getcookie, sendmail, write_database, get_api_param
from Test_scripts import generate_result, status_errormessage, pass_rate, separate_backup_db

if __name__ == "__main__":
    bt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 测试开始时间
    print('测试开始: ' + bt)

    testNo = time.strftime('%Y%m%d%H%M', time.localtime())
    cur_dir = os.path.dirname(os.getcwd())

    print('备份分离数据库')
    param = yaml.load(open(cur_dir + '\\Config\\db_config.yaml'))
    separate_backup_db.Separate_Backup_DB(param['dbname'], param['host'], param['user'],
                                          param['password']).copy_database()

    conf = json.loads(codecs.open(cur_dir + '\\Config\\config.json', encoding='utf-8').read())
    api_ver = conf['api_version']
    cookie = getcookie.gecookie(api_ver)
    inroad_url = get_api_param.APIparam().url()  # api的url的地址
    cn_name = get_api_param.APIparam().cn_name()  # api的中文名字
    params = get_api_param.APIparam().params()  # api的参数
    api_len = len(inroad_url)  # 获取api的个数
    print('测试API的数目为: ' + str(api_len))
    headers = {"Referer": "123"}
    res = api_response.ApiResponse(inroad_url, params).res_results(cookie, api_ver, headers)
    res_code = [res[i].status_code for i in range(api_len)]
    res_time = ['%.1f' % (float(res[i].elapsed.microseconds) / 1000) for i in range(api_len)]
    res_status = status_errormessage.ResponseStatus(api_len).res_status(res)
    err_mes = status_errormessage.ErrorMessage(api_len).error_mes(res)
    passrate = pass_rate.PassRate(api_len).pass_rate(res_status, res_code)  # 计算成功率
    et = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 测试结束时间
    # 创建temp.html
    generate_result.GenerateResult(conf, cur_dir, inroad_url, api_len, cn_name, res, res_code, res_time,
                                   res_status).create_html(passrate, bt, et, testNo)

    os.chdir(cur_dir)
    print('尝试将测试结果写入数据库...')
    if write_database.WriteDB(conf['db_name'], conf['db_host'], conf['db_username'], conf['db_userpasswd'],
                              testNo).write_db(inroad_url, cn_name, res_code, res_time, res_status, err_mes) == 1:
        print('尝试发送测试报告...')
        try:
            sendmail.SendMail(conf['receiver_list'], conf['mail_subject'], testNo).send_mail()
            print('测试报告发送成功,API遍历测试完成')
        except Exception:
            print('发送邮件失败')
    else:
        print('写入数据库或者测试报告发送失败,请检查脚本和错误信息')

# coding:utf-8
import os
import pymssql
import shutil


class write_db:
    def __init__(self, dbname, host, username, password, t):
        self.dbname = dbname
        self.host = host
        self.username = username
        self.password = password
        self.t = t

    def write_db(self, url, cnname, res_code, res_tim, res_status, error_mes):
        try:  # 判定是否存在temp.csv，如没有，则抛出异常
            os.chdir('Test_results')
            if os.path.exists(r'temp.html'):
                os.remove('temp.html')
            os.chdir(os.path.dirname(os.getcwd()))
            shutil.move('temp.html', 'Test_results')
            os.chdir('Test_results')
            print u'连接数据库'
            conn = pymssql.connect(host=self.host, user=self.username, password=self.password, database=self.dbname)
            cur = conn.cursor()
            print u"开始写入数据库"
            sql = "insert into Inroad_Crawler_Test(TestNo, API_URL, API_ChineseName, Response_code, Response_time,Response_status, Error_Message) values(%s,%s,%s,%s,%s,%s,%s)"
            for i in range(len(url)):  # 循环写入数据库
                cur.execute(sql, (self.t, url[i], cnname[i].decode('utf-8'), res_code[i], res_tim[i], res_status[i], error_mes[i]))
            conn.commit()
            cur.close()
            conn.close()
            print u"写入成功"
            return 1
        except Exception:
            print u"写入失败"
            return 0

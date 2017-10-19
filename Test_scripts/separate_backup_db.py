import pymssql
import os

"""
8088数据库分离备份
"""


class Separate_Backup_DB:
    """
    该模块用于测试完后的数据库清理
    """

    def __init__(self, dbname, host, username, password):
        """
        :param dbname: 数据库名字
        :param host: 主机地址
        :param username: 用户名
        :param password: 密码
        """
        self.dbname = dbname
        self.host = host
        self.username = username
        self.password = password

    def copy_database(self):
        """
        数据库的复制,清理,还原
        :return: None
        """
        conn = pymssql.connect(host=self.host, user=self.username, password=self.password, database=self.dbname)
        cur = conn.cursor()
        print("Connect database successfully")
        print("关闭所有链接")
        sql1 = '''
        use master
        begin transaction
        DECLARE @sql NVARCHAR(500)
        DECLARE @spid NVARCHAR(20)

        DECLARE #tb CURSOR FOR
        SELECT spid=CAST(spid AS VARCHAR(20)) FROM master..sysprocesses WHERE dbid=DB_ID('InroadTest')
        OPEN #tb
        FETCH NEXT FROM #tb INTO @spid
        WHILE @@fetch_status = 0 
            BEGIN
                EXEC('kill '+@spid)
                FETCH NEXT FROM #tb INTO @spid
            END
        CLOSE #tb
        DEALLOCATE #tb
        commit transaction
        commit transaction
        '''
        cur.execute(sql1)
        print("done")
        print("分离数据库")
        cur.callproc('sp_detach_db', ("InroadTest",))
        print("done")
        print("copy 数据库")
        # os.system("net use * /del /y")
        os.system(r"net use \\192.168.31.99\ipc$ Esl91n /user:Administrator")
        os.system(r"xcopy  \\192.168.31.99\d$\DB\InroadTest.mdf   \\192.168.31.99\e$\TestDb\InroadTestBak  /s/e/y/r/q")
        os.system(
            r"xcopy  \\192.168.31.99\d$\DB\InroadTest_1.ldf   \\192.168.31.99\e$\TestDb\InroadTestBak  /s/e/y/r/q")
        os.system("net use * /del /y")
        print("done")
        sql2 = '''
        begin transaction
        commit transaction
        '''
        cur.execute(sql2)
        cur.callproc('sp_attach_db', (
            'InroadTest', 'E:\TestDb\InroadTestBak\InroadTest.mdf', 'E:\TestDb\InroadTestBak\InroadTest_1.ldf',))
        print("分离备份完成")
        cur.close()
        conn.close()

        # if __name__ == "__main__":
        # help("separate_backup_db")
        # param = yaml.load(open('config/db_config.yaml'))
        # print(param['host'])
        # Separate_Backup_DB(param['dbname'], param['host'], param['user'], param['password']).copy_database()

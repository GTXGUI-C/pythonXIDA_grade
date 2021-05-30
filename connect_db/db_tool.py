import pandas as pd
import re
import pymysql


class db_playhouse:
    def __init__(self, host=None, username=None, password=None, database=None, port=None):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.db = None

    def connect(self, host, username, password, database, port):
        print('尝试建立连接')
        try:
            self.host = host
            self.username = username
            self.password = password
            self.database = database
            self.port = port
            self.db = pymysql.connect(host=self.host, user=self.username, password=self.password, port=self.port)
        except Exception as e:
            print('建立连接失败，请排查异常:', e)

    # 这个函数有两个输入，一个是执行的sql语句。分为插入和获取两种模式，以get_data为开关。若get_data为true，返回值为包含结果的迭代器。
    def execute_sql(self, sql, get_data=False):
        if get_data:
            cursor = self.db.cursor(pymysql.cursors.SSCursor)
            cursor.execute(sql)

            # 创建一个生成器，该生成器没有长度限制，因此非常适合大数据的存储。在这个情况之下，cursor不能关闭。
            def cursor_iterator():
                data = cursor.fetchone()
                while data:
                    yield data
                    data = cursor.fetchone()
            return cursor_iterator()

        else:
            with self.db.cursor() as cursor:  # 使用with，运行完后自动关闭游标
                cursor.execute(sql)  # 创建游标执行
                self.db.commit()  # 使用connection 来进行提交

    # 停止与数据库的通信
    def disconnect(self):
        self.db.close()
        print('已和数据库断开连接')

    # 这个方法的目的是根据一个dataframe创建相应的数据库，方便存入信息。
    # 相应的参数有四个：
    # (1) dataframe
    # (2) 选择创建的表格所要存放的数据库
    # (3) 选择创建的表格的名字
    # (4) 表格的主键
    def get_sql_query_create_table(self, data, database_name, table_name, primary_key=None, foreign_key=None,
                                   charset='utf8'):
        sql = """use {}""".format(database_name)
        self.execute_sql(sql)
        sql = """create table if not exists {} (""".format(table_name)
        # 如果没有主键，设立一个自增加主键
        if not primary_key:
            sql += "id int primary key not null auto_increment,"
        # 逻辑如下：根据字段的类型，创建mysql表格的初始设定。
        for column in data.columns:
            if data[column].dtype == 'O':
                sql += "{} varchar(50),".format(re.sub(r'[-/]', '_', column))
            elif data[column].dtype == float:
                sql += "{} double(6,2),".format(re.sub(r'[-/]', '_', column))
            elif data[column].dtype == pd.Timestamp:
                sql += "{} date,".format(re.sub(r'[-/]', '_', column))
            elif data[column].dtype == 'int64':
                sql += "{} int,".format(re.sub(r'[-/]', '_', column))
        if primary_key:
            sql += ",primary key({}) )DEFAULT CHARSET={};".format(primary_key, charset)
        # 这里后面可以添加一个外键的选项
        sql = sql[:-1] + ")DEFAULT CHARSET={};".format(charset)
        print("形成的sql语句为:")
        print(sql)
        return sql

    def insert_data_into_database(self, data, database_name, table_name):
        sql = """use {}""".format(database_name)
        self.execute_sql(sql)
        column_names = re.sub(r'[-/]', '_', ','.join(data.columns))
        for i in range(len(data)):
            str_value_list = []
            for value in data.iloc[i]:
                if type(value) == str:
                    str_value_list.append('\'' + str(value).strip() + '\'')
                else:
                    str_value_list.append(str(value).strip())
            values = ','.join(str_value_list)
            sql = """insert into {} ({}) values({})""".format(table_name, column_names, values)
            # Bug在于sql语句的插入字符串values需要加引号
            # print(sql)
            self.execute_sql(sql)

        print('插入数据完成')

# 加一个名字 孔泽亚 ---> 研究声--> wwt

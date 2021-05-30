# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from connect_db import db_tool
from make_table import make_table
import pandas as pd

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    database = db_tool.db_playhouse()  # make an instance for the db_playhouse class
    database.connect(host='117.78.18.51', username='root', password='123456', database='XIDA', port=3306)
    print(database.db)  # see if the database has been correctly connected

    data = pd.read_csv(r'D:\Files\mydata.csv')
    data = data.drop(data.columns[0], axis=1)

    # 执行建立数据库和插入数据的操作，这里创建了一个新的表，数据来自于data。存放在XIDA数据库下，然后表名字为test
    # sql = database.get_sql_query_create_table(data, 'XIDA', 'test')
    # database.execute_sql(sql)

    # 往数据表里插入数据
    # database.insert_data_into_database(data, 'XIDA', 'test')

    # 尝试获取数据，这里必须要声明用什么数据库
    sql = """use XIDA"""
    database.execute_sql(sql)
    sql = """select * from test limit 10;"""
    dt_iterator = database.execute_sql(sql, get_data=True)
    print(dt_iterator)
    for i in dt_iterator:
        print(i)
    database.disconnect()

    # tool = make_table.make_table()
    # path_list=[r'D:\Files\西南大学2021数统实习实训\bachelor.xlsx',r'D:\Files\西南大学2021数统实习实训\postgraduate.xlsx']
    # name_check_list=tool.get_name_check_list(path_list=path_list)
    # for name in name_check_list:
    #     print(name)
    # data = tool.create_group_collection(name_check_list)
    # data.to_excel(r'D:\Files\XIDA.xlsx')

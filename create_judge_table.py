# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from connect_db import db_tool
from make_table import make_table
import pandas as pd

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    database = db_tool.db_playhouse() # make an instance for the db_playhouse class
    database.connect(host='117.78.18.51', username='root', password='123456', database='XIDA', port=3306)
    print(database.db)  # see if the database has been correctly connected

    data = pd.read_csv(r'D:\Files\mydata.csv')
    data = data.drop(data.columns[0], axis=1)
    print(type(data['age']))

    # 执行建立数据库和插入数据的操作
    sql = database.get_sql_query_create_table(data, 'XIDA', 'test')
    database.execute_sql(sql)
    # sql = """insert into wuliga (workclass) values ('man');"""
    # database.execute_sql(sql)

    database.insert_data_into_database(data, 'XIDA', 'test')

    database.disconnect()

    # tool = make_table.make_table()
    # path_list=[r'D:\Files\西南大学2021数统实习实训\bachelor.xlsx',r'D:\Files\西南大学2021数统实习实训\postgraduate.xlsx']
    # name_check_list=tool.get_name_check_list(path_list=path_list)
    # for name in name_check_list:
    #     print(name)
    # data = tool.create_group_collection(name_check_list)
    # data.to_excel(r'D:\Files\XIDA.xlsx')
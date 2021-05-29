from pymongo import MongoClient
from connect_db import db_tool
import pymysql

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client = MongoClient()
    # show items in MongoDBclient
    # for i in client.list_database_names():
    #     print(i)

    # -------------------------------
    # database = db_tool.db_playhouse()
    # database.connect(host='117.78.18.51',username='root',password='123456',database='XIDA',port=3306)
    # print(database.db)
    # sql="""insert into Student (ID) values ('005')"""
    # database.disconnect()
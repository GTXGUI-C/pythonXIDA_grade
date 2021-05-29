import pandas as pd
import re
class make_table:
    def __init__(self):
        pass

    def create_group_collection(self,name_check_list):
        print('请输入数据')
        info=input('请输入小组信息，若需要结束输入，请输入q')
        group_info_list=[]
        while info!='q':
            group_info_list.append(self.process_group_name(info,name_check_list))
            info = input('请输入小组信息，若需要结束输入，请输入q')
        columns = ['group_name'] + ['leader'] + ['成员{}'.format(i) for i in range(1,15)]
        data = pd.DataFrame(group_info_list,columns=columns)
        return data

    def get_name_check_list(self,path_list):
        # 有的文件不一定是从第一行开始，我们可以自由选择从哪里输入
        def read_from_n():
            n = int(input('从第几行开始读取'))
            return n
        # 建立空列表存放名字
        name_check_list = []
        # 数据读取
        for path in path_list:
            while True:
                file_type = input('请输入文件的类型')
                if file_type == 'csv':
                    n = read_from_n()
                    temp = pd.read_csv(path, header=n)
                    break
                elif file_type == 'xlsx':
                    n = read_from_n()
                    temp_dt = pd.ExcelFile(path)
                    sheet_name = temp_dt.sheet_names
                    first_sheet = pd.read_excel(path, header=n, sheet_name=sheet_name[0])
                    for i in sheet_name[1:]:
                        temp = pd.read_excel(path, header=n, sheet_name=i)
                        first_sheet = pd.concat((first_sheet, temp), axis=0, ignore_index=True)
                    temp = first_sheet
                    break
                elif file_type == 'q':
                    break
                else:
                    print('类型错误，请重新输入')

            # 完成读取后，把特定字段加入到我们的表格里
            while True:
                try:
                    column = input('请输入选择的字段')
                    name_check_list += list(temp[column])
                    break
                except:
                    continue_or_not = bool(input("出现问题，是否继续? y/n"))
                    if continue_or_not == 'y':
                        continue
                    else:
                        print('结束')
                        break

        # name_list里可能有重复项
        def remove_nan_in_namelist(name_list):
            return list(pd.Series(name_list).dropna())
        # 全部完成后返回我们要的name_list
        return remove_nan_in_namelist(name_check_list)

    def process_group_name(self,input_str,name_check_list):
        # 把输入的字符串变成名字列表--->自动对比添加队名---->去重
        def cleanser(input_str):
            temp = re.sub(r'_', ' ', input_str).split()
            return remove_duplicate(temp)
        #  去重函数
        def remove_duplicate(data):
            res = []
            for i in range(len(data)):
                if data[i] not in res:
                    res.append(data[i])
            return res
        # 添加填充函数
        def add_padding(data):
            diff = 16-len(data)
            data+=['无']*diff
            return data

        #(1)
        group_data = cleanser(input_str)
        #(2)
        if group_data[0] in name_check_list:
            group_data=['无名']+group_data
        group_data=remove_duplicate(group_data)
        #(3)
        group_data=add_padding(group_data)
        return group_data






import numpy as np
import pandas as pd
import time
# https://blog.csdn.net/qq_31112205/article/details/86608136
# https://www.jb51.net/article/164740.htm
def save_csv_or_excel(arr_or_dic,ftype='xlsx',dir=None,fname=None,list_columns_names = [],index=False,append_time=False):
    '''
    一键将arr或dict数据保存为csv或者xls，xlsx文件
    :param arr_or_dic: arr或者 字典数组类型变量
    :param ftype: csv/xls/xlsx
    :param exc_filename: 不含文件后缀的文件名称
    :param list_columns_names: arr对应的列名称list
    :return:
    '''
    if fname == None:
        fname = "0_saved_csv_or_excel"
    if isinstance(fname,list):
        if append_time==True:
            fname.append(time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time())))
        fname=list(map(str, fname))
        fname="_".join(fname)
        if dir != None:
            fname=f"{dir}/{fname}"
    arr_df = pd.DataFrame(arr_or_dic)

    # 如果存在列标题，那么就设定列标题
    if list_columns_names:
        arr_df.columns = list_columns_names

    if ftype=='csv':
        arr_df.to_csv(fname+"."+ftype, index=index,sep='\t')
        # arr_df.to_csv(filename+"."+ftype, float_format='%.8f',index=index)
    else:
        writer = pd.ExcelWriter(fname+"."+ftype)
        arr_df.to_excel(writer, 'Sheet1',index=index) # index=None表示不需要列索引
        # arr_df.to_excel(writer, 'Sheet1', float_format='%.8f',index=index) # index=None表示不需要列索引
        writer.save()
    print(f'文件保存成功：{fname}.{ftype}')

def testArr():
    '''
    测试数组的保存
    :return:
    '''
    a1 = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45]
    a2 = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

    arr = []
    arr.append(a1)
    arr.append(a2)
    arr.append(a1)
    arr.append(a2)

    save_csv_or_excel(arr,ftype='xls')
    save_csv_or_excel(arr,list_columns_names=['1','22','33','44','55','66','7','88','9','10'])

def testDict1():
    # https://www.jb51.net/article/164740.htm
    '''从python创建DataFrame的“默认”方式是使用字典列表。在这种情况下，每个字典键用于列标题。'''
    sales = [{'account': 'Jones LLC', 'Jan': 150, 'Feb': 200, 'Mar': 140},
             {'account': 'Alpha Co', 'Jan': 200, 'Feb': 210, 'Mar': 215},
             {'account': 'Blue Inc', 'Jan': 50, 'Feb': 90, 'Mar': 95}]

    sales1 = {'account': ['Jones LLC', 'Alpha Co', 'Blue Inc'],
             'B': [200, 210, 90],
             'A': [150, 200, 50],
             'C': [140, 215, 95]}
    # df = pd.DataFrame(sales)
    # print(df)
    save_csv_or_excel(sales1,ftype='csv')
    save_csv_or_excel(sales1,ftype='xls')

if __name__ == '__main__':
    testArr()
    # testDict1()
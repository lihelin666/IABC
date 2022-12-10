import xlwt
import datetime

# 输出数据到Excel表，输入数据为字典
# res_dict={'a':arr,...}
# def outputDataByDict(res_dict):
#     for i in len(res_dict[0])
#     for key in res_dict:
#         for i in range(res.shape[0]):
#             dicti={}
#             dicti['设定值']=settedparams[i]
#             dicti['求解值']=res[i]
#             dicti['误差值']=error[i]
#             dicti['误差比率']=error_ratio[i]
#             res_arr.append(dicti)

# ↓ 输出数据到excel表，可用于excel和origin绘图
# res=[{}{}]

def outputData(res,file_name,time=False,res1={},res2={},num_blank_col=0):
    '''
    :param res:字典列表类型
    :param file_name:
    :param res1:
    :param num_blank_col:表头下空白num_blank_col行再写入数据
    :return:
    '''
    res0=res[0]
    col_names=[] # 列名称
    for key in res0:
        col_names.append(key)

    import xlwt  # 导入模块
    workbook = xlwt.Workbook(encoding='utf-8')  # 创建workbook 对象
    for index,res in enumerate([res,res1,res2]):
        worksheet = workbook.add_sheet(f'sheet{index}')  # 创建工作表sheet
        # ↓ 写列标题
        for index,val in enumerate(col_names):
            worksheet.write(0, index, val)
            if '=' in val:
                worksheet.write(1, index, val.split('=')[-1])
        # ↓ 逐行写数据
        for index_row,r in enumerate(res):
            for index_col, col_name in enumerate(col_names):
                worksheet.write(index_row+1+num_blank_col, index_col, r[col_name])
    # 存储第二个结果到sheet2
    # if res1:
    #     worksheet = workbook.add_sheet('参数')  # 创建工作表sheet
    #     ik=0
    #     for key in res1:
    #         worksheet.write(ik,0,key)
    #         worksheet.write(ik,1,res1[key])
    #         ik=ik+1

    if time:
        full_path=file_name+str(datetime.datetime.now()).replace(':','-')+'.xls' #构造完整的文件名
    else:
        full_path=file_name+'.xls' #构造完整的文件名
    workbook.save(full_path)  # 保存表为students.xls
    print(full_path,'保持完成')

if __name__ == '__main__':
    outputData(res=[],file_name='test',res1={})
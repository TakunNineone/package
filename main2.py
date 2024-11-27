import warnings,os,re
warnings.filterwarnings("ignore")
import pickle
import pandas as pd
# os.chdir(f'{os.getcwd()}//ulya')

import zipfile
list_comment={}
os.chdir('C:\\XBRL\\xw7 server 2\\data\\2')
#name='1021603631224_42pm30_20211031_1_REGNUMBER_1.zip'
name='2.zip'
i=0
with zipfile.ZipFile(name) as z:
    for filename in z.namelist():
        print(filename)
        with z.open(filename) as f:
            for line in f:
                print(line)
                txt,filename=line,filename
                i=i+1
                # if i==1000:
                #     break
                    m = re.findall ('<!--(.+?)-->', txt)
                    list_comment[filename]=m
                    with open('list2.pkl','wb') as f:
                        pickle.dump(list_comment, f)
#
# # list_comment={}
# # list_file=os.listdir()
# # for path in list_file:
# #     if 'xml' in path:
# #         with open(path,'r',encoding='utf-8') as f:
# #             txt=f.read()
# #         m = re.findall ('<!--(.+?)-->', txt)
# #         list_comment[path]=m
# # with open('list2.pkl','wb') as f:
# #     pickle.dump(list_comment, f)
#
# list_for_df=[]
# columns=['name','vendor']
#
#
# with open('list2.pkl', 'rb') as f:
#     list_comment = pickle.load(f)
#
# for xx in list_comment.keys():
#     str_vendor='|'.join(str(yy) for yy in list_comment[xx])
#     list_for_df.append([xx,str_vendor])
# df=pd.DataFrame(data=list_for_df,columns=columns)
#
# writer = pd.ExcelWriter('result2.xlsx', engine='xlsxwriter')
# df.to_excel(writer, sheet_name='vendor')
# writer._save()
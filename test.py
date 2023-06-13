import zipfile,os,re,datetime,operator,pandas as pd
name='1.zip'
with zipfile.ZipFile(name) as z:
    for filename in z.namelist():
        if not os.path.isdir(filename):
            with z.open(filename) as f:
                final_dict=[]
                doprint=False
                i=0
                ii=0
                temp_list=[]
                temp_line={}
                for xx in f:
                    if doprint==True and i!=0:
                        ii += 1
                        i -= 1
                        if i==0:
                            assertion_id=xx.decode('utf-8').strip()
                            temp_list.append([assertion_id,time])
                    else:
                        i=0
                        doprint==False
                        temp_line = {}
                    if re.findall('ru.softailor.xwand.service.handlers.FormulaLinkResultHandlerImpl -(.+?)false\r\n',xx.decode("utf-8")) or \
                            re.findall('ru.softailor.xwand.service.handlers.FormulaLinkResultHandlerImpl -(.+?)true\r\n',xx.decode("utf-8")):
                        time=xx.decode('utf-8').split(' ')[0]+' '+xx.decode('utf-8').split(' ')[1]
                        doprint=True
                        i=3
assertions_group=[xx[0] for xx in temp_list]
assertions_group=list(set(assertions_group))
#assertions_group=['id=valueAssertion_sr0420154_2_34_2248']
list_ff={}
final_list=[]
for xx in assertions_group:
    list_ff[xx]=[]
    for yy in temp_list:
        if yy[0]==xx:
            list_ff[xx].append(datetime.datetime.strptime(yy[1], '%Y-%m-%d %H:%M:%S:%f'))
sum=datetime.timedelta()
for xx in list_ff.keys():
    delta=max(list_ff[xx])-min(list_ff[xx])
    sum=sum+delta
    mindate = min(list_ff[xx]).strftime('%Y-%m-%d %H:%M:%S.%f')
    maxdate = max(list_ff[xx]).strftime('%Y-%m-%d %H:%M:%S.%f')
    mindate_s = (min(list_ff[xx])-datetime.datetime(1970,1,1)).total_seconds()
    maxdate_s = (max(list_ff[xx])-datetime.datetime(1970,1,1)).total_seconds()
    sort=int(min(list_ff[xx]).strftime('%Y%m%d%H%M%S%f'))
    # if delta>datetime.timedelta(seconds=0):
    final_list.append({'assertion':xx,'sort':sort,'min':mindate,'max':maxdate,'delta':delta.total_seconds(),'mindate_s':mindate_s,'maxdate_s':maxdate_s})

final_list=sorted(final_list, key=operator.itemgetter('sort'))
df = pd.DataFrame.from_dict(final_list)
df.to_excel('log_all.xlsx')
# with open('log_all.txt','a') as f:
#     for xx in final_list:
#         f.write(f"{xx.get('assertion')};{xx.get('delta')};{xx.get('min')}';'{xx.get('max')}\n")



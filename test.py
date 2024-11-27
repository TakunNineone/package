import zipfile,os,re,datetime,operator,pandas as pd
name='2.zip'
with zipfile.ZipFile(name) as z:
    for filename in z.namelist():
        if not os.path.isdir(filename):
            with z.open(filename) as f:
                final_dict=[]
                doprint=''
                i=0
                ii=0
                k_true=0
                k_false=0
                temp_list=[]
                temp_line={}
                for xx in f:
                    if doprint in ('false','true') and i!=0:
                        ii += 1
                        i -= 1
                        if i==0:
                            assertion_id=xx.decode('utf-8').strip()
                            temp_list.append([assertion_id,time,k_true,k_false])
                            k_true=0
                            k_false=0
                    else:
                        i=0
                        doprint=''
                        temp_line = {}
                    if re.findall('ru.softailor.xwand.service.handlers.FormulaLinkResultHandlerImpl -(.+?)false\r\n',xx.decode("utf-8")) or \
                            re.findall('ru.softailor.xwand.service.handlers.FormulaLinkResultHandlerImpl -(.+?)true\r\n',xx.decode("utf-8")):
                        if re.findall('ru.softailor.xwand.service.handlers.FormulaLinkResultHandlerImpl -(.+?)false\r\n',xx.decode("utf-8")):
                            k_false = 1
                            doprint='false'
                        elif re.findall('ru.softailor.xwand.service.handlers.FormulaLinkResultHandlerImpl -(.+?)true\r\n',xx.decode("utf-8")):
                            k_true = 1
                            doprint = 'true'
                        time=xx.decode('utf-8').split(' ')[0]+' '+xx.decode('utf-8').split(' ')[1]
                        if  '2024-11-26 14:00' in time:
                            None
                        i=3
assertions_group=[xx[0] for xx in temp_list]
assertions_group=list(set(assertions_group))
#assertions_group=['id=valueAssertion_sr0420154_2_34_2248']
list_ff={}
final_list=[]
cnt_srab={}
for xx in assertions_group:
    cnt_srab[xx]={'cnt_false':0,'cnt_true':0}
    list_ff[xx]=[]
    for yy in temp_list:
        if yy[0]==xx:
            list_ff[xx].append(datetime.datetime.strptime(yy[1], '%Y-%m-%d %H:%M:%S:%f'))
            cnt_srab[xx]['cnt_true']=cnt_srab[xx]['cnt_true'] + yy[2]
            cnt_srab[xx]['cnt_false'] = cnt_srab[xx]['cnt_false'] + yy[3]

# for xx in cnt_srab.keys():
#     for yy in cnt_srab[xx].keys():
#         print(xx,yy,cnt_srab[xx][yy])


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
    final_list.append({'assertion':xx,'sort':sort,'min':mindate,'max':maxdate,'delta':delta.total_seconds(),'mindate_s':mindate_s,'maxdate_s':maxdate_s,'cnt_true':cnt_srab[xx].get('cnt_true'),'cnt_false':cnt_srab[xx].get('cnt_false')})

final_list=sorted(final_list, key=operator.itemgetter('sort'))
df = pd.DataFrame.from_dict(final_list)
df.to_excel('bki_disabled_crosscheck.xlsx')
# with open('log_all.txt','a') as f:
#     for xx in final_list:
#         f.write(f"{xx.get('assertion')};{xx.get('delta')};{xx.get('min')}';'{xx.get('max')}\n")



import zipfile,os,re,datetime,operator,pandas as pd
from itertools import chain
from collections import Counter

name='1.zip'
times_array= {}
va_array= {}
pool_array={}
va_dict={}
va_dict_srab={}
srab_dic={}
va_dict_res={}
pool_dict={}
with zipfile.ZipFile(name) as z:
    for filename in z.namelist():
        if not os.path.isdir(filename):
            with z.open(filename) as f:
                pattern_time = r"\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}:\d{3}\b"
                pattern_va = r"\s+id=(.+)$"
                pattern_thread=r'\[pool-\d+-thread-\d+\]'
                for idx,xx in enumerate(f):
                    print("", end=f"\rprocess: {idx}")
                    if len(xx)>250:
                        continue
                    else:
                        line = xx.decode('utf-8')
                        if 'false' in line:
                            srab_dic[idx]='false'
                        if 'true' in line:
                            srab_dic[idx]='true'
                        # if i > 3512 and i < 3523:
                        matches_time = re.findall(pattern_time, line)
                        matches_va = re.search(pattern_va, line)
                        match_thread = re.findall(pattern_thread, line)
                        None
                        if matches_time!=[]:
                            times_array[idx]=matches_time[0]
                        if matches_va != None:
                            va_array[idx]=matches_va.group(1).strip()
                        if match_thread !=[]:
                            pool_array[idx]=match_thread[0]



unique_va = list(set([x for x in va_array.values()]))
for xx in unique_va:
    va_dict[xx]=[]
    pool_dict[xx]=''
None
for xx in unique_va:
    va_dict_srab[xx]=[]

tt=1
for id,row in va_array.items():
    print("", end=f"\rprocess_srab: {round((tt) / len(va_array) * 100, 2)}%")
    srab=''
    ii = 0
    while srab=='':
        try:
            srab=srab_dic[id-ii]
            va_dict_srab[row].append(srab)
        except:
            ii += 1
    tt+=1
None

tt=1
for id,row in va_array.items():
    print("", end=f"\rprocess_time: {round((tt) / len(va_array) * 100, 2)}%")
    time=''
    ii=0
    while time=='':
        try:
            time=times_array[id-ii]
            va_dict[row].append(datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S:%f'))
            pool_dict[row]=pool_array[id-ii]
            None
        except:
            ii+=1
    tt += 1

tt=1
for id,row in pool_array.items():
    print("", end=f"\rprocess_pool: {round((tt) / len(pool_array) * 100, 2)}%")
    pool=''
    ii=0
    while pool=='':
        try:
            pool=pool_array[id-ii]
            pool_dict[row]=pool
            None
        except:
            ii+=1
    tt+=1


for id,row in va_dict.items():
    cnt = len(va_dict[id])
    c = Counter(va_dict_srab[id])
    cnt_true=c['true']
    cnt_false=c['false']
    max_time=max(va_dict[id])
    min_time=min(va_dict[id])
    duration=max_time-min_time
    duration_in_s=duration.total_seconds()
    minutes = divmod(duration_in_s, 60)[0]
    va_dict_res[id]={'Время старта':min_time,'Время окончания':max_time,'Время работы контроля (сек.)':duration_in_s,'Количество срабатываний':cnt,'True':cnt_true,'False':cnt_false}
    None

data = []
for va_id, values in va_dict_res.items():
    row = {'va_id': va_id,'pool':pool_dict[va_id]}
    row.update(values)
    data.append(row)

df = pd.DataFrame(data)
df_sorted = df.sort_values(by=['pool', 'Время старта'], ascending=True)
df_sorted['Время расчета контроля (сек.)'] = (df_sorted['Время старта'] - df_sorted['Время окончания'].shift(1)).dt.total_seconds()
df_sorted['Время расчета контроля (сек.)'] = [xx if xx>0 else 0 for xx in df_sorted['Время расчета контроля (сек.)']]
df_sorted.to_excel('1__.xlsx',index=False)

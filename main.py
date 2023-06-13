import xmltodict as xmltodict
from bs4 import BeautifulSoup
import warnings,gc
import xmltodict, json,xml.sax
warnings.filterwarnings("ignore")
from xml.etree import ElementTree as ET


def readjson(path):
    with open(path, encoding='utf-8') as f:
        json_list = json.load(f)
    return json_list

path='XBRL_1147799010314_ep_nso_npf_y_90d_reestr_0420258_20221231.xml'
path2='report_0409725_output.xml'
# with open(path,encoding='utf-8') as fd:
#     doc = xmltodict.parse(fd.read())
# dict=json.dumps(doc)
# with open("instance.json", "w") as json_file:
#     json_file.write(dict)
#     json_file.close()

dict_=readjson('instance.json')
contexts=dict_['xbrli:xbrl']['xbrli:context']
contexts_id=[]
varible_refs=[]
varible_refs_txt=[]
for xx in contexts:
    contexts_id.append(xx['@id'])

varible=dict_['xbrli:xbrl']

for xx in varible.keys():
    if '@' not in xx and 'link:schemaRef' not in xx and 'xbrli:context' not in xx and 'xbrli:unit' not in xx:
        for varcont in dict_['xbrli:xbrl'][xx]:
            if type(varcont)==dict:
                varible_refs.append(varcont.get('@contextRef'))
                #print(type(varcont), varcont)
            else:
                varible_refs.append(dict_['xbrli:xbrl'][xx].get('@contextRef'))
print('Всего показателей',len(varible_refs),'Уникальных контекстов в показателях',len(set(varible_refs)))
print('Всего контекстов',len(contexts_id),'Уникальных контекстов',len(set(contexts_id)))
res=list(set(varible_refs) - set(contexts_id))
del varible_refs,contexts_id,contexts,varible
gc.collect()
print('Показателей с неправильной ссылкой на контекст',len(res))

with open('log.txt','w') as f:
    for xx in res:
        f.write(xx+'\n')
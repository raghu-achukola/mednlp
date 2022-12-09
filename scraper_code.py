from bs4 import BeautifulSoup
import requests
import re
import time
import json

ROOT = 'https://www.icd10data.com/'
LEVEL0_ROOT = 'https://www.icd10data.com/ICD10CM/Codes'


def diag_code_split(codes:list)-> dict:
    return {definition.split()[0]:' '.join(definition.split()[1:] )for definition in codes}

# GET DATA 
def def_to_dict(l:list)-> dict:
    return {definition.split()[0]:' '.join(definition.split()[1:] )for definition in l}
def get_l0_data(soupy)->dict:
    return {x.find('a').text:' '.join(x.text.strip().split()[1:])for x in soupy.find_all('li') if x.find_all('div')}
def get_l1_or_l2_data(single_soup) -> tuple: 
    return def_to_dict([y.text.strip() for x in single_soup.find_all('ul',{'class':'i51'}) for y in x.find_all('li') if y.find('div',{'class':'tip images-note'})])
def get_l3plus_data(code_hierarchy_soup):
    lies =  [x.text for x in code_hierarchy_soup.find('li').find_all('span')]
    return diag_code_split(lies)
    
class ICDCodeRange:
    def __init__(self,name:str,level:str,link:str, definition='', subcodes = {})-> None:
        self.level, self.name, self.link,self.definition,self.subcodes = level,name,link,definition, subcodes
    def fill_subcodes(self):
        soup = BeautifulSoup(requests.get(self.link).text,'lxml')
        if self.level in (0,1):
            fn = ICDCodeRange.get_l1_or_l2_data
            ln = lambda x,y: '{}/{}'.format(x,y)
        else:
            fn = lambda x: {}
            ln = lambda x,y:'{}/{}'.format(x,y)
        for k,v in fn(soup).items():
            self.subcodes[k] = ICDCodeRange(name = k,level = self.level+1,link = ln(self.link,k), definition = v,subcodes = {})
    def crawl(self, rec_depth = 1, sleep_interval = 2, p = False):
        if  type(rec_depth) != int or rec_depth <= 0 : 
            return 
        else:
            time.sleep(sleep_interval)
            if not self.subcodes:
                if p:
                    print('Filling subcodes for L{}:{}'.format(self.level,self.name))
                self.fill_subcodes()
            for k,v in self.subcodes.items():
                print('Crawling for L{}:{}'.format(v.level,k))
                time.sleep(sleep_interval)
                self.subcodes[k].crawl(rec_depth = rec_depth-1,sleep_interval=sleep_interval)


if __name__ == '__main__':
    # Start at LEVEL 0 
    response = requests.get(LEVEL0_ROOT)
    assert response.status_code == 200
    LEVEL0 = get_l0_data(BeautifulSoup(response.text,'lxml'))
    print(LEVEL0)
    with open('transformed_data/icd10_l0.json','w') as f:
        f.write(json.dumps(LEVEL0, indent = 2))

    LEVEL1 = {}    
    for k,v in LEVEL0.items():
        print('{}-{}'.format(k,v))
        CODE1_ROOT = '{}/{}'.format(LEVEL0_ROOT,k)
        icr = ICDCodeRange(k,0,CODE1_ROOT,v,subcodes={})
        print(icr.__dict__)
        time.sleep(4)
        icr.fill_subcodes()
        LEVEL1 |= {'{}/{}'.format(CODE1_ROOT,k):v.definition for k,v in icr.subcodes.items()}
    print(LEVEL1)
    with open('transformed_data/icd10_l1.json','w') as f:
        f.write(json.dumps(LEVEL1,indent = 2))
    LEVEL2 = {}
    for k,v in LEVEL1.items():
        print('{} - {}'.format(k,v))
        icr = ICDCodeRange(k.split('/')[-1],1,k,v,subcodes={})
        time.sleep(4)
        icr.fill_subcodes()
        LEVEL2 |= {v.link:v.definition for _, v in icr.subcodes.items()}
    with open('transformed_data/icd10_l2.json','w') as f:
        f.write(json.dumps(LEVEL2,indent=2))




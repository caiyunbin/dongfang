# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 16:38:27 2019

@author: Caiyunbin
"""
import time,random
import json
from multiprocessing import Pool
import requests
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
import csv

def get_one_page(url):
    try:
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
        response=requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    doc=pq(html)
    items=doc('.clearfix .subject-list .subject-item').items()
    for item in items:
        yield{'name':item('.info h2 a').attr('title'),
              'author':item('.pub').text().strip(),
              'star':item('.clearfix .rating_nums').text().strip(),
              'intro':item.find('.info p').text().strip()
              }
"""    
def save_to_json(dics):
    with open('douban.txt','a',encoding='GB18030') as f:
        f.write(json.dumps(dics,ensure_ascii=False) + '\n')
"""
def save_to_csv(dics):
    with open('douban_his.csv','a',encoding='GB18030') as csvfile:
        fieldnames = ['name','author','star','intro']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writerow(dics)

def main(start):
   url = 'https://book.douban.com/tag/历史?start='+str(start)+'&type=T'
   html = get_one_page(url)
   items = parse_one_page(html)
   for item in items:
       print(item)
       save_to_csv(item)
       
if __name__ == '__main__':
    pool=Pool()
    result= pool.map(main, [i*20 for i in range(50)])
    time.sleep(random.randint(0,2))

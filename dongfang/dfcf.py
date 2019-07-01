# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 14:41:08 2019

@author: Caiyunbin
"""
import csv
import requests
from urllib.parse import urlencode
import re
import pymysql
import json
from multiprocessing import Pool

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSLQ_PASSWORD = 'caiyunbin3344'
MYSQL_PORT = '3306'


def get_one_page(page):
    print('正在读取第:%d页' % (page))
    try:
        params = {
            'sty': 'analy',
            'SortType': 'NDATE,SCODE,RANK',
            'SortRule': '1',
            'PageIndex': page,
            'PageSize': '50',
            'type': 'NSHDDETAIL'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }
        url = 'http://data.eastmoney.com/DataCenter_V3/gdfx/data.ashx?' + urlencode(params)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
            return None
    except requests.exceptions:
        return None


def parse_one_page(html):
    pattern = re.compile(
        '.*?"SHAREHDNAME":"(.*?)","SHAREHDTYPE":"(.*?)","SHARESTYPE":"(.*?)","RANK":(.*?),"SCODE":"(.*?)","SNAME":"(.*?)","RDATE":"(.*?)","SHAREHDNUM":(.*?),"LTAG":(.*?),"ZB".*?"BZ":"(.*?)","BDBL":(.*?),.*?"SHAREHDRATIO":(.*?),"BDSUM".*?}',
        re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'p_name': item[0],
            'p_type': item[1],
            'p_class': item[2],
            'p_rank': item[3],
            's_code': item[4],
            'invest_c': item[5],
            're_date': item[6],
            'quantity': item[7],
            'liutong': item[8],
            'biandong': item[9],
            'changgerio': item[10],
            'sharerio': item[11]
        }


def save_to_csv(csvf):
    with open('E:\崔庆才爬虫课程\learning scripts\dongfang.csv', 'a', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['股东名称', '股东类型', '股票类别', '股东排序', '股票代码', '投资公司', '报告日期', '持有数量', '流通市值', '持股变动', '变动比例', '股票占比']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(csvf)


def save_to_json(txt):
    with open('E:\崔庆才爬虫课程\learning scripts\dongfang.txt', 'a', encoding='GB18030') as f:
        f.write(json.dumps(txt, ensure_ascii=False) + '\n')


class Mysql():
    def __init__(self, host=MYSQL_HOST, username=MYSQL_USER, password=MYSLQ_PASSWORD, port=MYSQL_PORT,
                 database='dongfang'):
        try:
            self.db = pymysql.connect(host, username, password, database, charset='gb18030', port=port)
            self.cursor = self.db.cursor()
        except pymysql.MySQLError as e:
            print(e.args)

    def insert(self, table, data):
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql_query = 'INSERT INTO %s (%s) VALUES (%s)' % (table, keys, values)
        try:
            self.cursor.execute(sql_query, tuple(data.values()))
            self.db.commit()
        except pymysql.MySQLError as e:
            print(e.args)
            self.db.rollback()


##关键实现了数据库的存储方法
def main(page):
    mysql = Mysql()
    html = get_one_page(page)
    con = parse_one_page(html)
    print(type(con))
    for item in con:
        mysql.insert('tablename',item)


if __name__ == '__main__':
    pool = Pool()
    result = pool.map(main, [page for page in range(1, 718)])
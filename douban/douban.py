# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from pyquery import PyQuery as pq

response=requests.get('https://book.douban.com/')
print(response.status_code)

content=response.text

doc=pq(content)

cover = doc('.popular-books .list-col li .author').items()
for item in cover:
    print(item.text())

all = doc('.popular-books .list-col li').items()

for item in all:
    rate = item.find('p .average-rating').text()
    author = item.find('p .author').text()
    classfy = item.find('p .book-list-classification').text()
    reviews = item.find('p .reviews').text().strip()
    
    
    
    
print(type(item[0]))

print(rate)
print(author)
print(classfy)
print(reviews)

rate = all.find('.average-rating').text()
author = all('.author').text()
classfy = all('.book-list-classification').text()
reviews = all('.reviews').text().strip()

print(cover.attr("title"))










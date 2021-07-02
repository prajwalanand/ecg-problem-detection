# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 22:48:15 2018

@author: prajw
"""

import requests
from bs4 import BeautifulSoup as bs
import urllib.request as urllib2


_URL = 'https://physionet.org/physiobank/database/chfdb/'

# functional
r = requests.get(_URL)
soup = bs(r.text, 'lxml')
urls = []
names = []
for i, link in enumerate(soup.findAll('a')):
    _FULLURL = link.get('href')
    print(_FULLURL)
    if _FULLURL is None:
        continue
    if _FULLURL.endswith('.hea') or _FULLURL.endswith('.dat') or _FULLURL.endswith('.hea-'):
        print(_FULLURL)
        urls.append(_URL+_FULLURL)
        names.append(soup.select('a')[i].attrs['href'])

names_urls = zip(names, urls)

for name, url in names_urls:
    print(url)
    rq = urllib2.Request(url)
    res = urllib2.urlopen(rq)
    pdf = open("Data/chfdb/" + name, 'wb')
    pdf.write(res.read())
    pdf.close()
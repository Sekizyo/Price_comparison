import concurrent.futures
import time
import random
from random import randint

import re
import csv
import sys
import operator

from module.sql_func import add_query_stats, save_query
from module.models import Item, Prices, Query, Update, Spec
from module.pretty import time_start, time_end
from module.check import x_kom, morele, media_expert

def query(url, shop_id):
    if shop_id == 1:
        x_kom("", "name_low", url)

    if shop_id == 2:
        morele("", "name_low", url)
        
    if shop_id == 3:
        media_expert("", "name_low", url)

def query_run(choice):
    
    urls = [] 
    shop_id = []
    word_list = []
    passes = 6
    for _ in range(4):
        word = random.choice('abcdefghijklmnopqrstuvwxyz')+random.choice('abcdefghijklmnopqrstuvwxyz')
        word_list.append(word)

        nr = random.choice('1234567890')+random.choice('1234567890')
        word_list.append(nr)

    if choice == "all":
        for x in range(len(word_list)):
            for y in range(passes):     
                url = "https://www.x-kom.pl/szukaj?page="+str(y)+"&sort_by=accuracy_desc&q="+str(word_list[x])
                urls.append(url)
                shop_id.append(1)

                url = "https://www.morele.net/wyszukiwarka/0/0/,,,,,,,,0,,,,/"+str(y)+"/?q="+str(word_list[x])
                urls.append(url)
                shop_id.append(2)

                url = "https://www.mediaexpert.pl/search?limit=30&page="+str(y)+"&query%5Bmenu_item%5D=&query%5Bquerystring%5D="+str(word_list[x])
                urls.append(url)
                shop_id.append(3)

    if choice == "x_kom":
        for x in range(len(word_list)):
            for y in range(passes):     
                url = "https://www.x-kom.pl/szukaj?page="+str(y)+"&sort_by=accuracy_desc&q="+str(word_list[x])
                urls.append(url)
                shop_id.append(1)

    if choice == "morele":
        for x in range(len(word_list)):
            for y in range(passes):     
                url = "https://www.morele.net/wyszukiwarka/0/0/,,,,,,,,0,,,,/"+str(y)+"/?q="+str(word_list[x])
                urls.append(url)
                shop_id.append(2)

    if choice == "media_expert":
        for x in range(len(word_list)):
            for y in range(passes):     
                url = "https://www.mediaexpert.pl/search?limit=30&page="+str(y)+"&query%5Bmenu_item%5D=&query%5Bquerystring%5D="+str(word_list[x])
                urls.append(url)
                shop_id.append(3)
                
    start = time.time()
    stats_start = len(Item.query.order_by(Item.id).all())
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(query, urls, shop_id)

    stats_end = len(Item.query.order_by(Item.id).all())
    
    updated = stats_end - stats_start
    end = time.time()
    times = end - start
    times = times

    add_query_stats(times, updated)

    
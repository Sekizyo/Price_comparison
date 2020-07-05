import re
import csv
import sys
import time
import datetime
import operator
import requests
import random
from random import randint


from webbot import Browser
from bs4 import BeautifulSoup
import concurrent.futures

from module import app, db
from module.models import Item, Prices, Query, Update, Spec
from flask_sqlalchemy import BaseQuery


now = datetime.datetime.now()
date_now = datetime.date.today()
now_date = now.strftime("%d-%m-%Y")
now_time = now.strftime("%H:%M:%S")

def time_start():
    start = time.time()
    return start

def time_end(start_time):
    end = time.time()
    times = end - start_time
    print(f" - {times} sec")
    

def format_price(price):
    price_formated = []
    price_list = list(price)
    flag = True

    for letter in price_list:
        if letter == ",":
            flag = False
        else:
            pass
        if flag == True:
            price_formated.append(letter)

    for x in range(len(price_formated)):
        if " " in price_formated:
            price_formated.remove(" ")

        if "," in price_formated:
            price_formated.remove(",")

        if "\n" in price_formated:
            price_formated.remove("\n")

        if "z" in price_formated:
            price_formated.remove("z")

        if "ł" in price_formated:
            price_formated.remove("ł")

        if "o" in price_formated:
            price_formated.remove("o")

        if "d" in price_formated:
            price_formated.remove("d")

        if " " in price_formated:
            price_formated.remove(" ")

        if "\xa0" in price_formated:
            price_formated.remove("\xa0")
        
    price0 = ''.join(price_formated)

    return price0
"""
def format_name(name):
    name_formated = []
    name_formated0 = []
    end = []
    name_list = list(name)
        
    for item in name_list:
        name_formated.append(item)

    for word in name_formated:
        l1 = list(word)
        for l in l1:
            if l == "\n" or l == "\t":
                pass
            else:
                name_formated0.append(l)
        end0 = "".join(name_formated0)
        name_formated0.clear()
        end.append(end0)
        
    return end
"""

def sort(name, price, link, sort0="price_low"):
    if sort0 == "name_low":
        name = [str(i) for i in name] 

        zipped = zip(name, price, link)
        zipped = sorted(zipped, reverse=False)
        name, price, link = zip(*zipped)
        
        return (list(name), list(price), list(link))

    if sort0 == "name_high":
        name = [str(i) for i in name] 

        zipped = zip(name, price, link)
        zipped = sorted(zipped, reverse=True)
        name, price, link = zip(*zipped)
        
        return (list(name), list(price), list(link))
    
    if sort0 == "price_low":
        sort_by0 = False
    if sort0 == "price_high":
        sort_by0 = True

    price = [int(i) for i in price]
    
    zipped = zip(price, name, link)
    zipped = sorted(zipped, reverse=sort_by0)
    price, name, link = zip(*zipped)
        
    return name, price, link

def spec_save(name, price, url, shop): #TODO
    spec_item = Spec_Item(name=name, url=url, shop_id=shop)
    spec_price = Spec_Prices(created=now_date, price=price)
    return

def check_spec(shop):
    price = Spec_Prices.query.filter_by(shop_id=shop).all()#TODO check if price changed
    pass

def save_single(id, price):
    price = format_price(price)
    
    item = Item.query.filter_by(id=id).first()
    old_price = Prices.query.filter_by(item_id=item.id).all()

    if len(old_price) == 0:
            item_price = Prices(author=item, created=now_date, price=price)
            db.session.add(item_price)
            db.session.commit()
            updated+=1
    else:
        if not int(price) == int(old_price[-1].price):
            item_price = Prices(author=item, created=now_date, price=price)
            db.session.add(item_price)
            db.session.commit()
            updated+=1

def save_query(name, price, link, shop_id):
    match = 0
    for x in range(len(name)):
        item0 = Item.query.filter_by(name=name[x]).first()
        if not item0:
            item = Item(name=name[x], url=link[x], shop_id=shop_id)
            db.session.add(item)
            db.session.commit()
        else:
            match+=1

        item = Item.query.filter_by(name=name[x]).first()
        old_price = Prices.query.filter_by(item_id=item.id).all()
        
        if len(old_price) == 0:
            new_price = Prices(author=item, created=now_date, price=price[x])
            db.session.add(new_price)
            
        else:
            if not int(price[x]) == int(old_price[-1].price):
                new_price = Prices(author=item, created=now_date, price=price[x])
                db.session.add(new_price)

        db.session.commit()
        query_stats2(match, len(name))

def update_prices():
    items = Item.query.order_by(Item.id).all()

    url_xkom = []
    id_xkom = []
    
    url_morele = [] 
    id_morele = [] 
    
    url_media = [] 
    id_media = [] 
    

    for item in items:
        if item.shop_id == 1:
            url_xkom.append(item.url)
            id_xkom.append(item.id)

        if item.shop_id == 2:
            url_morele.append(item.url)
            id_morele.append(item.id)

        if item.shop_id == 3:
            url_media.append(item.url)
            id_media.append(item.id)

    start = time.time()
    stats_start = len(Prices.query.order_by(Prices.id).all())

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(check_xkom, url_xkom, id_xkom)
        results = executor.map(check_morele, url_morele, id_morele)
        results = executor.map(check_media, url_media, id_media)
    
    stats_end = len(Prices.query.order_by(Prices.id).all())
    
    item_len = stats_end - stats_start
    end = time.time()
    times = end - start
    times = times

    update_stats(times, item_len)
    
def x_kom(objects, sort_by="price_low", url=False):
    main_page = "https://www.x-kom.pl/szukaj?q="
    link_page = "https://www.x-kom.pl"
    if " " in objects:
        output = []
        for letter in objects:
            if letter == " ":
                output.append("%20")
            else:
                output.append(letter)
        objects = ''.join(output) 
    if url == False:
        url = str(main_page+str(objects))
    else:
        url = str(url)
    
    page = requests.get(str(url))
    soup = BeautifulSoup(page.text, 'html.parser')
    name = []
    price = []
    link = [] 

    repo = soup.find(class_="sc-bwzfXH sc-162ysh3-0 jaUCAK sc-htpNat gSgMmi") #contener
    try:
        repo_list = repo.find_all(class_='sc-162ysh3-1 cVKkKd sc-bwzfXH dXCVXY') # item block
    except:
        repo_list = []
        price0 = "No in stock"

    for repo in repo_list:
        name1 = repo.find(class_='sc-1yu46qn-12 edAUTq sc-16zrtke-0 hovdBk').text.split('/')
        name0 = ''.join(name1)
            
        try:
            price1 = repo.find(class_='sc-6n68ef-1 eOCAwm').text.split('/')
            price0 = price1[0].strip()
        except:
            price0 = "No in stock"
            break

        link0 = repo.find('a')
        link0 = link0.get("href")
        link0 = link_page + link0

        price0 = format_price(price0)
        name.append(name0)
        price.append(price0)
        link.append(link0)

    if name:
        # name = format_name(name)
        name, price, link = sort(name, price, link, sort_by)
        save_query(name, price, link, 1)

        return(name, price, link)
    else:
        return("", "", "")

    # except:
        # return print("Xkom Item not found or error ")

def check_xkom(url, id):
    page = requests.get(str(url))
    soup = BeautifulSoup(page.text, 'html.parser')
    repo = soup.find(class_="page-wrapper") #contener
    price1 = repo.find(class_='u7xnnm-4 iVazGO').text.split('/')
    price0 = price1[0].strip()
    
    save_single(id, price0)
            
def morele(objects, sort_by="price_low", url=False):
    main_page = "https://www.morele.net/wyszukiwarka/0/0/,,,,,,,,,,,,/1/?q="
    link_page = "https://www.morele.net"
    if " " in objects:
        output = []
        for letter in objects:
            if letter == " ":
                output.append("+")
            else:
                output.append(letter)
        objects = ''.join(output) 
    if url == False:
        url = str(main_page+str(objects))
    else:
        url = str(url)    
    page = requests.get(str(url))

    soup = BeautifulSoup(page.text, 'html.parser')
    name = []
    price = []
    link = [] 

    repo = soup.find(class_="cat-list-products") #contener
    try:
        repo_list = repo.find_all(class_='cat-product card') # item block
    except:
        repo_list=[]

    for repo in repo_list:
        name1 = repo.find(class_='cat-product-name').text.split('/')
        name0 = name1[0].strip()
        try:
            price1 = repo.find(class_='price-new').text.split('/')
            price0 = price1[0].strip()
        except:
            price0 = "No in stock"

        link0 = repo.find('a')
        link0 = link0.get("href")
        link0 = link_page + link0

        price0 = format_price(price0)
        name.append(name0)
        price.append(price0)
        link.append(link0)

    if name:
        name, price, link = sort(name, price, link, sort_by)
        save_query(name, price, link, 2)
        return(name, price, link)
    else:
        return("", "", "")
     
def check_morele(url, id):
    page = requests.get(str(url))
    soup = BeautifulSoup(page.text, 'html.parser')
    
    repo = soup.find(class_="main-content") #contener
        
    price1 = repo.find(class_='price-new').text.split('/')
    price0 = price1[0].strip()
    
    save_single(id, price0)

def media_expert(objects, sort_by="price_low", url=False):
    main_page = "https://www.mediaexpert.pl/search?query[menu_item]=&query[querystring]="
    link_page = "https://www.mediaexpert.pl"
    if " " in objects:
        output = []
        for letter in objects:
            if letter == " ":
                output.append("%2520")
            else:
                output.append(letter)
    
        objects = ''.join(output) 
    if url == False:
        url = str(main_page+str(objects))
    else:
        url = str(url)
    page = requests.get(str(url))

    soup = BeautifulSoup(page.text, 'html.parser')
    name = []
    price = []
    link = [] 

    repo = soup.find(class_="c-layout v-product v-product_list is-classic") #contener
    try:
        repo_list = repo.find_all(class_='c-grid_col is-grid-col-1') # item block
    except:
        repo_list = []
        price0 = "No in stock"

    for repo in repo_list:
        name1 = repo.find(class_='a-typo is-secondary').text.split('/')
        name0 = name1[0].strip()
        try:
            price1 = repo.find(class_='a-price_price').text.split('/')
            price0 = price1[0].strip()
        except:
            price0 = "No in stock"

        link0 = repo.find(class_='a-typo is-secondary')
        link0 = link0.get("href")
        link0 = link_page + link0
        
        price0 = format_price(price0)
        name.append(name0)
        price.append(price0)
        link.append(link0)
    if name:
        name, price, link = sort(name, price, link, sort_by)
        save_query(name, price, link, 3)
        return(name, price, link)
    else:
        return("", "", "")

def check_media(url, id):
    page = requests.get(str(url))
    soup = BeautifulSoup(page.text, 'html.parser')

    repo = soup.find(class_="c-layout v-product v-product_show") #contener

    price1 = repo.find(class_='a-price_price').text.split('/')
    price0 = price1[0].strip()
    
    save_single(id, price0)

def query_run(url, shop_id):
    if shop_id == 1:
        name, price1, link = x_kom("", "name_low", url)

    if shop_id == 2:
        name, price1, link = morele("", "name_low", url)
        
    if shop_id == 3:
        name, price1, link = media_expert("", "name_low", url)

    save_query(name, price1, link, shop_id)

    
def query_prep(choice):
    import concurrent.futures
    import time
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
        executor.map(query_run, urls, shop_id)

    stats_end = len(Item.query.order_by(Item.id).all())
    
    item_len = stats_end - stats_start
    end = time.time()
    times = end - start
    times = times

    query_stats(times, item_len)

def check_stats():
    items = Item.query.order_by(Item.id).all()
    prices = Prices.query.order_by(Prices.id).all()

    xkom = len(Item.query.filter_by(shop_id=1).all())
    morele = len(Item.query.filter_by(shop_id=3).all())
    media = len(Item.query.filter_by(shop_id=4).all()) 
    avg = len(prices)/len(items)

    return len(items), len(prices), xkom, morele, media, avg

def query_stats(time, added):
    now_date = now.strftime("%d-%m-%Y")
    now_time = now.strftime("%H:%M:%S")

    total = len(Item.query.order_by(Item.id).all())
    query = Query(date=now_date, time=now_time, run_time=time, added=added, match=query_stats_match, searched=query_ststs_searched, total=total)
    db.session.add(query)
    db.session.commit()

query_stats_match = 0
query_ststs_searched = 0
def query_stats2(match0, searched):
    global query_stats_match
    global query_ststs_searched
    
    query_stats_match+=match0
    query_ststs_searched+=searched

def return_query_stats():
    query = Query.query.order_by(Query.id).all()
    return query[-1].date, query[-1].time, query[-1].run_time, query[-1].added, query[-1].match, query[-1].searched, query[-1].total

def update_stats(time, updated):
    now_date = now.strftime("%d-%m-%Y")
    now_time = now.strftime("%H:%M:%S")

    total = len(Prices.query.order_by(Prices.id).all())
    updates = Update(date=now_date, time=now_time, run_time=time, updated=updated, total=total)
    db.session.add(updates)
    db.session.commit()


def return_update_stats():
    update = Update.query.order_by(Update.id).all()
    return update[-1].date, update[-1].time, update[-1].run_time, update[-1].updated, update[-1].total

def return_search(item, sort_by1):
    processes = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        xkom0 = executor.submit(x_kom, item, sort_by1)
        morele0 = executor.submit(morele, item, sort_by1)
        media0 = executor.submit(media_expert, item, sort_by1)

        x_name, x_price, x_link = xkom0.result()
        morele_name, morele_price, morele_link = morele0.result()
        media_name, media_price, media_link = media0.result()

    return  x_name, x_price, x_link, morele_name, morele_price, morele_link, media_name, media_price, media_link


def return_lowest_price(names):
    lowest_price = []
    l_price = []
    for name in names:
        items = Item.query.filter_by(name=name).all()
        for item in items:
            prices = Prices.query.filter_by(item_id=item.id).all()

            for price in prices:
                l_price.append(price.price)
                l_price.sort()
                lowest_price.append(l_price[0])
                l_price.clear() 

    return lowest_price

def return_highest_price(names):
    highest_price = []
    h_price = []
    for name in names:
        items = Item.query.filter_by(name=name).all()
        for item in items:
            prices = Prices.query.filter_by(item_id=item.id).all()

            for price in prices:
                h_price.append(price.price)
                h_price.sort()
                highest_price.append(h_price[-1])
                h_price.clear() 

    return highest_price
        
def add_spec(url0):
    url = list(url0)
    xkom_template = url[12]+url[13]+url[14]+url[15]+url[16]
    morele_template = url[12]+url[13]+url[14]+url[15]+url[16]+url[17]
    media_template = url[12]+url[13]+url[14]+url[15]+url[16]
    
    if xkom_template == "x-kom":
        save_spec(url0, 1)
    if morele_template == "morele":
        save_spec(url0, 2)
    if media_template == "media":
        save_spec(url0, 3)

def get_name_by_url_xkom(url):
    page = requests.get(str(url))
    soup = BeautifulSoup(page.text, 'html.parser')

    repo = soup.find(class_="page-wrapper") #contener
    name1 = repo.find(class_='sc-1x6crnh-5 cYILyh').text.split('/')
        
    name = ''.join(name1)
    # name = format_name(name)
    return name

def get_price_by_url_xkom(url):
    page = requests.get(str(url))
    soup = BeautifulSoup(page.text, 'html.parser')

    repo = soup.find(class_="page-wrapper") #contener
    try:
        price1 = repo.find(class_='u7xnnm-4 iVazGO').text.split('/')
    except:
        price1 = repo.find(class_='u7xnnm-3 gAOShm').text.split('/')

    price0 = price1[0].strip()
    price = format_price(price0)
    return price

def save_spec(url, shop_id):
    item = Item.query.filter_by(url=url).first()

    if not item:
        name = get_name_by_url_xkom(url)
        
        item = Item(name=name, url=url, shop_id=shop_id)
        db.session.add(item)
        db.session.commit()

    spec = Spec.query.filter_by(item_id=item.id).first()
    if not spec:
        spec = Spec(item_id=item.id)
        db.session.add(spec)
        db.session.commit()

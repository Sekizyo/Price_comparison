import re
import csv
import sys
import time
import operator
import requests

import concurrent.futures
from webbot import Browser
from bs4 import BeautifulSoup

from module.sql_func import save_query, add_update_stats, add_price_by_id
from module.models import Item, Prices, Query, Update, Spec 
from module.pretty import sort, format_price, time_start, time_end

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
        
        name, price, link = sort(name, price, link, sort_by)
        save_query(name, price, link, 1)

        return(name, price, link)
    else:
        return("", "", "")

def check_xkom(url, id):
    page = requests.get(str(url))
    soup = BeautifulSoup(page.text, 'html.parser')
    repo = soup.find(class_="page-wrapper") #contener
    price1 = repo.find(class_='u7xnnm-4 iVazGO').text.split('/')
    price0 = price1[0].strip()
    
    add_price_by_id(id, price0)
            
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
            break

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
    
    add_price_by_id(id, price0)

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
            break

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
    
    add_price_by_id(id, price0)

def search_all(item, sort_by1):
    processes = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        xkom0 = executor.submit(x_kom, item, sort_by1)
        morele0 = executor.submit(morele, item, sort_by1)
        media0 = executor.submit(media_expert, item, sort_by1)

        x_name, x_price, x_link = xkom0.result()
        morele_name, morele_price, morele_link = morele0.result()
        media_name, media_price, media_link = media0.result()

    return x_name, x_price, x_link, morele_name, morele_price, morele_link, media_name, media_price, media_link
   
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
    
def check_spec(shop):
    price = Spec_Prices.query.filter_by(shop_id=shop).all()#TODO check if price changed
    pass

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
    
    updated = stats_end - stats_start
    end = time.time()
    times = end - start
    times = times

    add_update_stats(times, updated)
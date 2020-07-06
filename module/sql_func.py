from module import app, db
from module.models import Item, Prices, Query, Update, Spec
from module.pretty import time_start, time_end, format_price
from flask_sqlalchemy import BaseQuery

import concurrent.futures

import time
import datetime
now = datetime.datetime.now()
now_date = now.strftime("%d-%m-%Y")

def add_spec(url, shop_id):
    item = Item.query.filter_by(url=url).first()

    if not item:
        name = get_name_by_url_xkom(url)#TODO fix
        
        item = Item(name=name, url=url, shop_id=shop_id)
        db.session.add(item)
        db.session.commit()

    spec = Spec.query.filter_by(item_id=item.id).first()
    if not spec:
        spec = Spec(item_id=item.id)
        db.session.add(spec)
        db.session.commit()

def add_price_by_id(id, price):
    now = datetime.datetime.now()
    now_date = now.strftime("%d-%m-%Y")

    price = format_price(price)
    
    item = Item.query.filter_by(id=id).first()
    old_price = Prices.query.filter_by(item_id=item.id).all()

    if len(old_price) == 0:
            item_price = Prices(author=item, created=now_date, price=price)
            db.session.add(item_price)
            db.session.commit()
    else:
        if not int(price) == int(old_price[-1].price):
            item_price = Prices(author=item, created=now_date, price=price)
            db.session.add(item_price)
            db.session.commit()
    
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

def add_update_stats(time, updated):
    now_date = now.strftime("%d-%m-%Y")
    now_time = now.strftime("%H:%M:%S")

    total = len(Prices.query.order_by(Prices.id).all())
    updates = Update(date=now_date, time=now_time, run_time=time, updated=updated, total=total)
    db.session.add(updates)
    db.session.commit()

def add_spec_by_url(url0):
    url = list(url0)
    xkom_template = url[12]+url[13]+url[14]+url[15]+url[16]
    morele_template = url[12]+url[13]+url[14]+url[15]+url[16]+url[17]
    media_template = url[12]+url[13]+url[14]+url[15]+url[16]
    
    if xkom_template == "x-kom":
        add_spec(url0, 1)
    if morele_template == "morele":
        add_spec(url0, 2)
    if media_template == "media":
        add_spec(url0, 3)
        
def add_spec(url, shop_id):
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

def add_query_stats(time, added):
    now_date = now.strftime("%d-%m-%Y")
    now_time = now.strftime("%H:%M:%S")

    total = len(Item.query.order_by(Item.id).all())
    query = Query(date=now_date, time=now_time, run_time=time, added=added, total=total)
    db.session.add(query)
    db.session.commit()

import os
import time
import datetime
from datetime import time

from flask import render_template, url_for, flash, redirect, request, Response

from module import app, db
from module.models import Item, Prices
from module.check import x_kom, euro, morele, media_expert, query_prep, check_stats, return_query_stats, update_prices, return_update_stats, return_search, compare, query_by_url
from module.forms import Search_item, Query_items, Spec_item

now = datetime.datetime.now()
now_date = now.strftime("%d-%m-%Y")
now_date2 = now.strftime("%Y-%m-%d")

@app.route('/')
@app.route("/index", methods=['GET', 'POST'])
def index():
    search = url_for('search')
    query = url_for('query')
    update = url_for('update')
    spec = url_for('spec')
    stats = url_for('stats')
    test = url_for('test')
    return render_template('index.html', search=search, query=query, update=update, spec=spec, stats=stats, test=test)

@app.route("/search", methods=['GET', 'POST'])
def search():
    form = Search_item()
    return render_template('search.html', form=form)


@app.route("/search_result", methods=['GET', 'POST'])
def search_result():
    form = Search_item()
    item_name = form.item.data
    sort_by = form.sort_by.data

    x_name, x_price, x_link, euro_name, euro_price, euro_link, morele_name, morele_price, morele_link, media_name, media_price, media_link = return_search(item_name, sort_by)
    x_low_prices = compare(x_name)
    euro_low_prices = compare(euro_name)
    morele_low_prices = compare(morele_name)
    media_low_prices = compare(media_name)

    x_kom_len = len(x_name)
    euro_len = len(euro_name)
    morele_len = len(morele_name)
    media_len = len(media_name)

    return render_template('search_result.html',item_name=item_name, x_name=x_name, x_price=x_price, x_low_prices=x_low_prices, x_link=x_link, x_kom_len=x_kom_len,
        euro_name=euro_name, euro_price=euro_price, euro_low_prices=euro_low_prices, euro_link=euro_link, euro_len=euro_len,
        morele_name=morele_name, morele_price=morele_price, morele_low_prices=morele_low_prices, morele_link=morele_link, morele_len=morele_len,
        media_name=media_name, media_price=media_price, media_low_prices=media_low_prices, media_link=media_link, media_len=media_len)


@app.route("/query", methods=['GET', 'POST'])
def query():
    form = Query_items()
    return render_template('query.html', form=form)
     
@app.route('/query_result', methods=['GET', 'POST'])
def query_search():
    form = Query_items()
    query_items = form.query.data
    query_prep(query_items)
    date, time, run_time, added, match, searched, total = return_query_stats()
    return render_template('query_result.html', time=time, run_time=run_time, added=added, match=match, searched=searched, total=total)

@app.route('/spec', methods=['GET', 'POST'])
def spec():
    spec_add = url_for('spec_add')
    spec_show = url_for('spec_show')
    spec_del = url_for('spec_del')

    return render_template('spec.html', spec_add=spec_add, spec_show=spec_show, spec_del=spec_del)

@app.route('/spec_add', methods=['GET', 'POST'])
def spec_add():
    

    return render_template('spec_add.html')

@app.route('/spec_show', methods=['GET', 'POST'])
def spec_show():
    

    return render_template('spec_show.html')

@app.route('/spec_del', methods=['GET', 'POST'])
def spec_del():
    

    return render_template('spec_del.html')

@app.route('/spec_result', methods=['GET', 'POST'])#TODO add spec to system
def spec_result():
    form = Spec_item()

    url = form.url.data
    choice = form.choice.data

    if choice == "x_kom":
        # spec_xkom(url)
        pass
    if choice == "euro":
        #spec_euro(url)
        pass
    if choice == "morele":
        #spec_morele(url)
        pass
    if choice == "media_expert":
        #spec_media(url)
        pass

    flash('Succes', 'succes')
    return redirect(url_for('spec'))

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    items, prices, xkom, euro, morele, media, avg = check_stats()
    query_date, query_time, query_run_time, query_added, query_match, query_searched, query_total = return_query_stats() 
    return render_template('stats.html', items=items, prices=prices, xkom=xkom, euro=euro, morele=morele, media=media, avg=avg, query_date=query_date, query_time=query_time, query_run_time=query_run_time, query_added=query_added)

@app.route('/update', methods=['GET', 'POST'])
def update():
    update_prices()
    update_date, update_time, update_run_time, update_updated, update_total = return_update_stats() 
    return render_template('update_result.html', update_date=update_date, update_time=update_time, update_run_time=update_run_time, update_updated=update_updated, update_total=update_total)

@app.route('/test', methods=['GET', 'POST'])
def test():
    query_by_url("https://www.x-kom.pl/p/566358-smartfon-telefon-xiaomi-redmi-note-9-3-64gb-forest-green.html")
    return render_template('test.html')
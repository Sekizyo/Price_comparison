from module.models import Item, Prices, Query, Update, Spec

def return_query_stats():
    query = Query.query.order_by(Query.id).all()
    return query[-1].date, query[-1].time, query[-1].run_time, query[-1].added, query[-1].total

def return_update_stats():
    update = Update.query.order_by(Update.id).all()
    return update[-1].date, update[-1].time, update[-1].run_time, update[-1].updated, update[-1].total

def return_spec_stats(): #TODO
    query = Query.query.order_by(Query.id).all()
    return query[-1].date, query[-1].time, query[-1].run_time, query[-1].added, query[-1].total

def return_total_stats():
    items = Item.query.order_by(Item.id).all()
    prices = Prices.query.order_by(Prices.id).all()

    xkom = len(Item.query.filter_by(shop_id=1).all())
    morele = len(Item.query.filter_by(shop_id=3).all())
    media = len(Item.query.filter_by(shop_id=4).all()) 
    avg = len(prices)/len(items)

    return len(items), len(prices), xkom, morele, media, avg

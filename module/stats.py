from module.models import Item, Prices, Query, Update, Spec

def return_query_stats():
    query = Query.query.order_by(Query.id).all()
    return query[-1].date, query[-1].time, query[-1].run_time, query[-1].added, query[-1].total

def return_update_stats():
    update = Update.query.order_by(Update.id).all()
    return update[-1].date, update[-1].time, update[-1].run_time, update[-1].updated, update[-1].total

def return_spec_stats():
    ids = [] 
    item_ids = [] 
    
    names = [] 
    urls = []
    shop_ids = [] 
    
    spec = Spec.query.order_by(Spec.id).all()
    for items in spec:
        item = Item.query.filter_by(id=items.item_id).first()

        ids.append(items.id)
        item_ids.append(items.item_id)

        names.append(item.name)
        urls.append(item.url)
        shop_ids.append(item.shop_id)
        
    return ids, item_ids, names, urls, shop_ids

def return_total_stats():
    items = Item.query.order_by(Item.id).all()
    prices = Prices.query.order_by(Prices.id).all()

    xkom = len(Item.query.filter_by(shop_id=1).all())
    morele = len(Item.query.filter_by(shop_id=3).all())
    media = len(Item.query.filter_by(shop_id=4).all()) 
    avg = len(prices)/len(items)

    return len(items), len(prices), xkom, morele, media, avg

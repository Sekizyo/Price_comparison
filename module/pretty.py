from module import app, db
from module.models import Item, Prices, Query, Update, Spec
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

    lower_strings = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
    high_strings = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'y', 'Z']
    black_list = [' ', ',', '\n', '\t', '\xa0', 'ł', 'Ł']

    for x in range(len(price_formated)):
        for y in lower_strings:
            try:
                price_formated.remove(y)
            except:
                pass

        for z in high_strings:
            try:
                price_formated.remove(z)
            except:
                pass

        for t in black_list:
            try:
                price_formated.remove(t)
            except:
                pass

    price0 = ''.join(price_formated)

    return price0

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

def get_lowest_price(names):
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

def get_highest_price(names):
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
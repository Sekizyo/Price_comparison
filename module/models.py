from datetime import datetime
from module import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    shop_id = db.Column(db.Integer, nullable=False)

    prices = db.relationship('Prices', backref='author')

    def __repr__(self):
        return f"Item(ID: '{self.id}', Name: '{self.name}', ShopId: '{self.shop_id}')"

class Prices(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    created = db.Column(db.Text, default="0", nullable=False)
    price = db.Column(db.Integer, default="0", nullable=False)

    def __repr__(self):
        return f"Prices(Item_id: '{self.item_id}',Created: '{self.created}', Price: '{self.price}')"

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text, nullable=False)

    run_time = db.Column(db.Text, nullable=False)
    added = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Query(ID: '{self.id}', Date: '{self.date}', Time: '{self.time}', Run time: '{self.run_time}', Added: '{self.added}', Total: '{self.total}')"

class Update(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text, nullable=False)

    run_time = db.Column(db.Text, nullable=False)
    updated = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Query(ID: '{self.id}', Date: '{self.date}', Time: '{self.time}', Run time: '{self.run_time}', Updated: '{self.updated}', Total: '{self.total}')"


class Spec(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Spec(ID: '{self.id}', Item id: '{self.item_id}')"

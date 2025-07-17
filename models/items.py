from db import db

#tables and columns
class ItemModel(db.Model):
    __tablename__ = "items" #create a table named items for this class

    #Columns for the table
    id = db.Column(db.Integer, primary_key = True)  #autoincrement
    name = db.Column(db.String(80), nullable = False)   
    price = db.Column(db.Float(precision = 2), nullable = False, unique = False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"),nullable = False, unique = False)
    store = db.relationship("StoreModel", back_populates = "item")
    tags = db.relationship('TagModel', back_populates = 'item', secondary = 'item_tags')


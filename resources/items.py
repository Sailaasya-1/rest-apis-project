import uuid
from db import db

from flask import Flask, request
from flask_smorest import abort, Blueprint
from flask.views import MethodView

from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel

from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt


#from db import items- as we are creating sqlalchemy for database   
blp = Blueprint("Items", __name__, description = "Operation on items.")

@blp.route('/item')
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many = True))  #it usually expects single object but we ask it to treat as multiple 
    def get(self):
        return ItemModel.query.all()
    
    #here to create a new time we need the fresh = true which is the access_token generated while logging in but not with the help of refresh_token.
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)    #it should have name,price and store_id
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "An error occured while inserting an item.")
        return item

@blp.route('/item/<int:item_id>')
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)  #The response which needs to follow ItemSchema
    def get(self,item_id):
        item = ItemModel.query.get_or_404(item_id)  #automatically abort if it doesnt find(db comes from db.Model that flask sqlalchmey provides)
        return item 
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self,item_data, item_id):
        item = ItemModel.query.get(item_id) ##fetching the item_id
        if item:
            item.price = item_data['price']
            item.name = item_data['name']
        else:
            item = ItemModel(id = item_id, **item_data)
        db.session.add(item)
        db.session.commit()

        return item
    
    #Here the item is deleted only if the user registered is one.
    @jwt_required()
    def delete(self,item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message = "Admin access is required.")

        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}



#2- @blp.route('/item')
# class ItemList(MethodView):
#     @blp.response(200, ItemSchema(many = True))  #it usually expects single object but we ask it to treat as multiple 
#     def get(self):
#         return items
    
#     @blp.arguments(ItemSchema)
#     @blp.response(201, ItemSchema)
#     def post(self, item_data):
#         item = ItemModel(**item_data)
#         try:
#             db.session.add(item)
#             db.session.commit()
#         except SQLAlchemyError:
#             abort(500, message = "An error occured while inserting an item.")
#         return item

# 2- @blp.route('/item/<string:item_id>')
# class Item(MethodView):
#     @blp.response(200, ItemSchema)  #The response which needs to follow ItemSchema
#     def get(self,item_id):
#         try:
#             return items[item_id]
#         except KeyError:
#             abort(404, message = "Item not found.")
    
#     @blp.arguments(ItemUpdateSchema)
#     @blp.response(200,ItemSchema)
#     def put(self,item_data, item_id):
#         #Here price is a number and both items
#         try:
#             item = items[item_id]
#             item |= item_data
#             return item, 201
#         except:
#             abort(400, message = "Item mot found")

#     def delete(self,item_id):
#         try:
#             del items[item_id]
#             return {"message": "Item deleted"}
#         except KeyError:
#             abort(400, messaage = "Item not found to perform the delete operation.")




# @blp.route('/item')
# class ItemList(MethodView):
#     @blp.response(200, ItemSchema(many = True))  #it usually expects single object but we ask it to treat as multiple 
#     def get(self):
#         return items.values()
    
#     @blp.arguments(ItemSchema)
#     @blp.response(201, ItemSchema)
#     def post(self, item_data):
#         for item in items:
#             if item['store_id'] == item_data['store_id'] and item['name'] == item_data['name']:
#                 abort(400, message = f"Item already exists in that store.")

#         item_id = uuid.uuid4().hex
#         new_item = {** item_data, "id": item_id}
#         items[item_id] = new_item
#         return new_item, 201
    


# @blp.route('/item/<string:item_id>')
# class Item(MethodView):
#     @blp.response(200, ItemSchema)  #The response which needs to follow ItemSchema
#     def get(self,item_id):
#         try:
#             return items[item_id]
#         except KeyError:
#             abort(404, message = "Item not found.")
    
#     @blp.arguments(ItemUpdateSchema)
#     @blp.response(200,ItemSchema)
#     def put(self,item_data, item_id):
#         #Here price is a number and both items
#         try:
#             item = items[item_id]
#             item |= item_data
#             return item, 201
#         except:
#             abort(400, message = "Item mot found")

#     def delete(self,item_id):
#         try:
#             del items[item_id]
#             return {"message": "Item deleted"}
#         except KeyError:
#             abort(400, messaage = "Item not found to perform the delete operation.")

    


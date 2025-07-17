import uuid
from db import db
from flask import request


from flask_smorest import abort, Blueprint
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


#from db import stores - as we are using sqlalchemy for database
from schemas import StoreSchema
from models import StoreModel


blp = Blueprint("stores", __name__, description = "Operation on stores")  # goes into api documentation 
#Blueprint divides api into segments and the __name__ to have a unique for stores.

#This connects with flask_smorest to methodview
@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store


    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message" :"store deleted"}


@blp.route('/store')     #Doesn't need to be a list and takes the value paramters = true for taking all the paramters that schema has
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        new_store = StoreModel(**store_data)
        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "Store already exsits.")
        except SQLAlchemyError:
            abort(500, message = "An error occured while creating a store.")
        return new_store
    
# #This connects with flask_smorest to methodview
# 2-app.route("/store/<string:store_id>")
# class Store(MethodView):
#     @blp.response(200, StoreSchema)
#     def get(self, store_id):
#         try:
#            return stores[store_id]
#         except KeyError:
#             abort(404, message = "Store not found.")

#     def delete(self, store_id):
#         try:
#            del stores[store_id]
#            return {"message": "Store is deleted."}
#         except KeyError:
#            abort(400, message = "Store not found to perform delete operation.")


#2- lp.route('/store')     #Doesn't need to be a list and takes the value paramters = true for taking all the paramters that schema has
# class StoreList(MethodView):
#     @blp.response(200, StoreSchema(many=True))
#     def get(self):
#         return stores.values()
    
#     @blp.arguments(StoreSchema)
#     @blp.response(200, StoreSchema)
#     def post(self, store_data):
#         new_store = StoreModel(**store_data)
#         try:
#             db.session.add(new_store)
#             db.session.commit()
#         except IntegrityError:
#             abort(400, message = "Store already exsits.")
#         except SQLAlchemyError:
#             abort(500, message = "An error occured while creating a store.")
#         return new_store
      
# @blp.route("/store/<string:store_id>")
# class Store(MethodView):
#     @blp.response(200, StoreSchema)
#     def get(self, store_id):
#         try:
#            return stores[store_id]
#         except KeyError:
#             abort(404, message = "Store not found.")

#     def delete(self, store_id):
#         try:
#            del stores[store_id]
#            return {"message": "Store is deleted."}
#         except KeyError:
#            abort(400, message = "Store not found to perform delete operation.")


# @blp.route('/store')     #Doesn't need to be a list and takes the value paramters = true for taking all the paramters that schema has
# class StoreList(MethodView):
#     @blp.response(200, StoreSchema(many=True))
#     def get(self):
#         return stores.values()
    
#     @blp.arguments(StoreSchema)
#     @blp.response(200, StoreSchema)
#     def post(self, store_data):
#         for store in stores:
#             if store["name"] == store_data["name"]:
#                 abort(400, message = "Store already exists.")
#         store_id = uuid.uuid4().hex
#         new_store = {'id': store_id, ** store_data}
#         stores[store_id] = new_store
#         return new_store, 201
    
    
    
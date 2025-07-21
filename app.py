import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager, jwt_required
from flask_migrate import Migrate
from dotenv import load_dotenv

import models #same as calling models.__init__
from db import db
from blocklist import BLOCKLIST

from resources.items import blp as ItemBlueprint
from resources.stores import blp as StoreBlueprint
from resources.tags import blp as TagBlueprint
from resources.users import blp as UserBlueprint

def create_app(db_url = None):

    #Factory pattern
    app = Flask(__name__)

    #This function loads the env file and calls the DBURL this loads the Postgresql link.
    load_dotenv()

    #We need to register these blueprints with API
    app.config['PROGATE_EXCEPTIONS'] = True #extension that occurs hidden inside the extension of flask to propogate 
    app.config['API_TITLE'] = "Stores REST API"   #documentation
    app.config['API_VERSION'] = "v1"
    app.config['OPENAPI_VERSION'] = "3.0.3"    #standard version
    app.config['OPENAPI_URL_PREFIX'] = "/"      #root of api as it starts with /
    app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger-ui"       #tells swagger to use api documentation
    app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"   #code is here
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")  #we use env var if its exsists uses that value or sqlite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False                                                   # we often use env variable as its stores arbitary ssecrest
                                                                                                             
    
    db.init_app(app) #connecting sqlalchmey to app
    api = Api(app)

    #Adding the flask-migrate connection between flask and alembic
    migrate = Migrate(app, db)
    
    #Creating a secret key using JWT
    app.config['JWT_SECRET_KEY'] = "jose"
    jwt = JWTManager(app)

    #It takes the jwt and then checks if the jwt is already stored inside the blocklist.
    #If the jwt is already stored it return false and we have the other function for returning the message for false.
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description":"The token has been revoked.", "error": "token_revoked"}
            ), 401
        )
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (jsonify(
            {
             "description":"The token is not fresh",
             "error": "fresh_token_required"
        }
        ),
        401
        )
    
    #Here we are adding additional claims to the user
    #Providing the admin access for deletion. Only the first registered user as the identity is set to 1.
    #The user created using jwt will have an identity, that identity is used.
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        else:
            return {"is_admin" : False}
    

    #The access token which is considered expired, invalid and unauthorized.
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return(jsonify({"message":"The token has expired", 
                       "error":"token expired"}), 401)
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return(jsonify({"message":"Signature verfication failed.",
                        "error":"invalid_token"}), 401)
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(jsonify({"description":"Request does not contain access token",
                        "error":"authorization_required"}, 401))

    # with app.app_context():
    #     db.create_all()


    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app



#Storing the data inside the list
#@app.get('/store')
#def get_store():
# return {'stores': stores}
# @app.post('/store')
# def create_store():
# request_data = request.get_json()
    # new_store = {'name': request_data['name'], 'items':[]}
    # stores.append(new_store)
    # return new_store, 201


# @app.post('/store/<string:name>/item')
# def create_item(name):
#     request_data = request.get_json()
#     for store in stores:
#         if store['name'] == name:
#             new_item = {'name': request_data['name'], 'price': request_data['price']}
#             store['items'].append(new_item)
#             return new_item, 201
#     return {"message": "Store not found"}, 404


# @app.get('/store/<string:name>')
# def get_store_details(name):
#     for store in stores:
#         if store['name'] == name:
#             return store
#     return {"message" : "store not found"}, 404

# @app.get('/store/<string:name>/item')
# def get_store_items(name):
#     for store in stores:
#         if store['name'] == name:
#             return {'items': store['items']}
#     return {"message" : "store not found"}, 404


#Updated code
# @app.get('/store')
# def get_stores():
#     return {"stores": list(stores.values())}

# @app.get('/store/<string:store_id>')
# def get_store(store_id):
#     try:
#         return stores[store_id]
#     except KeyError:
#         abort(404, message = "Store not found.")

# @app.get('/item')
# def get_items():
#     return {"items":list(items.values())}

# @app.get('/item/<string:item_id>')
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         abort(404, message = "Item not found.")

# @app.delete('/item/<string:item_id>')
# def delete_item(item_id):
#     try:
#         del items[item_id]
#         return {"message": "Item deleted"}
#     except KeyError:
#         abort(400, messaage = "Item not found to perform the delete operation.")


# @app.post('/store')
# def create_store():
#     store_data = request.get_json()
#     if "name" not in store_data:
#         abort(400, message = "Bad request, ensure to include name in the requested payload.")
#     for store in stores:
#         if store["name"] == store_data["name"]:
#             abort(400, message = "Store already exists.")
#     store_id = uuid.uuid4().hex
#     new_store = {'id': store_id, ** store_data}
#     stores[store_id] = new_store
#     return new_store, 201

    
# @app.post('/item')
# def create_items():
#     item_data = request.get_json()
#     if (
#         'price' not in item_data or
#         'name' not in item_data or
#         'store_id' not in item_data
#     ):
#         abort(400, message = "Make sure to have price, name and store_id in the sending request.")
#     for item in items:
#         if item['store_id'] == item_data['store_id'] and item['name'] == item_data['name']:
#             abort(400, message = f"Item already exists in that store.")
#     item_id = uuid.uuid4().hex
#     new_item = {** item_data, "id": item_id}
#     items[item_id] = new_item
#     return new_item, 201
        


# @app.put('/item/<string:item_id>')
# def update_item(item_id):
#     item_data = request.get_json()
#     if ("name" not in item_data or "price" not in item_data):
#         abort(400, message = "Please provide name and price for the item to stay updated.")
#     try:
#         item = items[item_id]
#         item |= item_data
#         return item, 201
#     except:
#         abort(400, message = "Item mot found")

# @app.delete('/store/<string:store_id>')
# def delete_store(store_id):
#     try:
#         del stores[store_id]
#         return {"message": "Store is deleted."}
#     except KeyError:
#         abort(400, message = "Store not found to perform delete operation.")

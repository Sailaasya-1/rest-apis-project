from marshmallow import Schema, fields


#For checking the data type of the variables

#Post - request for items
#dump_only to return the value, required taking input and sending output
#This doesnt deal with store, include nested item within a store but we dont want to add anything about store itself.
class PlainItemSchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str(required = True)
    price = fields.Float(required = True)
    

#Post - Create a store
class PlainStoreSchema(Schema):
    id = fields.Str(dump_only = True)
    name = fields.Str(required=True)


#Post - Create a Tag
class PlainTagSchema(Schema):
    id = fields.Int(dump_only = True)
    name = fields.Str()


#Put - update details of an item, here updating an item doesn't need all paramters.
#Name or Price should be enough
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True,load_only=True)
    store = fields.Nested(PlainStoreSchema(),dump_only = True )  # we dont want to include tonly the storeid, i want to include the nested store object
    

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only = True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only = True)

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only = True)
    store = fields.Nested(PlainStoreSchema(), dump_only = True)
    item = fields.Nested(PlainItemSchema(), dump_only = True)

class ItemsTagSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only = True)
    username = fields.String(required= True)
    password = fields.String(required = True, load_only= True)
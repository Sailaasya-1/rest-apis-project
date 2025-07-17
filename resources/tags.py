from db import db

from flask import Flask, request
from flask_smorest import abort, Blueprint
from flask.views import MethodView

from schemas import TagSchema, PlainTagSchema, ItemsTagSchema
from models import  StoreModel, TagModel, ItemModel, Itemtags

from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("Tags", "tags", description = "Operation on tags")

@blp.route('/store/<string:store_id>/tag')
class TagInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tag.all()

    
    @blp.arguments(TagSchema)
    @blp.response(200, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data, store_id = store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message = str(e)) #the error is converted into the string
    
        return tag
    
@blp.route('/item/<int:item_id>/tag/<int:tag_id>')
class LinkTagstoItem(MethodView):
    @blp.response(200, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tag.append(tag)   #considering the tag as list in the item column and then adding the tag to it
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "an error occurd while inserting the tag")
        
        return tag
    
    @blp.response(200, ItemsTagSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.delete(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "An error occured while deleting te tag")
        
        return {"message": "Item removed", "item":item, "tag":tag}
    


@blp.route('/tag/<int:tag_id>')
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(200, description= "Deletes a tag if no item is tagged with it.", example = {"message":"tag deleted"})
    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(404, description="Returned if the tag is assigned to one or more items. In this case, tag is not deleted.")
    
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        #If the tag doesn't have any items with it then delete it
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
        
        abort(400, message = "Could not delete the tag make sure it is assigned with the items, then try again.")
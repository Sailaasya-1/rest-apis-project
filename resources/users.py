import os
import requests
from flask_smorest import abort, Blueprint
from schemas import UserSchema, UserRegisterSchema
from models import UserModel
from sqlalchemy import or_
from db import db
from blocklist import BLOCKLIST
from flask.views import MethodView

#hash algorithm turn passsword into unreadabel characters
from passlib.hash import pbkdf2_sha256

#Combinaation of nums and chars, generate in the server.
from flask_jwt_extended import create_access_token,create_refresh_token, get_jwt_identity, jwt_required, get_jwt

blp = Blueprint("Users", "users", description = "Operation on users")

#The function from the mail gun to send the emails to the users.
def send_simple_message(to, subject, body):
    domain = os.getenv("MAILGUN_DOMAIN")
    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={
            "from": f"GSL <mailgun@{domain}>",
            "to": [to],
            "subject": subject,
            "text": body
        }
    )


@blp.route('/register')
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            or_(
                UserModel.username == user_data['username'],
                UserModel.email == user_data['email']
        )).first():
            abort(409, message = "A user with that username already exists.")
        
        user = UserModel(
            username = user_data['username'],
            password = pbkdf2_sha256.hash(user_data['password']),
            email = user_data['email']
        )
        db.session.add(user)
        db.session.commit()

        send_simple_message( to = user.email, subject = "Successffuly signed up", body = f"Hi {user.username}! You have successfully signed up to the Stores REST API.")
        return {"message":"user created successful"}, 201


@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data['username']).first()

        #checking if the user exsits and along side checking the password with the DB password
        if user and pbkdf2_sha256.verify(user_data['password'], user.password):

            #The access_token is the fresh token which is generated while logging-in
            access_token = create_access_token(identity= str(user.id), fresh = True)
            refresh_token = create_refresh_token(identity= str(user.id))
            return {"access_token": access_token, "refresh_token": refresh_token}
        
        abort(401, message = "Invalid credentials.")

@blp.route('/refresh')
class TokenRefresh(MethodView):
    @jwt_required(refresh = True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        #To set the limit for the access_token to get generated from refresh_token.
        #After collecting the jti it is added to the blocklist which means the refreah_token can only be used oncw for generating access_token.
        
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"access_token":new_token}
        
@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"message":"Successfully logged out."}

@blp.route('/user/<int:user_id>')
class User(MethodView):
    @blp.arguments(UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message":"user deleted"}


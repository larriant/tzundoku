import models

from flask import Flask
from flask.ext.restful import reqparse, abort, fields, marshal_with, Resource
from tzundoku import tzundoku, db, tzundoku_api

user_fields={
    'id' : fields.Integer,
    'username' : fields.String,
    'email' : fields.String
}

class UserList(Resource):
    @marshal_with(user_fields)
    def get(self):
        users=models.User.query.all()
        return users

class SingleUser(Resource):
    @marshal_with(user_fields)
    def get(self, username):
        users=models.User.query.filter_by(username=username).all()
        return users

doku_fields={
    'name' : fields.String,
    'id' : fields.Integer
}

class DokuResource(Resource):
    @marshal_with(doku_fields)
    def get(self, doku_name):
        dokus=models.Doku.query.filter_by(doku=doku_name).all()
        return dokus

tzundoku_api.add_resource(UserList, '/users')
tzundoku_api.add_resource(SingleUser, '/users/<string:username>')

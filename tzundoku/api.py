import models

from flask import Flask, jsonify, make_response
from tzundoku import tzundoku, db

@tzundoku.route('/api/v1.0/users', methods=['GET'])
def get_user_list():
    users=models.User.query.all()
    result=[{'id' : u.id, 'username' : u.username, 'email' : u.email} for u in users]
    return jsonify(users=result)

@tzundoku.route('/api/v1.0/users/<username>', methods=['GET'])
def get_user_info(username):
    user_result=models.User.query.filter_by(username=username).all()
    if len(user_result)==0:
        return make_response(jsonify(error="Username not found"), 404)
    elif len(user_result)==1:
        user=user_result[0]
        return jsonify(id=user.id, username=user.username, email=user.email)
        
    else:
        return make_response(jsonify(error="Too many users"), 404)

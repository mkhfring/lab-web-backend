
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import User, UserSchema, NewsItems, NewsCard, NewsItemsSchema, NewsCardSchema, Lab, LabSchema



news = Blueprint('news', __name__, url_prefix='/apiv1')


@news.route('/list_news', methods=['GET'])
def get_news_list():
    if request.method == 'GET':
        news_list = NewsItems.get_news_list()
                
        return jsonify(NewsItemsSchema(many=True).dump(news_list))
    
    
@news.route('/news_card', methods=['GET'])
def get_news_fied():
    if request.method == 'GET':
        news_fied = NewsCard.get_news_fied()
        
        return jsonify(NewsCardSchema().dump(news_fied))
    
    
    
@news.route('/news_card', methods=['PUT'])
@jwt_required()
def edit_news_card():
    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
        email = get_jwt_identity()
        member = User.get_member(email=email)
        if not member:
            return jsonify({"msg": "Bad Token"}), 400
        
        if member.role !='admin':
            return jsonify({"msg": "Unauthorized"}), 401
        
        title = request.json.get('title', None)
        news_card = NewsCard.get_news_fied();
        edited_card = NewsCard.edit_card(news_card, {'title': title})
        
        return jsonify(NewsCardSchema().dump(edited_card))   
    

@news.route('/edit_news', methods=['PUT'])
@jwt_required()
def edit_news_item():
    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
        email = get_jwt_identity()
        member = User.get_member(email=email)
        if not member:
            return jsonify({"msg": "Bad Token"}), 400
        
        if member.role !='admin':
            return jsonify({"msg": "Unauthorized"}), 401
        
        body= request.json.get('body', None)
        id = request.json.get('id', None)
        if id is None:
            return jsonify({"msg": "The News id should be "}), 400
        
        if body == "":
            return jsonify({"msg": "Body cannot be empty"}), 400
        
        edited_news = NewsItems.edit_news(id, body)
        if edited_news is None:
            return jsonify({"msg": "Message doesn't exist"}), 400
        
        return jsonify(NewsCardSchema().dump(edited_news))  
    

@news.route('/add_news', methods=['POST'])
@jwt_required()
def add_news_item():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
        email = get_jwt_identity()
        member = User.get_member(email=email)
        if not member:
            return jsonify({"msg": "Bad Token"}), 400
        
        if member.role !='admin':
            return jsonify({"msg": "Unauthorized"}), 401
        
        body= request.json.get('body', None)

        if body == "":
            return jsonify({"msg": "Body cannot be empty"}), 400
        
        news = NewsItems(body=body)
        NewsItems.add_news(news)
        
        return jsonify(NewsCardSchema().dump(news))  
    
    
@news.route('/delete_news', methods=['POST'])
@jwt_required()
def delete_news_item():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
        email = get_jwt_identity()
        member = User.get_member(email=email)
        if not member:
            return jsonify({"msg": "Bad Token"}), 400
        
        if member.role !='admin':
            return jsonify({"msg": "Unauthorized"}), 401
        
        id = request.json.get('id', None)
        if id is None:
            return jsonify({"msg": "The News id should be "}), 400
        
        
        deleted_news = NewsItems.delete_news(id)
        if deleted_news is None:
            return jsonify({"msg": "Message doesn't exist"}), 400
        
        return jsonify(NewsCardSchema().dump(deleted_news)) 
    
    
@news.route('/get_news', methods=['POST'])
def get_news():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
        id = request.json.get('id', None)
        if id is None:
            return jsonify({"msg": "Id is None"}), 400
        
        news = NewsItems.get_news(id)
        if news is None:
            return jsonify({"msg": "No News Found"}), 400
        
        return jsonify(NewsItemsSchema().dump(news))    
    
    
@news.route('/lab', methods=['GET'])
def get_lab():
    if request.method == 'GET':
        lab = Lab.get_lab()     
        return jsonify(LabSchema().dump(lab))    

    
@news.route('/lab', methods=('GET', 'PUT'))
@jwt_required()
def edit_lab():
    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
        email = get_jwt_identity()
        member = User.get_member(email=email)
        if not member:
            return jsonify({"msg": "Bad Token"}), 400
        
        if member.role !='admin':
            return jsonify({"msg": "Unauthorized"}), 401
        
        title = request.json.get('title', None)
        summary = request.json.get('summary', None)
        lab = Lab.get_lab();
        edited_lab = Lab.edit_lab(lab, {'title': title, 'summary':summary})
        
        return jsonify(LabSchema().dump(edited_lab))
    
    
 
    
    
# @member.route('/members', methods=(['GET']))
# def list_members():
#     if request.method =='GET':
#         members_list = User.list_members()
#         return jsonify(UserSchema(many=True).dump(members_list))
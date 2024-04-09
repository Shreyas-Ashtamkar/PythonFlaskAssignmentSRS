from flask import Blueprint, request, render_template, redirect, url_for, flash
from ..models.Recipies import Recipie
from ..models.Users import User

from sqlalchemy import or_
from ..utils import dbutils
import json

bp = Blueprint('home', __name__, url_prefix='/')
db = dbutils.get_db()

@bp.route('/')
def home_page():
    page_no  = request.args.get('page') or 1
    per_page = request.args.get('per_page') or 5
    all_recipies = Recipie.get_all(page=int(page_no), per_page=int(per_page))
    recipie_list = []
    
    for recipie in all_recipies:
        recipie_list.append({
            'id' : recipie.id,
            'title' : recipie.title.split('-')[0],
            'description'  : recipie.description[:250] + '...',
            'ingredients_count'  : len(json.loads(recipie.ingredients)),
            'instructions_count'  : len(json.loads(recipie.instructions)),
            'category' : recipie.category,
            'created_by' : User.find_user(recipie.created_by)
        })

    all_categories = [ { 'name' : category[0], 'count' : Recipie.get_category_count(category[0])} for category in db.session.query(Recipie.category).distinct().all()]

    return render_template('home.html', recipie_list=recipie_list, category_list=all_categories, pagination=all_recipies)

@bp.route('/search')
def browse_recipies():
    page_no  = request.args.get('page') or 1
    per_page = request.args.get('per_page') or 8
    requested_filters = request.args.to_dict()
    if request.args.get('page'):
        del requested_filters['page']
    request_query = ""
    category = None
    users = None
    title = None
    ingredients = None
    results = None
    
    if 'category' in requested_filters:
        category = [Recipie.category.contains(requested_filters['category'])]
        
    if 'created_by' in requested_filters:
        users = User.query.filter(User.fullname.contains(requested_filters['created_by'])).all()
    elif 'username' in requested_filters:
        users = [User.find_by_username(requested_filters['username'])]
    elif 'uid' in requested_filters:
        users = [User.find_user(requested_filters['uid'])]
    
    if 'title' in requested_filters:
        title = [Recipie.title.contains(requested_filters['title'])]
    
    if 'ingredients' in requested_filters:
        all_ingredients = requested_filters['ingredients']
        ingredients = [ingredient.strip(',') for ingredient in all_ingredients.strip(',').split(',')]
        ingredients = [Recipie.ingredients.contains(ingredient) for ingredient in ingredients]
    
    for q in requested_filters:
        request_query += f"&{q}={requested_filters[q]}"

    processed_filters = []
    
    if users:
        users = [Recipie.created_by == user.id for user in users]
        processed_filters.append(or_(*users))
    
    if title:
        processed_filters.append(or_(*title))
        
    if ingredients:
        processed_filters.append(or_(*ingredients))
        
    if category:
        processed_filters.append(or_(*category))
    
    results = Recipie.query.filter(*processed_filters).paginate(page=int(page_no), per_page=int(per_page))
    
    recipie_list = []
    for recipie in results.items:
        recipie_list.append({
            'id' : recipie.id,
            'title' : recipie.title.split('-')[0],
            'description'  : recipie.description[:250] + '...',
            'ingredients_count'  : len(json.loads(recipie.ingredients)),
            'instructions_count'  : len(json.loads(recipie.instructions)),
            'category' : recipie.category,
            'created_by' : User.find_user(recipie.created_by)
        })
    
    return render_template('search.html', recipies=recipie_list, pagination=results, all_categories=Recipie.get_categories(), current_query=f"{request_query}", requested_filters=requested_filters)

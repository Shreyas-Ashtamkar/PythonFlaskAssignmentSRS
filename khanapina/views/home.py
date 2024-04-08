from flask import Blueprint, request, render_template, redirect, url_for, flash
from ..models.Recipies import Recipie
from ..models.Users import User

from ..utils import dbutils

bp = Blueprint('home', __name__, url_prefix='/')

db = dbutils.get_db()

@bp.route('/')
def home_page():
    page_no  = request.args.get('page') or 1
    per_page = request.args.get('per_page') or 5
    all_recipies = []
        
    for recipie in Recipie.get_all(page=int(page_no), per_page=int(per_page)):
        all_recipies.append({
            'id' : recipie.id,
            'title' : recipie.title,
            'description'  : recipie.description[:300] + '...',
            'ingredients'  : recipie.ingredients.replace('\n',' ').split(".")[:-1],
            'instructions' : recipie.instructions.replace('\n',' ').split(".")[:-1],
            'category' : recipie.category,
            'created_by' : User.find_user(recipie.created_by)
        })

    all_categories = [ { 'name' : category[0], 'count' : Recipie.get_category_count(category[0])} for category in db.session.query(Recipie.category).distinct().all()]
    print(all_categories)

    return render_template('home.html', recipie_list=all_recipies, category_list=all_categories)

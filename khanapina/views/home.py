from flask import Blueprint, request, render_template, redirect, url_for, flash
from ..models.Recipies import Recipie

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def home_page():
    page_no  = request.args.get('page') or 1
    per_page = request.args.get('per_page') or 15
    all_recipies = Recipie.get_all(page=int(page_no), per_page=int(per_page))
    return render_template('home.html', recipie_list=all_recipies)

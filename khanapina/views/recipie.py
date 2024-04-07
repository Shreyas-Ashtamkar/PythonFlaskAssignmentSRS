from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from ..models.Recipies import Recipie
from ..models.Users import User
from ..forms import Recipies
from ..utils import dbutils

db = dbutils.get_db()

bp = Blueprint('recipie', __name__, url_prefix='/recipie')

@bp.route('/new', methods=('GET', 'POST'))
@login_required
def new_recipie():
    new_recipie_form = Recipies.CreateRecipie()
    response = render_template('recipie/new.html', form=new_recipie_form)

    if request.method == 'POST' and new_recipie_form.validate_on_submit():
        title = new_recipie_form.title.data
        description = new_recipie_form.description.data
        ingredients = new_recipie_form.ingredients.data
        instructions = new_recipie_form.instructions.data
        category = new_recipie_form.category.data
        new_recipie = Recipie(
            title, 
            description, 
            ingredients, 
            instructions,
            current_user.id,
            category
        )
        db.session.add(new_recipie)
        db.session.commit()
        return redirect(url_for('recipie.view_recipie', id=new_recipie.id))
    
    
    return response

@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit_recipie(id):
    recipie = Recipie.find_by_id(id)
    edit_recipie_form = Recipies.CreateRecipie(obj=recipie)
    response = render_template('recipie/edit.html', form=edit_recipie_form)
    if request.method == 'POST' and edit_recipie_form.validate_on_submit():
        recipie.title = edit_recipie_form.title.data
        recipie.description = edit_recipie_form.description.data
        recipie.ingredients = edit_recipie_form.ingredients.data
        recipie.instructions = edit_recipie_form.instructions.data
        
        db.session.add(recipie)
        db.session.commit()
        return redirect(url_for('recipie.view_recipie', id=id))
    return response

@bp.route('/<int:id>/delete', methods=('GET', 'POST'))
@login_required
def delete_recipie(id):
    recipie = Recipie.find_by_id(id)
    if request.method == 'POST':
        db.session.delete(recipie)
        db.session.commit()
        return redirect(url_for('home.home'))
    return render_template('recipie/delete.html', recipie=recipie)

@bp.route('/<int:id>', methods=('GET',))
def view_recipie(id):
    recipie = Recipie.find_by_id(id)
    recipie_chef = User.find_user(recipie.created_by)
    
    recipie = {
        'title' : recipie.title,
        'description'  : recipie.description,
        'ingredients'  : recipie.ingredients.replace('\n',' ').split(".")[:-1],
        'instructions' : recipie.instructions.replace('\n',' ').split(".")[:-1],
        'category' : recipie.category,
        'user' : recipie_chef
    }
    
    return render_template('recipie/details.html', recipie = recipie)

import click
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_db() -> SQLAlchemy:
    return db

def init_db():
    db = get_db()
    db.create_all()
    
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    db = get_db()
    db.init_app(app)
    app.cli.add_command(init_db_command)

from ..utils import dbutils

db = dbutils.get_db()

class Recipie(db.Model):
    __tablename__ = "Recipies"
    
    id      = db.Column(db.Integer, primary_key=True)
    title   = db.Column(db.String(100), nullable=False)
    description   = db.Column(db.String(1500))
    ingredients   = db.Column(db.String(1000))
    instructions  = db.Column(db.String(2000))
    category      = db.Column(db.String(50))
    created_by    = db.Column(db.Integer, db.ForeignKey('Users.id'))
    
    def __init__(self, title, description, ingredients, instructions, user, category="Lunch"):
        self.title          = title
        self.description    = description
        self.ingredients    = ingredients
        self.instructions   = instructions
        self.category       = category
        self.created_by     = user
    
    def __str__(self) -> str:
        return self.title
    
    @staticmethod
    def find_by_id(rid):
        return Recipie.query.get(rid)
    
    @staticmethod
    def find_by_user(uid):
        return Recipie.query.filter_by(created_by=uid).all()
    
    @staticmethod
    def get_all(page=1, per_page=10):
        return Recipie.query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_categories():
        return Recipie.query.distinct(Recipie.category).all()
    
    @staticmethod
    def get_category_count(category=None):
        return Recipie.query.filter_by(category=category).count()

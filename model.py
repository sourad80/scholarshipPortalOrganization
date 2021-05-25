from app import db,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_student(user_id):
    return Organization.query.get(int(user_id))

class Student(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(13), unique=True, nullable=False)
    address = db.Column(db.String(120))
    income = db.Column(db.Float)
    clx = db.Column(db.String(120))
    clxmarks = db.Column(db.Float)
    clxii = db.Column(db.String(120))
    clxiimarks = db.Column(db.Float,default = 0.0)
    ug = db.Column(db.String(120))
    ugmarks = db.Column(db.Float,default = 0.0)
    pg = db.Column(db.String(120))
    pgmarks = db.Column(db.Float,default = 0.0,nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Student('{self.username}', '{self.email}')"

class Organization(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(13), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    scholarships = db.relationship('Scholarship', backref='organization', lazy=True)

    def __repr__(self):
        return f"Organization('{self.username}', '{self.email}')"

class Scholarship(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(256))
    amount= db.Column(db.Float)
    cls_x_min_per = db.Column(db.Float)
    cls_xii_min_per = db.Column(db.Float)
    cls_ug_min_per = db.Column(db.Float)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)

    def __repr__(self):
        return f"Scholarship('{self.name}', '{self.organization_id}')"

'''

scholarship = Scholarships.query.filter_by(id=form.id.data).first()
print(scholarship.organization.username)

scholarship = Scholarship(...., organization_id=current_user.id)

'''

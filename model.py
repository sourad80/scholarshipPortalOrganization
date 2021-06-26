from app import db,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_student(user_id):
    return Student.query.get(int(user_id))

class Student(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
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
    applications = db.relationship('scholarship_application', backref='student', lazy=True)

    def __repr__(self):
        return f"Student('{self.username}', '{self.email}')"

class Organization(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(13), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    scholarships = db.relationship('Scholarship', backref='organization', lazy=True)

    def __repr__(self):
        return f"Organization('{self.username}', '{self.email}')"

class Scholarship(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(256))
    amount= db.Column(db.Float)
    cls_x_min_per = db.Column(db.Float)
    cls_xii_min_per = db.Column(db.Float)
    cls_ug_min_per = db.Column(db.Float)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    life = db.Column(db.Integer, default=1)
    datetime = db.Column(db.DateTime, default=datetime.utcnow())
    applications = db.relationship('scholarship_application', backref='scholarship', lazy=True)

    def __repr__(self):
        return f"Scholarship('{self.name}', '{self.organization_id}','{self.description}','{self.cls_x_min_per}','{self.cls_xii_min_per}','{self.cls_ug_min_per}')"

class scholarship_application(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sch_id = db.Column(db.Integer, db.ForeignKey('scholarship.id'), nullable=False)
    stu_id = db.Column(db.Integer, db.ForeignKey('student.id'),nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow())
    status = db.Column(db.Integer,nullable=False)
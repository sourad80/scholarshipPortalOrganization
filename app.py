from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '4b95e49882f86d7397154c929806fe8d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://qrtggwfmstohzl:0a89cf8c918a805453e847147c36aef4fa1206930dbd23038baaa4340ead05e0@ec2-54-211-77-238.compute-1.amazonaws.com:5432/d4h9o0dgsuo00j'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

from routes import *

if __name__=='__main__':
    db.create_all()
    app.run(debug=True) 
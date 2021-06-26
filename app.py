from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '4b95e49882f86d7397154c929806fe8d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://daojhkswkkktev:d600ab2bc360d7cf93951b69fa4dcddd4a227db14796bc7e9b52cd2c66a9b0ac@ec2-52-5-247-46.compute-1.amazonaws.com:5432/d66fcb0i0tt3uf'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from routes import *

if __name__=='__main__':
    db.create_all()
    app.run(debug=True) 

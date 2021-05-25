from flask_login.utils import logout_user
from app import app,db,bcrypt
from flask import render_template,redirect,flash,url_for,request
from forms import OrgRegistration,OrgLogin
from model import Organization, Student
from flask_login import login_user,current_user,login_required

@app.route('/',methods=['POST','GET'])
def home():
    if current_user.is_authenticated:
        flash(f'Already loged in', 'success')
        return redirect(url_for('dashboard'))
    form = OrgRegistration()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('Utf-8')
        print(hashed_password)
        organization = Organization(username = form.name.data, email = form.email.data, phone = form.phone.data ,password = hashed_password )
        db.session.add(organization)
        db.session.commit()
        flash(f'Created New Account.Check Your Registered mail for more details!!', 'success')
        return redirect(url_for('login'))

    return render_template("home.html", title="Home",form = form)

@app.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        flash(f'Already loged in', 'success')
        return redirect(url_for('dashboard'))
    form = OrgLogin()
    if form.validate_on_submit():
        user = Organization.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data ):
            login_user(user,remember=form.remember.data)
            flash(f'Logged In', 'success')
            return redirect(url_for('dashboard'))
        flash(f'Login Unsuccessfull, Please Check Email and Password!!!', 'danger')
        return redirect(url_for('login'))
    return render_template("login.html", title="Login",form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'Successfully Loggeout User','info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title = "Welcome"+current_user.username)
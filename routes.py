from flask_login.utils import logout_user
from werkzeug.exceptions import abort
from app import app,db,bcrypt
from flask import render_template,redirect,flash,url_for,request
from forms import OrgRegistration,OrgLogin,AddSch,UpdateSch
from model import Organization, Student,Scholarship,scholarship_application
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

@app.route('/addSch',methods=['POST','GET'])
@login_required
def add_sch():
    form=AddSch()
    if form.validate_on_submit():
        scholarship = Scholarship(name = form.name.data,description=form.description.data,amount=form.amount.data,cls_x_min_per=form.cls_x_min_per.data,cls_xii_min_per=form.cls_xii_min_per.data,cls_ug_min_per=form.cls_ug_min_per.data,organization_id=current_user.id )
        db.session.add(scholarship)
        db.session.commit()
        flash(f'Created New Scholarship', 'success')
        return redirect(url_for('dashboard'))
    return render_template('schAdd.html', title = "Welcome"+current_user.username,form = form)

@app.route('/updateSch/<id>',methods=['POST','GET'])
@login_required
def update_sch_id(id):
    form=UpdateSch()
    scholarship = Scholarship.query.filter_by(id=id).first()
    if form.validate_on_submit():
            scholarship.name = form.name.data
            scholarship.amount = form.amount.data
            scholarship.cls_x_min_per = form.cls_x_min_per.data
            scholarship.cls_xii_min_per = form.cls_xii_min_per.data
            scholarship.cls_ug_min_per = form.cls_ug_min_per.data
            scholarship.description = form.description.data
            db.session.commit()
            flash(f'Scholarship Updated Successfully!!', 'success')
            return redirect(url_for('dashboard'))
    elif request.method == 'GET':
            form.name.data = scholarship.name
            form.amount.data = scholarship.amount
            form.cls_x_min_per.data = scholarship.cls_x_min_per
            form.cls_xii_min_per.data = scholarship.cls_xii_min_per
            form.cls_ug_min_per.data = scholarship.cls_ug_min_per
            form.description.data = scholarship.description

            return render_template("schUpdate.html", title="SchUpdate",form = form)

@app.route('/updateSch',methods=['POST','GET'])
@login_required
def update_sch():
    scholarships = Scholarship.query.filter_by(organization_id=current_user.id)
    return render_template('viewUpdateScholarship.html',title="Your Scholarships",scholarships = scholarships)

@app.route('/deleteSch/<id>',methods=['POST','GET'])
@login_required
def delete_sch_id(id):
    scholarship = Scholarship.query.get_or_404(id)
    if scholarship.organization_id != current_user.id:
        abort(404)
    else:
        db.session.delete(scholarship)
        db.session.commit()
    flash(f'Scholarship Deleted Successfully!!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/deleteSch',methods=['POST','GET'])
@login_required
def delete_sch():
    scholarships = Scholarship.query.filter_by(organization_id=current_user.id)
    return render_template('viewDeleteScholarship.html',title="Your Scholarships",scholarships = scholarships)

@app.route('/viewApplication',methods=['POST','GET'])
@login_required
def view_application():
    scholarships = Scholarship.query.filter_by(organization_id=current_user.id)
    return render_template('viewApplication.html',title="Your Scholarships",scholarships = scholarships)

@app.route('/viewApplication/<id>',methods=['POST','GET'])
@login_required
def view_application_id(id):
    scholarship_applications = scholarship_application.query.filter_by(sch_id=id)
    return render_template('viewApplicants.html',title="Applicants",scholarship_applications = scholarship_applications)

@app.route('/view_applicant_details/<id>',methods=['POST','GET'])
@login_required
def view_applicant_details_id(id):
    student = Student.query.filter_by(id=id).first()
    return render_template("applicantDetails.html", title="Details",student=student)

@app.route("/grantApplicant/", methods=['POST','GET'])
@login_required
def grantApplicant():
    # TO DO change status
    flash(f'Scholarship Granted Successfully!!', 'success')
    return redirect(url_for('view_application'));

@app.route("/revokeApplicant/", methods=['POST','GET'])
@login_required
def revokeApplicant():
    # TO DO change status
    flash(f'Scholarship Revoked Successfully!!', 'success')
    return redirect(url_for('view_application'));


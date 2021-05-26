from flask_wtf import Form
from flask_wtf.file import FileField,file_allowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from model import Student,Organization,Scholarship
from flask_login import current_user

class OrgRegistration(Form):
    name = StringField('Name', validators = [ DataRequired() , Length(min = 2, max = 25) ])
    email = StringField('Email',validators= [ DataRequired(), Email()])
    phone = StringField('Phone Number',validators= [ DataRequired(), Length(min = 10, max = 13)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,name):
        user = Organization.query.filter_by(name = name.data).first()

        if user:
            raise ValidationError('Name already exist!!')
    
    def validate_email(self,email):
        user = Organization.query.filter_by(email = email.data).first()

        if user:
            raise ValidationError('Emali already exist!!')
    
    def validate_phone(self,phone):
        user = Organization.query.filter_by(phone = phone.data).first()

        if user:
            raise ValidationError('Phone already exist!!')

class OrgLogin(Form):
    email = StringField('Email',validators= [ DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class AddSch(Form):
    name = StringField('Name', validators = [ DataRequired() , Length(min = 2, max = 25) ])
    description = StringField('Description', validators = [ DataRequired() , Length(min = 2, max = 256) ])
    amount= FloatField('Amount',validators=[DataRequired()],default=0.0)
    cls_x_min_per = FloatField('Class X min %',validators=[DataRequired()],default=0.0)
    cls_xii_min_per = FloatField('Class XII min %',validators=[DataRequired()],default=0.0)
    cls_ug_min_per = FloatField('UG min %',validators=[DataRequired()],default=0.0)
    submit = SubmitField('ADD')

    def validate_schname(self,name): #Not working
        scholarship = Scholarship.query.filter_by(name=name.data).first()

        if scholarship:
            raise ValidationError('Scholarship name already exist!!')

class UpdateSch(Form):
    name = StringField('Name', validators = [ DataRequired() , Length(min = 2, max = 25) ])
    description = StringField('Description', validators = [ DataRequired() , Length(min = 2, max = 256) ])
    amount= FloatField('Amount',validators=[DataRequired()],default=0.0)
    cls_x_min_per = FloatField('Class X min %',validators=[DataRequired()],default=0.0)
    cls_xii_min_per = FloatField('Class XII min %',validators=[DataRequired()],default=0.0)
    cls_ug_min_per = FloatField('UG min %',validators=[DataRequired()],default=0.0)
    submit = SubmitField('Update Scholarship')

        # Have to validate

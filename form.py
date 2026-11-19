from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, PasswordField, SubmitField,SelectField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from datetime import datetime
class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=5,max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=8,max=20)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password',
                                                            message='Passwords must match')])                            
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')   

class ExpenseForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired(), Length(max=100)])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be greater than zero")])
    category = SelectField('Category', choices=[('Food', 'Food'), ('Transportation', 'Transportation'), ('Entertainment', 'Entertainment')], validators=[DataRequired()])
    date = DateField('Date', default=datetime.today, format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Expense')
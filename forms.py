from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FormField, FieldList
from wtforms.validators import DataRequired, Length, Email, EqualTo
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
class ExpenseForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    income_limit = StringField('Income Limit')
    submit = SubmitField('Add Expense')
class IncomeForm(FlaskForm):
    amount = FieldList(FormField(ExpenseForm), min_entries=1)
    submit = SubmitField('Add Income')
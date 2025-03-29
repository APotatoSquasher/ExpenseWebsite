from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db, login_manager
from models import User, Expense
from forms import RegistrationForm, LoginForm, ExpenseForm, IncomeForm
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
@app.route('/')
def home():
    return render_template('home.html')
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
from forms import *
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in!', 'danger')
        print("User is already logged in")
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        form.username.data = ''
        form.email.data = ''
        form.password.data = ''
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    else:
        print("The form is not valid")
        return render_template('register.html', title='Home',form=form)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            #next_page = request.args.get('next')
            print("Logged in user:", user.username)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return render_template('login.html', title='Login', form=form)
    else:
        return render_template('login.html', title='Login', form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
@app.route('/dashboard',methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(name=form.name.data, amount=form.amount.data, date=form.date.data, user_id=current_user.id)
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('dashboard'))
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    render_template('dashboard.html', title='Dashboard', expenses=expenses, form=form)
@app.route('/delete_expense/<int:expense_id>', methods=['GET','POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        abort(403)
    else:
        db.session.delete(expense)
        db.session.commit()
        flash('Expense deleted successfully!', 'success')
        return redirect(url_for('home'))
@app.route('/expenses',methods=['GET', 'POST'])
@login_required
def expenses():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    total_expenses = sum(expense.amount for expense in expenses)
    return render_template('expenses.html', expenses=expenses,total_expenses=total_expenses)
@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    income_limits = Expense.query.filter_by(user_id=current_user.id).all()
    DictofCateogries={}
    #ListofValues=[]
    for income in income_limits:
        if income.category not in DictofCateogries:
            DictofCateogries.update({income.category:float(income.income_limit)})
    print(DictofCateogries)
    form = ExpenseForm()
    if form.validate_on_submit():
        if form.income_limit.data == '' and form.category.data in DictofCateogries:
            expense = Expense(description=form.description.data, amount=form.amount.data, user_id=current_user.id, category=form.category.data.capitalize(),income_limit=DictofCateogries[form.category.data])
        else:
            expense = Expense(description=form.description.data, amount=form.amount.data, user_id=current_user.id, category=form.category.data.capitalize(),income_limit=form.income_limit.data)
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
    return render_template('add_expense.html', form=form, income_limits=DictofCateogries)
@app.route('/add_income', methods=['GET', 'POST'])
@login_required
def add_income():
    income_limits = Expense.query.filter_by(user_id=current_user.id).all()
    SetofCateogries=set()
    for income in income_limits:
        SetofCateogries.add(income.category)
    print(SetofCateogries)
    SetofCateogries=list(SetofCateogries)
    #categories = income_limits.query.filter_by(Expense.category).first()
    if not income_limits:
        flash('You have not set any expensess yet. Please add some expenses', 'danger')
        return redirect(url_for('add_expense'))
    ListofForms=[]
    for category in SetofCateogries:
        form = IncomeForm()
        ListofForms.append(form)
    #print(ListofForms[1].amount.data)
    print(ListofForms)
    form = IncomeForm()
    if form.validate_on_submit():
        for item in form.amount.data:
            print(f"Item: {item['category']}, Amount: {item['amount']}")
    #for form0 in ListofForms:
        #print(form0.amount.data)
    #for item in SetofCateogries:
       # form = IncomeForm(prefix=item)
       # if form.validate_on_submit():
         #   print(f"Form submitted for category: {item}, included amount: {form.amount.data}")
            #return redirect(url_for('expenses'))
        #else:
           # print(f"Form not submitted for category: {item}, nor for amount: {form.amount.data}")
            #return redirect(url_for('add_income'))
    return render_template('add_income.html',income_limits=SetofCateogries,form=form,db=db,forms=ListofForms)
        #if ListofForms.validate_on_submit():
          #  print(form0.amount.data)
          #  print(ListofForms[1].amount.data)
          #  if ListofForms[len(ListofForms)-1].validate_on_submit():
          #      return redirect(url_for('expenses'))
          #  else:
          #      return render_template('add_income.html',income_limits=SetofCateogries,form=form,db=db,forms=ListofForms)
        #else:
          #  return render_template('add_income.html',income_limits=SetofCateogries,form=form,db=db,forms=ListofForms)
@app.route('/update_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def update_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        abort(403)
    form = ExpenseForm()
    if form.validate_on_submit():
        expense.description = form.description.data
        expense.amount = form.amount.data
        expense.category = form.category.data
        expense.income_limit = form.income_limit.data
        income_limits = Expense.query.filter_by(user_id=current_user.id).all()
        for income in income_limits:
            if income.category == expense.category:
                income.income_limit = expense.income_limit # Changes the income limit of every line in the category
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('expenses'))
    else:
        return render_template('update_expense.html', form=form, expense=expense)
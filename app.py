from flask import Flask, render_template, request, url_for, redirect,flash,session
from datetime import datetime
from form import RegisterForm, LoginForm, ExpenseForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

import form


app = Flask(__name__)
app.config['SECRET_KEY'] = "b1e51b4cbec18e2f2687711c5f0c1cc229aaef00ca772e41196effe61f539cd1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy=True)
    def __str__(self):
        return f"<User {self.username}>"


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.today)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return f"<Expense {self.description}, Amount: {self.amount}, Category: {self.category}, Date: {self.date}>"



def set_password(self, password):
        self.password_hash = generate_password_hash(password)

def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def check_login():
    if session.get('user_id'):
        return True
    else:
        return False


# home page route
@app.route('/')
def home():
    flash('Welcome to the Expense Tracker App!', 'success')
    return render_template('home.html')


# dashboard route
@app.route('/dashboard')
def dashboard():

    if not check_login():
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    total = 0
    current_user = session['user_id']
    user_expenses = Expense.query.filter_by(user_id=current_user).all()
    for expense in user_expenses:
        total += expense.amount

    transaction_count = len(user_expenses)
    categories= []
    breakdown = {}

    for expense in user_expenses:
        categories.append(expense.category)

        if expense.category in breakdown:
            breakdown[expense.category] += expense.amount
        else:
            breakdown[expense.category] = expense.amount

    n_categories = len(breakdown)

    return render_template(
        'dashboard.html',
        total=total,
        transaction_count=transaction_count,
        n_categories=n_categories,
        breakdown=breakdown)


# Expense route
@app.route('/expense')
def expense():

    if check_login():
        current_user = session['user_id']
        user_expenses = Expense.query.filter_by(user_id=current_user).order_by(Expense.date.desc()).all()
        flash('Please log in to access the expense page.', 'warning')
        return render_template('expense.html', expenses=user_expenses)
    else:
        flash('Please log in to access the expense page.', 'warning')
        return redirect(url_for('login'))

    
# add expense route
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if check_login():
       form = ExpenseForm()
       if form.validate_on_submit():
           description = form.description.data
           amount = form.amount.data
           category = form.category.data
           date = form.date.data

           current_user = session['user_id']
           new_expense = Expense(description=description, amount=amount, category=category, date=date, user_id=current_user)
           db.session.add(new_expense)
           db.session.commit()

           flash(f'Expense added: {description}, Amount: {amount}, Category: {category}', 'success')
           return redirect(url_for('expense'))

    return render_template('add_expense.html', form=form)


# view an single expense route
@app.route('/expense/<int:expense_id>', methods=['GET'])
def view_expense(expense_id):
    if check_login():
        expense = Expense.query.get_or_404(expense_id)
        if expense.user_id == session['user_id']:
            return render_template('single_expense.html', expense=expense)
        else:
            flash('You are not the owner of this expense.', 'warning')
            return redirect(url_for('expense'))
    else:
        flash('Please log in to view the expense details.', 'warning')
        return redirect(url_for('login'))

# delete expense route
@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):

    if not check_login():
        flash('Please log in to delete expenses.', 'warning')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    for expense in user.expenses:
        if expense.id == expense_id:
            db.session.delete(expense)
            db.session.commit()
            flash('Expense deleted successfully!', 'success')
            break
    else:
        flash('Expense not found.', 'danger')
    return redirect(url_for('expense'))


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Check if email already exists
        existing_email = User.query.filter_by(email=email).first()

        if existing_email:
            flash('Email already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        # Check if username already exists
        existing_username = User.query.filter_by(username=username).first()

        if existing_username:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        # Create new user
        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        # Save user to database
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {username}!', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        entered_email = form.email.data
        entered_password = form.password.data


        existing_user = User.query.filter_by(email=entered_email).first()
        if existing_user and check_password_hash(existing_user.password, entered_password):
            session['user_id'] = existing_user.id
            session['username'] = existing_user.username
            flash(f'Welcome back, {existing_user.username}!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)


# logout route
@app.route('/logout', methods=['GET', 'POST'])
def logout():

    if request.method == 'POST':
        session.clear()

        flash('You have been logged out.', 'success')

        return redirect(url_for('home'))

    return render_template('logout.html')


if __name__ == '__main__':
    app.run(debug=True)
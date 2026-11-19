from flask import Flask, render_template, request, url_for, redirect,flash,session
from datetime import datetime
from form import RegisterForm, LoginForm, ExpenseForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = "b1e51b4cbec18e2f2687711c5f0c1cc229aaef00ca772e41196effe61f539cd1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

user_data = [
    {
        "id": 1,
        "description": "Rice",
        "amount": 60,
        "category": "Grains",
        "date": "2026-11-01"
    },
    {
        "id": 2,
        "description": "Milk",
        "amount": 30,
        "category": "Dairy",
        "date": "2026-11-02"
    },
    {
        "id": 3,
        "description": "Sugar",
        "amount": 45,
        "category": "Essentials",
        "date": "2026-11-03"
    },
    {
        "id": 4,
        "description": "Cooking Oil",
        "amount": 150,
        "category": "Cooking Essentials",
        "date": "2026-11-04"
    },
    {
        "id": 5,
        "description": "Potato",
        "amount": 30,
        "category": "Vegetables",
        "date": "2026-11-05"
    }
]
user = []

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


# Expense route
@app.route('/expense')
def expense():

    if not check_login():
        flash('Please log in to access the expense page.', 'warning')
        return redirect(url_for('login'))
    
    return render_template('expense.html', expenses=user_data)


# dashboard route
@app.route('/dashboard')
def dashboard():

    if not check_login():
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    total = 0

    for expense in user_data:
        total += expense['amount']

    transaction_count = len(user_data)

    breakdown = {}

    for expense in user_data:
        category = expense['category']

        if category in breakdown:
            breakdown[category] += expense['amount']
        else:
            breakdown[category] = expense['amount']

    n_categories = len(breakdown)

    return render_template(
        'dashboard.html',
        total=total,
        transaction_count=transaction_count,
        n_categories=n_categories,
        breakdown=breakdown
    )


# add expense route
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if not check_login():
        flash('Please log in to add an expense.', 'warning')
        return redirect(url_for('login'))
    form = ExpenseForm()
    if form.validate_on_submit():
        description = form.description.data
        amount = form.amount.data
        category = form.category.data

        # todo : save to db
        flash(f'Expense added: {description}, Amount: {amount}, Category: {category}', 'success')
        return redirect(url_for('expense'))

    return render_template('add_expense.html', form=form)


# view expense route
@app.route('/expense/<int:expense_id>', methods=['GET'])
def view_expense(expense_id):

    expense = None

    for item in user_data:
        if item['id'] == expense_id:
            expense = item
            break

    if expense is None:
        return "Expense not found", 404

    return render_template('view_expense.html', expense=expense)


# delete expense route
@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):

    if not check_login():
        flash('Please log in to delete expenses.', 'warning')
        return redirect(url_for('login'))

    for expense in user_data:
        if expense['id'] == expense_id:
            user_data.remove(expense)
            flash('Expense deleted successfully!', 'success')
            break
    else:
        flash('Expense not found.', 'danger')

    return redirect(url_for('expense'))


# register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
       username = form.username.data
       email = form.email.data
       password = form.password.data


       for existing_user in user:
              if existing_user['email'] == email:
                flash('Email already exists. Please choose a different one.')
                return redirect(url_for('register'))
              if existing_user['username'] == username:
                flash('Username already exists. Please choose a different one.')
                return redirect(url_for('register'))

              
       user_details = {'id': len(user) + 1, 'username': username, 
                       'email': email, 'password': generate_password_hash(password)}
       user.append(user_details)

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

        for existing_user in user:
            if existing_user['email'] == entered_email and check_password_hash(existing_user['password'], entered_password):
                session['user_id'] = existing_user['id']
                session['username'] = existing_user['username']
                flash(f'Welcome back, {existing_user["username"]}!', 'success')
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
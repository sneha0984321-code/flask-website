from flask import Flask, url_for ,redirect

app = Flask(__name__)

@app.route('/home')
def home():
    return "<h1>Home</h1>"

with app.test_request_context():
    print(url_for('home'))  # Output: /home


@app.route('/expense/<int:expense_id>')
def expense_details(expense_id):
    return f"Viewing Expense {expense_id}"

with app.test_request_context():
    gen_url = url_for('expense_details', expense_id = 7)  # Output: /expense/7
    print(gen_url)

@app.route('/user/<string:username>/expense/<int:expense_id>')
def user_expense(username, expense_id):
   pass

with app.test_request_context():
    gen_url = url_for('user_expense', username='john', expense_id=42)  # Output: /user/john/expense/42
    print(gen_url)

@app.route('/expenses/<int:expense_id>/delete', methods=['POST'])
def delete_expense(expense_id):
    # Logic to delete the expense with the given expense_id
    return redirect(url_for('home'))
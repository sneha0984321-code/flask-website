from flask import Flask,jsonify

app = Flask(__name__)

@app.route('/ping')
def ping():
    return "pong"

@app.route('/api/summary')
def summary():
    return jsonify({
        "total_expenses": 1000 ,
        "currency": "INR"
    })
@app.route('/not-found')
def not_found():
    return jsonify({
        "error": "Resource not found"
    }), 404

if __name__ == '__main__':
    app.run(debug=True)
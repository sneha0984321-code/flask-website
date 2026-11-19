"""
This code will have the tables defines as models 
run it once
"""

from app import app,db
with app.app_context():
    db.create_all()

print("Tables created successfully")

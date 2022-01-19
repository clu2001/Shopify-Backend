from flask import Flask
from InventoryModel import database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///InventoryDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database.init_app(app)

@app.before_first_request
def create_table():
    database.create_all()


app.run(host="localhost", port=5000)


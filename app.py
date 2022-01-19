from flask import Flask, request, render_template, redirect
from InventoryModel import database, InventoryModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///InventoryDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database.init_app(app)

@app.before_first_request
def create_table():
    database.create_all()

@app.route('/data/create', methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
 
    if request.method == 'POST':
        inventory_id = request.form['inventory_id']
        item_name = request.form['item_name']
        employee = InventoryModel(inventory_id=inventory_id, item_name=item_name)
        database.session.add(employee)
        database.session.commit()
        return redirect('/data')

app.run(host="localhost", port=5000)


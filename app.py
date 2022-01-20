from flask import Flask, request, render_template, redirect, abort, Response
from InventoryModel import database, InventoryModel
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///InventoryDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database.init_app(app)

@app.before_first_request
def create_table():
    database.create_all()

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/data/create', methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
 
    if request.method == 'POST':
        inventory_id = request.form['inventory_id']
        item_name = request.form['item_name']
        inventory = InventoryModel(inventory_id=inventory_id, item_name=item_name)
        database.session.add(inventory)
        database.session.commit()
        return redirect('/data')

@app.route('/data')
def RetrieveDataList():
    inventory = InventoryModel.query.all()
    return render_template('datalist.html', inventory = inventory)

@app.route('/data/update', methods = ['GET','POST'])
def update():
    if request.method == 'POST':
        inventory_id = request.form['inventory_id']
        inventory = InventoryModel.query.filter_by(inventory_id=inventory_id).first()
        if inventory:
            database.session.delete(inventory)
            database.session.commit()
 
            item_name = request.form['item_name']
            inventory = InventoryModel(inventory_id=inventory_id, item_name=item_name)
 
            database.session.add(inventory)
            database.session.commit()
            return redirect(f'/data')
        return f"Inventory with id: {inventory_id} does not exist :("
    return render_template('createpage.html')

@app.route('/data/delete', methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        inventory_id = request.form['inventory_id']
        inventory = InventoryModel.query.filter_by(inventory_id=inventory_id).first()
        if inventory:
            database.session.delete(inventory)
            database.session.commit()
            return redirect('/data')
        abort(404)
    return render_template('createpage.html')

@app.route('/download')
def download():
	return render_template('download.html')

@app.route('/download/report/csv')
def download_report():
    with open('InventoryModel.csv', 'w') as outfile: 

        writer = csv.writer(outfile)
        records = InventoryModel.query.all()
        for item in records:
            writer.writerow([item])
    
    return Response(outfile, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=InventoryModel.csv"})

app.run(host="localhost", port=5000)


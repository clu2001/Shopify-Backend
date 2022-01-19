from flask import Flask, request, render_template, redirect, abort, Response
from InventoryModel import database, InventoryModel
import io
import csv

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
        inventory = InventoryModel(inventory_id=inventory_id, item_name=item_name)
        database.session.add(inventory)
        database.session.commit()
        return redirect('/data')

@app.route('/data')
def RetrieveDataList():
    inventory = InventoryModel.query.all()
    return render_template('datalist.html', inventory = inventory)

@app.route('/data/<int:id>/update',methods = ['GET','POST'])
def update(inventory_id):
    inventory = InventoryModel.query.filter_by(inventory_id=inventory_id).first()
    if request.method == 'POST':
        if inventory:
            database.session.delete(inventory)
            database.session.commit()
 
            item_name = request.form['item_name']
            inventory = InventoryModel(inventory_id=inventory_id, item_name=item_name)
 
            database.session.add(inventory)
            database.session.commit()
            return redirect(f'/data/{inventory_id}')
        return f"Inventory with id: {inventory_id} does not exist :("
 
    return render_template('update.html', inventory = inventory)

@app.route('/data/<int:id>/delete', methods=['GET','POST'])
def delete(inventory_id):
    inventory = InventoryModel.query.filter_by(inventory_id=inventory_id).first()
    if request.method == 'POST':
        if inventory:
            database.session.delete(inventory)
            database.session.commit()
            return redirect('/data')
        abort(404)
    return render_template('delete.html')

@app.route('/download')
def download():
	return render_template('download.html')

@app.route('/download/report/csv')
def download_report():
    outfile = open('InventoryModel.csv', 'w')
    outcsv = csv.writer(outfile)
    records = database.session.query(InventoryModel).all()
    
    for item in records: 
        outcsv.writerow([item.inventory_id, item.item_name])

    outfile.close()
    return Response(outfile, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=Inventory.csv"})

app.run(host="localhost", port=5000)


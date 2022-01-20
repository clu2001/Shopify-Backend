from flask import Flask, request, render_template, redirect, abort, Response
from InventoryModel import database, InventoryModel
import csv

# we create a flask object and name it app 
app = Flask(__name__)
# we will configure the SQLite connection with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///InventoryDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database.init_app(app)

# we need to link the database instance from InventoryModel.py and create the database 
# file before the user accesses the server 
@app.before_first_request
def create_table():
    database.create_all()

# we will serve a default home page by rendering homepage.html using flask's render_template 
# method 
@app.route('/')
def home():
    return render_template('homepage.html')

# this will be our Create View 
# when a client goes to this page (which is the GET method), we will display a form
# so that we can input data into the database 
# on submission of the form (which is the POST method), we will save the input data
# in the InventoryModel database 
@app.route('/data/create', methods = ['GET','POST'])
def create():
    # if it is GET request, return html page displaying form
    if request.method == 'GET':
        return render_template('createpage.html')
    # if it is a POST request, we will take the input inventory_id and item_name 
    # fields
    if request.method == 'POST':
        inventory_id = request.form['inventory_id']
        item_name = request.form['item_name']
        # add it to these two fields into our InventoryModel
        inventory = InventoryModel(inventory_id=inventory_id, item_name=item_name)
        database.session.add(inventory)
        # save the change to the database 
        database.session.commit()
        # redirect to the page where it lists out data in the inventory 
        return redirect('/data')

# this is the Retrive view where we will view a list of the current items in the inventory
@app.route('/data')
def RetrieveDataList():
    inventory = InventoryModel.query.all()
    return render_template('datalist.html', inventory = inventory)

# this is the Update view where we can update current items in the inventory 
# with new data submitted by the user 
@app.route('/data/update', methods = ['GET','POST'])
def update():
    # if it is a POST method, we will request the inventory id and search for the item
    if request.method == 'POST':
        inventory_id = request.form['inventory_id']
        inventory = InventoryModel.query.filter_by(inventory_id=inventory_id).first()
        # if the item is found, we will delete it from our inventory, save the changes 
        # in the database, and then request for a new item name 
        if inventory:
            database.session.delete(inventory)
            database.session.commit()
 
            item_name = request.form['item_name']
            inventory = InventoryModel(inventory_id=inventory_id, item_name=item_name)
            # the new item name will be added to the database and saved 
            database.session.add(inventory)
            database.session.commit()
            return redirect(f'/data')
        # if the inventory is not found, then the item does not exist 
        return f"Inventory with id: {inventory_id} does not exist :("
    return render_template('createpage.html')


# this is the Delete view where we can delete items from the inventory 
@app.route('/data/delete', methods=['GET','POST'])
def delete():
    # if POST method, we will request for the inventory id to be deleted 
    if request.method == 'POST':
        inventory_id = request.form['inventory_id']
        inventory = InventoryModel.query.filter_by(inventory_id=inventory_id).first()
        # if the inventory exists, then we will delete it from the database and save the 
        # changes to the data base
        # then the user will be redirected to the page where the current inventory will
        # be displayed 
        if inventory:
            database.session.delete(inventory)
            database.session.commit()
            return redirect('/data')
        # if the inventory does not exist, then an error will be thrown 
        abort(404)
    return render_template('createpage.html')

# this is the Download view, where we will display an option to download the inventory 
# as a CSV file 
@app.route('/download')
def download():
	return render_template('download.html')

# this function is called when the user presses the button that allows him to 
# download the inventory as a CSV file 
@app.route('/download/report/csv')
def download_report():
    # we will open a new CSV file called InventoryModel.csv, and open it in write mode
    with open('InventoryModel.csv', 'w') as outfile: 

        writer = csv.writer(outfile)
        # we will select all the values currently stored in our database, and 
        # write them one by one into the CSV file 
        records = InventoryModel.query.all()
        for item in records:
            writer.writerow([item])
    # after, we will send a response which prompts the user to download the CSV file 
    return Response(outfile, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=InventoryModel.csv"})

# we will be serving this app on port 5000 on localhost 
app.run(host="localhost", port=5000)


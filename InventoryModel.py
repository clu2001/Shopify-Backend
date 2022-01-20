from flask_sqlalchemy import SQLAlchemy

# first, we connect SQLAlchemy
database = SQLAlchemy()

# we create a Model class which will represent a table in a database
# this will contain information regarding our table structure 
class InventoryModel(database.Model):
    
    # name of the table will be called Inventory
    __tablename__ = "Inventory"
 
    # id of the database
    id = database.Column(database.Integer, primary_key=True)
    # id of the inventory 
    inventory_id = database.Column(database.Integer())
    # id of item name 
    item_name = database.Column(database.String())
 
    def __init__(self, inventory_id,item_name):
        self.inventory_id = inventory_id
        self.item_name = item_name
 
    def __repr__(self):
        return f"{self.item_name}:{self.inventory_id}"

from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

class InventoryModel(database.Model):
    
    __tablename__ = "Inventory"
 
    id = database.Column(database.Integer, primary_key=True)
    inventory_id = database.Column(database.Integer(),unique = True)
    item_name = database.Column(database.String())
 
    def __init__(self, inventory_id,item_name,age,position):
        self.inventory_id = inventory_id
        self.item_name = item_name
 
    def __repr__(self):
        return f"{self.item_name}:{self.inventory_id}"

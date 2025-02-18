import random
import string
from datetime import datetime
from app.extensions import db
from sqlalchemy import Enum

class Borrowing(db.Model):
    __tablename__ = 'borrowings'

    id = db.Column(db.Integer, primary_key=True)
    reference_number = db.Column(db.String(15), unique=True, nullable=False, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False) 
    start_date = db.Column(db.DateTime, default=datetime.utcnow) 
    end_date = db.Column(db.DateTime, nullable=True)  
    quantity = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(Enum("pending", "approved", "cancelled", "done", name="borrow_status"), 
                       default="pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 

    # Relationships
    user = db.relationship('User', backref=db.backref('borrowings', lazy=True))  
    inventory_item = db.relationship('Inventory', backref=db.backref('borrowings', lazy=True))  

    def generate_reference_number(self):
        """Generate a short, unique reference number."""
        date_str = datetime.utcnow().strftime("%y%m%d") 
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) 
        self.reference_number = f"B-{date_str}-{random_str}" 

    def __repr__(self):
        return f"<Borrowing(id={self.id}, reference_number='{self.reference_number}', user_id={self.user_id}, inventory_id={self.inventory_id}, status='{self.status}', quantity={self.quantity}, start_date='{self.start_date}', end_date='{self.end_date}')>"

# Automatically generate reference number before insert
from sqlalchemy.event import listens_for

@listens_for(Borrowing, "before_insert")
def set_reference_number(mapper, connection, target):
    target.generate_reference_number()

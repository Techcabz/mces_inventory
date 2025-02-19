import random
import string
from datetime import datetime
from app.extensions import db
from sqlalchemy import Enum
import uuid

class Borrowing(db.Model):
    __tablename__ = 'borrowings'

    id = db.Column(db.Integer, primary_key=True)
    reference_number = db.Column(db.String(15), unique=True, nullable=False, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False) 
    start_date = db.Column(db.DateTime, default=datetime.utcnow) 
    end_date = db.Column(db.DateTime, nullable=True)  
    quantity = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(Enum("pending", "approved", "cancelled", "completed", name="borrow_status"), 
                       default="pending", nullable=False)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))  
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

    def serialize(self):
        """Serialize the Borrowing object to a dictionary."""
        return {
            "id": self.id,
            "reference_number": self.reference_number,
            "user_id": self.user_id,
            "inventory_id": self.inventory_id,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "quantity": self.quantity,
            "status": self.status,
            "uuid": self.uuid,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user": self.user.serialize() if hasattr(self.user, 'serialize') else None,
            "inventory_item": self.inventory_item.serialize() if hasattr(self.inventory_item, 'serialize') else None,
        }

    def __repr__(self):
        return f"<Borrowing(id={self.id}, reference_number='{self.reference_number}', user_id={self.user_id}, inventory_id={self.inventory_id}, status='{self.status}', quantity={self.quantity}, start_date='{self.start_date}', end_date='{self.end_date}')>"

# Automatically generate reference number before insert
from sqlalchemy.event import listens_for

@listens_for(Borrowing, "before_insert")
def set_reference_number(mapper, connection, target):
    target.generate_reference_number()

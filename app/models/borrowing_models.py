from ..extensions import db
from datetime import datetime

class Borrowing(db.Model):
    __tablename__ = 'borrowings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False) 
    start_date = db.Column(db.DateTime, default=datetime.utcnow) 
    end_date = db.Column(db.DateTime, nullable=True)  
    status = db.Column(db.String(50), default='borrowed')  
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 

    # Relationships
    user = db.relationship('User', backref=db.backref('borrowings', lazy=True))  
    inventory_item = db.relationship('Inventory', backref=db.backref('borrowings', lazy=True)) 

    def __repr__(self):
        return f"<Borrowing {self.id}: User {self.user_id} borrowed {self.inventory_item.name} (Status: {self.status})>"

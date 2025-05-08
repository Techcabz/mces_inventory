from ..extensions import db
from datetime import datetime
from sqlalchemy import Enum
from app.models.category_models import Category
import uuid

class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    inv_tag = db.Column(db.String(120), unique=True, nullable=False)
    title = db.Column(db.String(120), unique=True, nullable=False)
    property_no = db.Column(db.String(255), unique=False, nullable=True)
    date_acquired = db.Column(db.Date, nullable=True)
    cost = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    unit = db.Column(db.String(120), nullable=False, default="pcs")
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))  
    fund_source = db.Column(db.String(255), nullable=True)
    officer = db.Column(db.String(255), nullable=True)
    school = db.Column(db.String(255), nullable=True)
    status = db.Column(Enum("available", "borrowed", "reserved", "damaged", name="inventory_status"), 
                       default="available", nullable=False)
    image = db.Column(db.String(255), nullable=True) 
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)  

    # Relationship to Category
    category = db.relationship('Category', backref=db.backref('inventory_items', lazy=True))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "inv_tag": self.inv_tag,
            "category_id": self.category_id,
            "category": self.category.name if self.category else 'Uncategorized',
            "property_no": self.property_no,
            "date_acquired": self.date_acquired.strftime('%Y-%m-%d') if self.date_acquired else None,
            "cost": float(self.cost),  # Ensure cost is properly serialized
            "unit": self.unit,
            "fund_source": self.fund_source,
            "officer": self.officer, 
            "school": self.school,
            "quantity": self.quantity,
            "status": self.status,
            "image": self.image, 
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __repr__(self):
        return f"<Inventory {self.id}: {self.title}, Quantity: {self.quantity}, Unit: {self.unit}, Cost: {self.cost}, Status: {self.status}, Inv_tag: {self.inv_tag}>"

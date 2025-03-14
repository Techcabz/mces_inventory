from datetime import datetime
from app.extensions import db
from sqlalchemy import Enum




class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(Enum("pending", "completed", name="cart_status"), default="pending", nullable=False)

    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    inventory_item = db.relationship('Inventory', backref=db.backref('cart_items', lazy=True))

from app.extensions import db
from datetime import datetime

class BorrowedItemStatus(db.Model):
    __tablename__ = 'borrowed_item_status'

    id = db.Column(db.Integer, primary_key=True)
    borrowing_id = db.Column(db.Integer, db.ForeignKey('borrowings.id', ondelete='CASCADE'), nullable=False)
    inventory_item_id = db.Column(db.Integer, db.ForeignKey('inventory.id', ondelete='SET NULL'))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    is_returned = db.Column(db.Boolean, default=False)
    return_date = db.Column(db.DateTime, nullable=True)

    # Optional: Track who marked it as returned
    marked_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    borrowing = db.relationship('Borrowing', backref='item_statuses')
    inventory_item = db.relationship('Inventory', backref='borrowed_statuses')
    marked_by = db.relationship('User', foreign_keys=[marked_by_id])

    def __repr__(self):
        return f"<BorrowedItemStatus item={self.inventory_item_id} returned={self.is_returned}>"

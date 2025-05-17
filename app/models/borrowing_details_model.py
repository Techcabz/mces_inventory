from app.extensions import db
from datetime import datetime


class BorrowingDetails(db.Model):
    __tablename__ = 'borrowing_details'

    id = db.Column(db.Integer, primary_key=True)
    borrowing_id = db.Column(
        db.Integer, 
        db.ForeignKey('borrowings.id', ondelete='CASCADE'), 
        nullable=False, 
        unique=True
    )
    cancel_reason = db.Column(db.Text, nullable=True)  
    remarks = db.Column(db.Text, nullable=True) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    borrowing = db.relationship(
        'Borrowing',
        backref=db.backref('details', uselist=False, lazy=True, cascade='all, delete-orphan', passive_deletes=True)
    )

    def __repr__(self):
        return f"<BorrowingDetails {self.id}: Reason={self.cancel_reason}, Remarks={self.remarks}>"

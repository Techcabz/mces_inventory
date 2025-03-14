from datetime import datetime
import uuid
import random
import string
from sqlalchemy import Enum
from sqlalchemy.event import listens_for
from app.extensions import db
from app.models.cart_models import Cart  

# Many-to-Many Relationship Table
borrowing_cart = db.Table(
    'borrowing_cart',
    db.Column('borrowing_id', db.Integer, db.ForeignKey('borrowings.id', ondelete="CASCADE"), primary_key=True),
    db.Column('cart_id', db.Integer, db.ForeignKey('cart.id', ondelete="CASCADE"), primary_key=True)
)

class Borrowing(db.Model):
    __tablename__ = 'borrowings'

    id = db.Column(db.Integer, primary_key=True)
    reference_number = db.Column(db.String(15), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(Enum("pending", "approved", "cancelled", "completed", name="borrow_status"),
                       default="pending", nullable=False)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('borrowings', lazy=True))
    cart_items = db.relationship('Cart', secondary=borrowing_cart, backref='borrowed_by')

    def generate_reference_number(self):
        """Generate a short, unique reference number."""
        if not self.reference_number:  # Prevent overriding existing reference number
            date_str = datetime.utcnow().strftime("%y%m%d")
            random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            self.reference_number = f"B-{date_str}-{random_str}"
    
    def get_cart_items(self):
        """Retrieve all cart items linked to this borrowing."""
        return db.session.query(Cart).join(borrowing_cart).filter(
            borrowing_cart.c.borrowing_id == self.id
        ).all()

# ✅ Automatically generate reference number before insert
@listens_for(Borrowing, "before_insert")
def set_reference_number(mapper, connection, target):
    if not target.reference_number:  # Generate only if None
        target.generate_reference_number()

from ..extensions import db
from datetime import datetime

class Logs(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    level = db.Column(db.String(50), nullable=False, default='INFO')
    message = db.Column(db.String(255), nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    user = db.relationship('User', backref=db.backref('logs', lazy=True, passive_deletes=True))
    source = db.Column(db.String(120), nullable=True) 
    metadatos = db.Column(db.JSON, nullable=True)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Logs {self.id}: {self.name} - {self.level}>"

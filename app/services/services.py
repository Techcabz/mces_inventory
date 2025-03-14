from ..extensions import db
from sqlalchemy.orm import joinedload

class CRUDService:
    def __init__(self, model):
        self.model = model

    def count(self, **filters):
        query = self.model.query
        for field, value in filters.items():
            query = query.filter(getattr(self.model, field) == value)
        return query.count()
    
    def create(self, **kwargs):
        instance = self.model(**kwargs)
        try:
            db.session.add(instance)
            db.session.commit()
            return instance
        except Exception as e:
            db.session.rollback()
            print(f"Error creating record: {e}")
            return None

    def get(self, **filters):
        query = self.model.query.options(joinedload('*'))
        for field, value in filters.items():
            query = query.filter(getattr(self.model, field) == value)
        return query.all()

    def get_one(self, **filters):
        query = self.model.query
        for field, value in filters.items():
            query = query.filter(getattr(self.model, field) == value)
        return query.first()

    def update(self, record_id, **kwargs):
        instance = self.model.query.get(record_id)
        if instance:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            try:
                db.session.commit()
                return instance
            except Exception as e:
                db.session.rollback()
                print(f"Error updating record: {e}")
        return None

    def delete(self, record_id):
        instance = self.model.query.get(record_id)
        if instance:
            try:
                db.session.delete(instance)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                print(f"Error deleting record: {e}")
        return False  

    # ✅ Add Methods for Managing Relationships
    def add_to_relationship(self, record_id, relationship_field, related_obj):
        """
        Add a related object to a many-to-many relationship field.
        Example: borrowing_service.add_to_relationship(borrowing.id, 'cart_items', cart_item)
        """
        instance = self.model.query.get(record_id)
        if instance:
            try:
                getattr(instance, relationship_field).append(related_obj)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                print(f"Error adding to relationship: {e}")
        return False

    def remove_from_relationship(self, record_id, relationship_field, related_obj):
        """
        Remove a related object from a many-to-many relationship field.
        Example: borrowing_service.remove_from_relationship(borrowing.id, 'cart_items', cart_item)
        """
        instance = self.model.query.get(record_id)
        if instance:
            try:
                getattr(instance, relationship_field).remove(related_obj)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                print(f"Error removing from relationship: {e}")
        return False

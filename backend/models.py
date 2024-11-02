from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"  # Ensure the table name is set explicitly if needed
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # One-to-Many relationship with List
    lists = db.relationship("List", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class List(db.Model):
    __tablename__ = "list"
    list_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # One-to-Many relationship with Item
    items = db.relationship("Item", backref="list", lazy=True)

    def __repr__(self):
        return f"<List {self.title} for User ID {self.user_id}>"


class Item(db.Model):
    __tablename__ = "item"
    item_id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey("list.list_id"), nullable=False)
    parent_item_id = db.Column(db.Integer, db.ForeignKey("item.item_id"), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Recursive relationship for hierarchical structure
    sub_items = db.relationship(
        "Item", backref=db.backref("parent", remote_side=[item_id]), lazy="dynamic"
    )

    def __repr__(self):
        return f"<Item {self.title} in List ID {self.list_id} (Parent ID: {self.parent_item_id})>"

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.Float, nullable=False)

    @classmethod
    def read_from_db(cls):
        return cls.query.first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouse.id"), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouse.id"), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

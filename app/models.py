from app.services import db


class Port(db.Model):
    code = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    parent_slug = db.Column(db.String(255), nullable=False)


class Region(db.Model):
    slug = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    parent_slug = db.Column(db.String(255))


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orig_code = db.Column(db.String(5), nullable=False)
    dest_code = db.Column(db.String(5), nullable=False)
    day = db.Column(db.Date, nullable=False)
    price = db.Column(db.Integer, nullable=False)

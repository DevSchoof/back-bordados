from datetime import datetime
from .extensions import db
from flask_login import UserMixin  # Importe UserMixin
from .utils import convert_google_drive_link

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    alt_description = db.Column(db.Text)
    image_url = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    @property
    def image_url_direct(self):
        return convert_google_drive_link(self.image_url)


class User(db.Model, UserMixin):  # Adicione esta classe
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
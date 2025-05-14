from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager  # Adicione esta linha

db = SQLAlchemy()
cors = CORS()
jwt = JWTManager()  # Adicione esta linha
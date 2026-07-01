from flask import Flask
from flask_migrate import Migrate
from models import db
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

BASE_DIR = Path(__file__).resolve().parent
DB_NAME = os.getenv('DB_NAME')
DATABASE_PATH = BASE_DIR / DB_NAME
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_PATH}?timeout=20"



db.init_app(app)

migrate = Migrate(app, db)
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from config import DATABASE_URL
from models import db
from auth import auth_bp
from notes import notes_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db.init_app(app)

migrate = Migrate(app, db)

CORS(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(notes_bp, url_prefix='/notes')

if __name__ == '__main__':
    app.run(debug=True)

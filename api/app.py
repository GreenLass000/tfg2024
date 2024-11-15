from flask import Flask
from routes import income_list_bp, spent_list_bp, person_bp, record_bp
from utils import init_db

app = Flask(__name__)

# Initialize database
init_db()

# Register blueprints
app.register_blueprint(income_list_bp)
app.register_blueprint(spent_list_bp)
app.register_blueprint(person_bp)
app.register_blueprint(record_bp)

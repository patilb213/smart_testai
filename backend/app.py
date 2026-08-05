import os
from flask import Flask
from models.models import db

# Build an absolute path to the database folder, regardless of where you run this from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # .../smart_testai/backend
DB_DIR = os.path.join(BASE_DIR, "..", "database")               # .../smart_testai/database
DB_PATH = os.path.join(DB_DIR, "app.db")

# Make sure the database folder actually exists
os.makedirs(DB_DIR, exist_ok=True)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def hello():
    return {"status": "ok", "message": "ChangeGuard AI backend running"}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
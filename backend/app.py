from flask import Flask
from flask_cors import CORS
from config import Config
from models.models import db
from auth.auth_routes import auth_bp
from routes.testcase_routes import testcase_bp
from routes.recording_routes import recording_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

db.init_app(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(testcase_bp, url_prefix="/testcases")
app.register_blueprint(recording_bp, url_prefix="/recording")

@app.route("/")
def hello():
    return {"status": "ok", "message": "ChangeGuard AI backend running"}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        try:
            db.session.execute(db.text("ALTER TABLE test_steps ADD COLUMN description VARCHAR(255)"))
            db.session.commit()
        except Exception:
            db.session.rollback()
    app.run(debug=True)
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return {"status": "ok", "message": "ChangeGuard AI backend running"}

if __name__ == "__main__":
    app.run(debug=True)
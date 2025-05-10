from flask import Flask
from backend.api.endpoints import api
from backend.api.events_api import events_api
from backend.database.db_config import Session



app = Flask(__name__)
app.register_blueprint(api)
app.register_blueprint(events_api)


@app.route("/")
def hello():
    return "Hello Fer from PyLynx! 🐾 Upload logs at /upload-log"

if __name__ == "__main__":
    app.run(debug=True)

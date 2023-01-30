from flask import Flask, send_from_directory
from flask_cors import CORS
from app.controller import main
from config import UPLOAD_FOLDER_PATH

app = Flask(__name__)
app.config['SECRET_KEY'] = "bosuna_sayma_yirmi_altı_harfli"

app.config["SQLALCHEMY_ECHO"] = True
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER_PATH
CORS(app)


app.register_blueprint(main)

@app.route('/uploads/<path:path>')
def uploads(path):
    return send_from_directory(app.config['UPLOAD_FOLDER'], path)
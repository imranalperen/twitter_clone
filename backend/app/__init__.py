from flask import Flask
from flask_cors import CORS
from app.controller import main

app = Flask(__name__)
app.config['SECRET_KEY'] = "bosuna_sayma_yirmi_altı_harfli"
app.config["SQLALCHEMY_ECHO"] = True
CORS(app)

app.register_blueprint(main)
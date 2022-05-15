from flask import Flask
from flask_cors import CORS


app = Flask(__name__, template_folder="../templates")
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///analytics.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
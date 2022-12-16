import os
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


    
app = Flask(__name__)
app.secret_key = "utojfmYAPUaD4s7nlCinAwr37FA5r21u"



from app import routes
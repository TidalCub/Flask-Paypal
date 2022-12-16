import os
import json
from flask import Flask


    
app = Flask(__name__)
app.secret_key = "utojfmYAPUaD4s7nlCinAwr37FA5r21u"



from app import routes
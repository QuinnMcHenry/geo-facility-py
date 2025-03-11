#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from flask import Flask, render_template
from flask_cors import CORS
from routes import routes

app = Flask(__name__)
CORS(app)  
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)


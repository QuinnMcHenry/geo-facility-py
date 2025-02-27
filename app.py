#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from flask import Flask, render_template
from flask_cors import CORS
from routes import routes

app = Flask(__name__)
CORS(app)  
app.register_blueprint(routes)

@app.route("/")
def index():
    """Render the main HTML page."""
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Blueprint, jsonify, request
from config import SessionLocal
from models import Facility
import pandas as pd

routes = Blueprint("routes", __name__)

# Hardcoded category dictionary
CATEGORY_DICT = {
    "Mental Health": ["Therapy", "Counseling", "Psychiatry"],
    "Substance Abuse": ["Rehab", "Support Groups"],
}

@routes.route("/categories", methods=["GET"])
def get_categories():
    """Return available categories."""
    return jsonify(list(CATEGORY_DICT.keys()))

@routes.route("/services/<category>", methods=["GET"])
def get_services(category):
    """Return services for a given category."""
    return jsonify(CATEGORY_DICT.get(category, []))

@routes.route("/facilities/<service>", methods=["GET"])
def get_facilities(service):
    """Return facilities offering a selected service."""
    session = SessionLocal()
    results = session.query(Facility).filter(Facility.service == service).all()
    session.close()

    data = [{"name": f.name1, "latitude": f.latitude, "longitude": f.longitude} for f in results]
    return jsonify(data)


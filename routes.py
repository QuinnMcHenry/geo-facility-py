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
    "Type of Care" : ["Substance use treatment",
                    "Detoxification",
                    "Transitional housing, halfway house, or sober home"],

"Service Setting (e.g., Outpatient, Residential, Inpatient, etc.)" : ["Outpatient",
                                                    "Hospital inpatient detoxification",
                                                    "Hospital inpatient treatment",
                                                    "Outpatient detoxification",
                                                    "Outpatient day treatment or partial hospitalization",
                                                    "Intensive outpatient treatment", 
                                                    "Regular outpatient treatment",
                                                    "Residential detoxification",
                                                    "Long-term residential",
                                                    "Short-term residential"],


"Hospitals" : ["General Hospital (including VA hospital)",
               "Psychiatric hospital"],

"Opioid Medications used in Treatment" : ["Methadone used in Treatment",
                                          "Buprenorphine used in Treatment",
                                          "Naltrexone used in Treatment"],


"External Opioid Medications Source" : ["In-network prescribing entity",
                                        "Other contracted prescribing entity",
                                        "No formal relationship with prescribing entity"],


"Type of Alcohol Use Disorder Treatment" : ["Does not treat alcohol use disorder",
                            "Does not use medication assisted treatment for alcohol use disorder",
                            "Accepts clients using medication assisted treatment for alcohol use disorder but prescribed elsewhere"],


"External Source of Medications Used for Alcohol Use Disorder Treatment" : ["In-network prescribing entity",
                                                            "Other contracted prescribing entity",
                                                            "No formal relationship with prescribing entity"],


"Type of Opioid Treatment" : ["Buprenorphine detoxification",
              "Buprenorphine maintenance",
              "Buprenorphine maintenance for predetermined time",
              "Federally-certified Opioid Treatment Program",
              "Methadone detoxification",
              "Methadone maintenance",
              "Methadone maintenance for predetermined time",
              "Prescribes buprenorphine",
              "Prescribes naltrexone",
              "Relapse prevention with naltrexone",
              "Accepts clients using MAT but prescribed elsewhere",
              "Does not use MAT for opioid use disorders",
              "Does not treat opioid use disorders"],


"Pharmacotherapies" : ["Acamprosate (Campral®)",
       "Disulfiram",
       "Methadone",
       "Buprenorphine sub-dermal implant",
       "Buprenorphine with naloxone",
       "Buprenorphine without naloxone",
       "Buprenorphine (extended-release, injectable)",
       "Naltrexone (oral)",
       "Naltrexone (extended-release, injectable)",
       "Medications for HIV treatment",
       "Medications for Hepatitis C treatment",
       "Lofexidine",
       "Clonidine",
       "Medication for mental disorders",
       "Medications for pre-exposure to prophylaxis",
       "Nicotine replacement"
],


"Treatment Approaches" : ["Anger management",
          "Brief intervention",
          "Cognitive behavioral therapy",
          "Community reinforcement plus vouchers",
          "Motivational interviewing",
          "Matrix Model",
          "Relapse prevention",
          "Substance use disorder counseling",
          "Trauma-related counseling",
          "12-step facilitation"
],


"Facility Operation (e.g., Private, Public)" : ["Local, county, or community government",
                                "Department of Defense",
                                "Indian Health Services",
                                "Private for-profit organization",
                                "Private non-profit organization",
                                "State government",
                                "Tribal government",
                                "U.S. Department of Veterans Affairs",
                                "Federal Government"],


"Payment Assistance Available" : ["Payment assistance (check with facility for details)",
                  "Sliding fee scale (fee is based on income and other factors)"],


"Testing" : ["Breathalyzer or blood alcohol testing",
"Drug and alcohol oral fluid testing",
"Drug or alcohol urine screening",
"HIV testing",
"STD testing",
"TB screening",
"Metabolic syndrome monitoring",
"Testing for Hepatitis B (HBV)",
"Testing for Hepatitis C (HCV)"],


"Transitional Services" : [
           "Discharge Planning",
           "Naloxone and overdose education",
           "Outcome follow-up after discharge"],


"Recovery Support Services" : ["Self-help groups",
               "Housing services",
               "Assistance with obtaining social services",
               "Recovery coach",
               "Employment counseling or training"],


"Other Services" : ["Treatment for gambling disorder",
    "Treatment for other addiction disorder"],


"Detoxification (medical withdrawal) Services" : ["Alcohol Detoxification",
                                  "Benzodiazepines Detoxification",
                                  "Cocaine Detoxification",
                                  "Methamphetamines detoxification",
                                  "Opioids detoxification",
                                  "Medication routinely used during detoxification"],


"Education and Counseling Services" : ["HIV or AIDS education, counseling, or support",
                       "Hepatitis education, counseling, or support",
                       "Substance use disorder education",
                       "Individual counseling",
                       "Group counseling",
                       "Family counseling",
                       "Vocational training or educational support (for example, high school coursework, GED preparation, etc.)"],


"Medical Services" : ["Hepatitis A (HAV) vaccination",
      "Hepatitis B (HBV) vaccination"],


"Facility Smoking Policy" : ["Smoking not permitted",
             "Smoking permitted without restriction",
             "Smoking permitted in designated area"],


"Age Groups Accepted" : ["Adults",
         "Seniors",
         "Young adults"],


"Gender Accepted" : ["Female",
     "Male"],


"Exclusive Services" : [
        "Alcohol use disorder clients only",
        "Opioid use disorder clients only"],


"Language Services" : ["Spanish",
       "Sign language services for the deaf and hard of hearing",
       "American Indian or Alaska Native languages",
       "Other languages (excluding Spanish)"],


"Facility Vaping Policy" : ["Vaping not permitted",
            "Vaping permitted without restriction",
            "Vaping permitted in a designated area"],


"Ancillary Services" : ["Acupuncture",
        "Residential beds for clients' children",
        "Case management service",
        "Child care for clients' children",
        "Domestic violence services, including family or partner",
        "Early intervention for HIV",
        "Mental health services",
        "Social skills development",
        "Transportation assistance",
        "Integrated primary care services",
        "Suicide prevention services"]
}

@routes.route("/categories", methods=["GET"])
def get_categories():
    # returns categories from category_dict
    return jsonify(list(CATEGORY_DICT.keys()))

@routes.route("/services/<category>", methods=["GET"])
def get_services(category):
    # returns services from category tuple
    return jsonify(CATEGORY_DICT.get(category, []))

@routes.route("/facilities/<service>", methods=["GET"])
def get_facilities(service):
    # queries SQL database for facilities WHERE service = service
    session = SessionLocal()
    results = session.query(Facility).filter(Facility.service == service).all()
    session.close()

    data = [{"name": f.name1, "latitude": f.latitude, "longitude": f.longitude} for f in results]
    return jsonify(data) # json version of relational data, all columns


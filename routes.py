from flask import Blueprint, jsonify, request
from config import SessionLocal
from models import Facility
import pandas as pd

routes = Blueprint("routes", __name__)

CATEGORY_DICT = {
	"Type of Care" : ["Substance use treatment",
                    "Detoxification",
                    "Transitional housing, halfway house, or sober home",
                    "Treatment for co-ocurring substance use plus either serious mental health illness in adults/serious emotional disturbance in children"],

"Service Setting (e.g., Outpatient, Residential, Inpatient, etc.)" : ["Hospital inpatient/24-hour hospital inpatient",
                                                    "Outpatient",
                                                    "Residential/24-hour residential",
                                                    "Hospital inpatient detoxification",
                                                    "Hospital inpatient treatment",
                                                    "Outpatient detoxification",
                                                    "Outpatient day treatment or partial hospitalization",
                                                    "Intensive outpatient treatment", 
                                                    "Outpatient methadone/buprenorphine or naltrexone treatment",
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
                            "Accepts clients using medication assisted treatment for alcohol use disorder but prescribed elsewhere",
                            "This facility administers/prescribes medication for alcohol use disorder"],


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
              "Use methadone/buprenorphine for pain management or emergency dosing",
              "Accepts clients using MAT but prescribed elsewhere",
              "Does not use MAT for opioid use disorders",
              "Lofexidine/clonidine detoxification",
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
       "Nicotine replacement",
       "Non-nicotine smoking/tobacco cessation"
],


"Treatment Approaches" : ["Anger management",
          "Brief intervention",
          "Cognitive behavioral therapy",
          "Contingency management/motivational incentives",
          "Community reinforcement plus vouchers",
          "Motivational interviewing",
          "Matrix Model",
          "Relapse prevention",
          "Substance use disorder counseling",
          "Telemedicine/telehealth therapy",
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


"License/Certification/Accreditation" : ["State Substance use treatment agency",
                         "State mental health department",
                         "State department of health",
                         "Commission on Accreditation of Rehabilitation Facilities (CARF)",
                         "Council on Accreditation (COA)",
                         "Healthcare Facilities Accreditation Program (HFAP)",
                         "Hospital licensing authority",
                         "The Joint Commission",
                         "National Committee for Quality Assurance (NCQA)",
                         "Federally Qualified Health Center",
                         "SAMHSA certification for opioid treatment program (OTP)",
                         "Drug Enforcement Agency (DEA)"],


"Payment/Insurance/Funding Accepted" : ["Federal, or any government funding for substance use treatment programs",
                        "IHS/Tribal/Urban (ITU) funds",
                        "Medicare",
                        "Medicaid",
                        "Federal military insurance (e.g., TRICARE)",
                        "No payment accepted",
                        "Private health insurance",
                        "Cash or self-payment",
                        "State-financed health insurance plan other than Medicaid",
                        "SAMHSA funding/block grants"],


"Payment Assistance Available" : ["Payment assistance (check with facility for details)",
                  "Sliding fee scale (fee is based on income and other factors)"],


"Special Programs/Groups Offered" : ["Adolescents",
                     "Young adults",
                     "Adult women",
                     "Pregnant/postpartum women",
                     "Adult men",
                     "Seniors or older adults",
                     "Lesbian, gay, bisexual, transgender, or queer/questioning (LGBTQ)",
                     "Veterans",
                     "Active duty military",
                     "Members of military families",
                     "Criminal justice (other than DUI/DWI)/Forensic clients",
                     "Clients with co-occurring mental and substance use disorders",
                     "Clients with co-occurring pain and substance use disorders",
                     "Clients with HIV or AIDS",
                     "Clients who have experienced sexual abuse",
                     "Clients who have experienced intimate partner violence, domestic violence",
                     "Clients who have experienced trauma"],


"Assessment/Pre-treatment" : ["Comprehensive mental health assessment",
              "Comprehensive substance use assessment",
              "Interim services for clients",
              "Outreach to persons in the community",
              "Complete medical history/physical exam",
              "Screening for tobacco use",
              "Screening for substance use",
              "Screening for mental disorders",
              "Professional interventionist/educational consultant"],


"Testing" : ["Breathalyzer or blood alcohol testing",
"Drug and alcohol oral fluid testing",
"Drug or alcohol urine screening",
"HIV testing",
"STD testing",
"TB screening",
"Metabolic syndrome monitoring",
"Testing for Hepatitis B (HBV)",
"Testing for Hepatitis C (HCV)"],


"Transitional Services" : ["Aftercare/continuing care",
           "Discharge Planning",
           "Naloxone and overdose education",
           "Outcome follow-up after discharge"],


"Recovery Support Services" : ["Self-help groups",
               "Housing services",
               "Assistance with obtaining social services",
               "Recovery coach",
               "Mentoring/peer support",
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
                       "Health education services other than HIV/AIDS or hepatitis",
                       "Substance use disorder education",
                       "Smoking/vaping/tobacco cessation counseling",
                       "Individual counseling",
                       "Group counseling",
                       "Family counseling",
                       "Marital/couples counseling",
                       "Vocational training or educational support (for example, high school coursework, GED preparation, etc.)"],


"Medical Services" : ["Hepatitis A (HAV) vaccination",
      "Hepatitis B (HBV) vaccination"],


"Facility Smoking Policy" : ["Smoking not permitted",
             "Smoking permitted without restriction",
             "Smoking permitted in designated area"],


"Age Groups Accepted" : ["Adults",
         "Children/Adolescents",
         "Seniors",
         "Young adults"],


"Gender Accepted" : ["Female",
     "Male"],


"Exclusive Services" : ["Specially designed program for DUI/DWI clients",
        "Serves only DUI/DWI clients",
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

@routes.route("/categories", methods = ["GET"])
def get_categories():
	return jsonify(list(CATEGORY_DICT.keys()))

@routes.route("/services/<category>", methods = ["GET"])
def get_services(category):
	return jsonify(CATEGORT_DICT.get(category, []))

@routes.route("/facilities/<service>", methods = ["GET"])
def get_facilities(service):
	session = SessionLocal()
	results = session.query(Facility).filter(Facility.service == service)
	session.close()

	data - [{"name": f.name1, "latitude": f.latitude, "longitude": f.longitude} for f in results]
	return jsonify(data)
	return jsonify(CATEGORY

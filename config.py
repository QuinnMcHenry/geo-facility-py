#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_USER = "root"
DB_PASSWORD = "Haloninja11"
DB_HOST = "127.0.0.1"
DB_NAME = "nobsv2"

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST:3306}/{DB_NAME}"

try:
    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(bind=engine)
    Base = declarative_base()
    print("Database connected successfully!")

except mysql.connector.Error as err:
    print("Database connection failed: {err}")


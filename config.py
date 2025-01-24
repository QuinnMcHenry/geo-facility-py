#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_USER = "root"
DB_PASSWORD = "Haloninja11"
DB_HOST = "nobsv2"
DB_NAME = "facilities"

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST:3306}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


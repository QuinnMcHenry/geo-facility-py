#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sqlalchemy import Column, Integer, String, Float
from config import Base

class Facility(Base):
    __tablename__ = "facilities"

    name1 = Column(String, primary_key=True)
    service = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)


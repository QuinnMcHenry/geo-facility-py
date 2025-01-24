#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sqlalchemy import Column, Integer, String, Float
from config import Base

class Facility(Base):
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name1 = Column(String(255))
    service = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)


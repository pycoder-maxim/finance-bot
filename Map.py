from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, BigInteger
from sqlalchemy.orm import relationship
from Models import *

association_table = Table('association',Base.metodata,
                          )
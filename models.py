from sqlalchemy import Column, Integer, String

from database import Base


class Drink(Base):
  __tablename = 'drinks'
  id = Column(Integer, primary_key=True)
  name = Column(String(50), unique=True)

  def __init__(self, name=None):
    self.name = name

  def __repr__(self):
    return f'Drink {self.name}'

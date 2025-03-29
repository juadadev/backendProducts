from sqlalchemy import Column, Integer, String
from ..database.database import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True)
    price = Column(Integer, index=True)
    quantity = Column(Integer, index=True)
    description = Column(String(255), index=True)

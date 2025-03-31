from sqlalchemy import Column, Integer, String
from ..database.database import Base
from sqlalchemy.dialects.mysql import CHAR
from uuid import uuid4

class Product(Base):
    __tablename__ = "product"

    id_product = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()), index=True)  # Cambié a CHAR(36) para almacenar UUID

    #id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), index=True)
    price = Column(Integer, index=True)
    quantity = Column(Integer, index=True)
    description = Column(String(255), index=True)

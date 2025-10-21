from uuid import uuid4

from sqlalchemy import Column, Integer, String

from app.database.database import Base


class Product(Base):
    __tablename__ = "product"

    id_product = Column(
        String(36), primary_key=True, default=lambda: str(uuid4()), index=True
    )
    name = Column(String(255), index=True)
    price = Column(Integer, index=True)
    quantity = Column(Integer, index=True)
    description = Column(String(255), index=True)

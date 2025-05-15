from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from app.backend.db import Base
from datetime import datetime


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    comment = Column(String)
    comment_date = Column(DateTime(timezone=True), server_default=func.now())
    grade = Column(Integer)
    is_active = Column(Boolean, default=True)
    user = relationship("User", back_populates="reviews")
    products = relationship("Product", back_populates="reviews")

from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String, Boolean, Enum, TIMESTAMP, func
from app.database import Base

class GroceryList(Base):    
    __tablename__ = "grocery_list"
    grocery_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    member_id = Column(Integer, ForeignKey("family_members.member_id"), nullable=True)
    week_start_date = Column(Date, nullable=False)
    item_name = Column(String(100), nullable=False)
    quantity = Column(String(50))
    purchased = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

class GroceryOrder(Base):
    __tablename__ = "grocery_orders"
    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    member_id = Column(Integer, ForeignKey("family_members.member_id"), nullable=True)
    order_date = Column(Date, nullable=False)
    total_amount = Column(Float)
    status = Column(Enum('Pending','Shipped','Delivered','Cancelled'))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
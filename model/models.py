# ============================================
# model/models.py
# ============================================

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    CASHIER = "cashier"
    STOCK_KEEPER = "stock_keeper"

class PaymentMethod(enum.Enum):
    CASH = "cash"
    CARD = "card"
    MOBILE = "mobile"
    LOYALTY = "loyalty"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    role = Column(Enum(UserRole), default=UserRole.CASHIER)
    branch_id = Column(Integer, ForeignKey("branches.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    branch = relationship("Branch", back_populates="users")
    sales = relationship("Sale", back_populates="cashier")

class Branch(Base):
    __tablename__ = "branches"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255))
    phone = Column(String(20))
    manager_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    
    users = relationship("User", back_populates="branch")
    inventory = relationship("Inventory", back_populates="branch")
    sales = relationship("Sale", back_populates="branch")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"))
    description = Column(Text)
    
    parent = relationship("Category", remote_side=[id])
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    barcode = Column(String(50), unique=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"))
    purchase_price = Column(DECIMAL(10, 2), nullable=False)
    selling_price = Column(DECIMAL(10, 2), nullable=False)
    is_weighted = Column(Boolean, default=False)
    tax_rate = Column(DECIMAL(5, 2), default=0.00)
    min_stock = Column(Integer, default=5)
    expiry_days = Column(Integer)
    unit = Column(String(20), default="piece")
    image_path = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    category = relationship("Category", back_populates="products")
    inventory_items = relationship("Inventory", back_populates="product")
    sale_items = relationship("SaleItem", back_populates="product")

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    branch_id = Column(Integer, ForeignKey("branches.id"))
    quantity = Column(DECIMAL(10, 2), default=0)
    reserved_quantity = Column(DECIMAL(10, 2), default=0)
    expiry_date = Column(DateTime)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    product = relationship("Product", back_populates="inventory_items")
    branch = relationship("Branch", back_populates="inventory")

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.id"))
    cashier_id = Column(Integer, ForeignKey("users.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    discount = Column(DECIMAL(10, 2), default=0)
    tax = Column(DECIMAL(10, 2), default=0)
    total = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(Enum(PaymentMethod), default=PaymentMethod.CASH)
    loyalty_points_earned = Column(Integer, default=0)
    loyalty_points_used = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    branch = relationship("Branch", back_populates="sales")
    cashier = relationship("User", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")

class SaleItem(Base):
    __tablename__ = "sale_items"
    
    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(DECIMAL(10, 2), nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    discount = Column(DECIMAL(10, 2), default=0)
    total = Column(DECIMAL(10, 2), nullable=False)
    
    sale = relationship("Sale", back_populates="items")
    product = relationship("Product", back_populates="sale_items")

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True)
    phone = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    address = Column(Text)
    loyalty_points = Column(Integer, default=0)
    total_spent = Column(DECIMAL(10, 2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_visit = Column(DateTime)
    
    sales = relationship("Sale", back_populates="customer")

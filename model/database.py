# ============================================
# model/database.py
# ============================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from config import Config

Base = declarative_base()

class Database:
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.engine = create_engine(
                Config.DATABASE_URL,
                echo=False,
                pool_size=10,
                max_overflow=20
            )
            cls._instance.Session = scoped_session(sessionmaker(bind=cls._instance.engine))
        return cls._instance
    
    def get_session(self):
        return self.Session()
    
    def create_tables(self):
        Base.metadata.create_all(self.engine)
    
    def drop_tables(self):
        Base.metadata.drop_all(self.engine)
    
    def init_default_data(self):
        session = self.get_session()
        try:
            from model.models import User, Branch, Category, UserRole
            import bcrypt
            
            admin_branch = session.query(Branch).filter(Branch.name == "الفرع الرئيسي").first()
            if not admin_branch:
                admin_branch = Branch(
                    name="الفرع الرئيسي",
                    address="العنوان الرئيسي",
                    phone="123456789",
                    manager_name="المدير العام"
                )
                session.add(admin_branch)
                session.flush()
            
            admin_user = session.query(User).filter(User.username == "admin").first()
            if not admin_user:
                hashed = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
                admin_user = User(
                    username="admin",
                    password_hash=hashed.decode('utf-8'),
                    full_name="مدير النظام",
                    email="admin@supermarket.com",
                    phone="123456789",
                    role=UserRole.ADMIN,
                    branch_id=admin_branch.id,
                    is_active=True
                )
                session.add(admin_user)
            
            categories = [
                {"name": "خضار وفواكه"},
                {"name": "معلبات"},
                {"name": "مشروبات"},
                {"name": "ألبان"},
                {"name": "لحوم"},
                {"name": "مخبوزات"},
                {"name": "منظفات"},
                {"name": "عناية شخصية"}
            ]
            
            for cat_data in categories:
                existing = session.query(Category).filter(Category.name == cat_data["name"]).first()
                if not existing:
                    category = Category(name=cat_data["name"])
                    session.add(category)
            
            session.commit()
            session.close()
            return True
        except Exception as e:
            session.rollback()
            session.close()
            return False

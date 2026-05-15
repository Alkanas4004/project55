# ============================================
# controller/customer_controller.py
# ============================================

from model.database import Database
from model.models import Customer

class CustomerController:
    
    def __init__(self):
        self.db = Database()
    
    def get_all_customers(self):
        session = self.db.get_session()
        try:
            customers = session.query(Customer).order_by(Customer.name).all()
            result = []
            for c in customers:
                result.append({
                    'id': c.id,
                    'name': c.name,
                    'phone': c.phone,
                    'email': c.email,
                    'address': c.address,
                    'loyalty_points': c.loyalty_points,
                    'total_spent': float(c.total_spent),
                    'last_visit': c.last_visit.strftime('%Y-%m-%d %H:%M:%S') if c.last_visit else None,
                    'created_at': c.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            session.close()
            return result
        except Exception as e:
            session.close()
            return []
    
    def search_customer(self, query):
        session = self.db.get_session()
        try:
            customers = session.query(Customer).filter(
                Customer.phone.like(f'%{query}%') | Customer.name.like(f'%{query}%')
            ).limit(10).all()
            
            result = []
            for c in customers:
                result.append({
                    'id': c.id,
                    'name': c.name,
                    'phone': c.phone,
                    'loyalty_points': c.loyalty_points
                })
            session.close()
            return result
        except Exception as e:
            session.close()
            return []
    
    def get_customer_by_phone(self, phone):
        session = self.db.get_session()
        try:
            customer = session.query(Customer).filter(Customer.phone == phone).first()
            if customer:
                result = {
                    'id': customer.id,
                    'name': customer.name,
                    'phone': customer.phone,
                    'email': customer.email,
                    'address': customer.address,
                    'loyalty_points': customer.loyalty_points,
                    'total_spent': float(customer.total_spent)
                }
                session.close()
                return result
            session.close()
            return None
        except Exception as e:
            session.close()
            return None
    
    def add_customer(self, customer_data):
        session = self.db.get_session()
        try:
            existing = session.query(Customer).filter(
                Customer.phone == customer_data.get('phone')
            ).first()
            
            if existing:
                session.close()
                return None
            
            new_customer = Customer(
                name=customer_data.get('name'),
                phone=customer_data.get('phone'),
                email=customer_data.get('email'),
                address=customer_data.get('address')
            )
            session.add(new_customer)
            session.commit()
            session.refresh(new_customer)
            session.close()
            return new_customer.id
        except Exception as e:
            session.rollback()
            session.close()
            return None
    
    def update_customer(self, customer_id, customer_data):
        session = self.db.get_session()
        try:
            customer = session.query(Customer).filter(Customer.id == customer_id).first()
            if customer:
                for key, value in customer_data.items():
                    if hasattr(customer, key):
                        setattr(customer, key, value)
                session.commit()
                session.close()
                return True
            session.close()
            return False
        except Exception as e:
            session.rollback()
            session.close()
            return False
    
    def use_loyalty_points(self, customer_id, points):
        session = self.db.get_session()
        try:
            customer = session.query(Customer).filter(Customer.id == customer_id).first()
            if customer and customer.loyalty_points >= points:
                customer.loyalty_points -= points
                session.commit()
                session.close()
                return True
            session.close()
            return False
        except Exception as e:
            session.rollback()
            session.close()
            return False

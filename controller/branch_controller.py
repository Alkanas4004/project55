# ============================================
# controller/branch_controller.py
# ============================================

from model.database import Database
from model.models import Branch, User, Inventory

class BranchController:
    
    def __init__(self):
        self.db = Database()
    
    def get_all_branches(self):
        session = self.db.get_session()
        try:
            branches = session.query(Branch).filter(Branch.is_active == True).all()
            result = []
            for b in branches:
                result.append({
                    'id': b.id,
                    'name': b.name,
                    'address': b.address,
                    'phone': b.phone,
                    'manager_name': b.manager_name
                })
            session.close()
            return result
        except Exception as e:
            session.close()
            return []
    
    def add_branch(self, branch_data):
        session = self.db.get_session()
        try:
            new_branch = Branch(
                name=branch_data.get('name'),
                address=branch_data.get('address'),
                phone=branch_data.get('phone'),
                manager_name=branch_data.get('manager_name')
            )
            session.add(new_branch)
            session.commit()
            session.refresh(new_branch)
            session.close()
            return new_branch.id
        except Exception as e:
            session.rollback()
            session.close()
            return None
    
    def update_branch(self, branch_id, branch_data):
        session = self.db.get_session()
        try:
            branch = session.query(Branch).filter(Branch.id == branch_id).first()
            if branch:
                for key, value in branch_data.items():
                    if hasattr(branch, key):
                        setattr(branch, key, value)
                session.commit()
                session.close()
                return True
            session.close()
            return False
        except Exception as e:
            session.rollback()
            session.close()
            return False
    
    def get_branch_inventory_summary(self, branch_id):
        session = self.db.get_session()
        try:
            total_products = session.query(Inventory).filter(
                Inventory.branch_id == branch_id
            ).count()
            
            total_value = session.query(
                func.sum(Inventory.quantity * Product.purchase_price)
            ).join(
                Product, Product.id == Inventory.product_id
            ).filter(
                Inventory.branch_id == branch_id
            ).first()
            
            low_stock = session.query(Inventory).filter(
                Inventory.branch_id == branch_id,
                Inventory.quantity <= Product.min_stock
            ).join(Product).count()
            
            session.close()
            
            return {
                'total_products': total_products,
                'total_value': float(total_value[0]) if total_value and total_value[0] else 0,
                'low_stock_count': low_stock
            }
        except Exception as e:
            session.close()
            return None

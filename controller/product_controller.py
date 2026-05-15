# ============================================
# controller/product_controller.py
# ============================================

from model.database import Database
from model.models import Product, Category, Inventory
from sqlalchemy import or_

class ProductController:
    
    def __init__(self):
        self.db = Database()
    
    def get_all_products(self, branch_id=None):
        session = self.db.get_session()
        try:
            query = session.query(Product).filter(Product.is_active == True)
            products = query.all()
            
            result = []
            for p in products:
                inventory = session.query(Inventory).filter(
                    Inventory.product_id == p.id,
                    Inventory.branch_id == branch_id
                ).first() if branch_id else None
                
                result.append({
                    'id': p.id,
                    'barcode': p.barcode,
                    'name': p.name,
                    'description': p.description,
                    'category_id': p.category_id,
                    'category_name': p.category.name if p.category else None,
                    'purchase_price': float(p.purchase_price),
                    'selling_price': float(p.selling_price),
                    'is_weighted': p.is_weighted,
                    'tax_rate': float(p.tax_rate),
                    'min_stock': p.min_stock,
                    'unit': p.unit,
                    'quantity': float(inventory.quantity) if inventory else 0,
                    'image_path': p.image_path,
                    'is_active': p.is_active
                })
            
            session.close()
            return result
        except Exception as e:
            session.close()
            return []
    
    def search_products(self, query, branch_id=None):
        session = self.db.get_session()
        try:
            products = session.query(Product).filter(
                Product.is_active == True,
                or_(
                    Product.barcode.like(f'%{query}%'),
                    Product.name.like(f'%{query}%')
                )
            ).limit(20).all()
            
            result = []
            for p in products:
                inventory = session.query(Inventory).filter(
                    Inventory.product_id == p.id,
                    Inventory.branch_id == branch_id
                ).first() if branch_id else None
                
                result.append({
                    'id': p.id,
                    'barcode': p.barcode,
                    'name': p.name,
                    'selling_price': float(p.selling_price),
                    'quantity': float(inventory.quantity) if inventory else 0,
                    'unit': p.unit
                })
            
            session.close()
            return result
        except Exception as e:
            session.close()
            return []
    
    def get_product_by_barcode(self, barcode, branch_id=None):
        session = self.db.get_session()
        try:
            product = session.query(Product).filter(
                Product.barcode == barcode,
                Product.is_active == True
            ).first()
            
            if product:
                inventory = session.query(Inventory).filter(
                    Inventory.product_id == product.id,
                    Inventory.branch_id == branch_id
                ).first() if branch_id else None
                
                result = {
                    'id': product.id,
                    'barcode': product.barcode,
                    'name': product.name,
                    'selling_price': float(product.selling_price),
                    'quantity': float(inventory.quantity) if inventory else 0,
                    'unit': product.unit
                }
                session.close()
                return result
            
            session.close()
            return None
        except Exception as e:
            session.close()
            return None
    
    def add_product(self, product_data):
        session = self.db.get_session()
        try:
            new_product = Product(
                barcode=product_data.get('barcode'),
                name=product_data.get('name'),
                description=product_data.get('description'),
                category_id=product_data.get('category_id'),
                purchase_price=product_data.get('purchase_price'),
                selling_price=product_data.get('selling_price'),
                is_weighted=product_data.get('is_weighted', False),
                tax_rate=product_data.get('tax_rate', 0),
                min_stock=product_data.get('min_stock', 5),
                unit=product_data.get('unit', 'piece')
            )
            session.add(new_product)
            session.commit()
            session.refresh(new_product)
            
            for branch_id in product_data.get('branch_ids', []):
                inventory = Inventory(
                    product_id=new_product.id,
                    branch_id=branch_id,
                    quantity=product_data.get('initial_quantity', 0)
                )
                session.add(inventory)
            
            session.commit()
            session.close()
            return new_product.id
        except Exception as e:
            session.rollback()
            session.close()
            return None
    
    def update_product(self, product_id, product_data):
        session = self.db.get_session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            if product:
                for key, value in product_data.items():
                    if hasattr(product, key):
                        setattr(product, key, value)
                session.commit()
                session.close()
                return True
            session.close()
            return False
        except Exception as e:
            session.rollback()
            session.close()
            return False
    
    def delete_product(self, product_id):
        session = self.db.get_session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            if product:
                product.is_active = False
                session.commit()
                session.close()
                return True
            session.close()
            return False
        except Exception as e:
            session.rollback()
            session.close()
            return False
    
    def get_categories(self):
        session = self.db.get_session()
        try:
            categories = session.query(Category).all()
            result = [{'id': c.id, 'name': c.name, 'parent_id': c.parent_id} for c in categories]
            session.close()
            return result
        except Exception as e:
            session.close()
            return []
    
    def update_stock(self, product_id, branch_id, quantity, operation='add'):
        session = self.db.get_session()
        try:
            inventory = session.query(Inventory).filter(
                Inventory.product_id == product_id,
                Inventory.branch_id == branch_id
            ).first()
            
            if inventory:
                if operation == 'add':
                    inventory.quantity += quantity
                elif operation == 'subtract':
                    inventory.quantity -= quantity
                elif operation == 'set':
                    inventory.quantity = quantity
                
                inventory.last_updated = None
                session.commit()
                session.close()
                return True
            
            if operation == 'add' or operation == 'set':
                new_inventory = Inventory(
                    product_id=product_id,
                    branch_id=branch_id,
                    quantity=quantity if operation == 'set' else quantity
                )
                session.add(new_inventory)
                session.commit()
                session.close()
                return True
            
            session.close()
            return False
        except Exception as e:
            session.rollback()
            session.close()
            return False

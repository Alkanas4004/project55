# ============================================
# controller/sale_controller.py
# ============================================

from model.database import Database
from model.models import Sale, SaleItem, Inventory, Customer
from datetime import datetime
import uuid

class SaleController:
    
    def __init__(self):
        self.db = Database()
    
    def create_sale(self, sale_data):
        session = self.db.get_session()
        try:
            invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
            
            new_sale = Sale(
                invoice_number=invoice_number,
                branch_id=sale_data.get('branch_id'),
                cashier_id=sale_data.get('cashier_id'),
                customer_id=sale_data.get('customer_id'),
                subtotal=sale_data.get('subtotal'),
                discount=sale_data.get('discount', 0),
                tax=sale_data.get('tax', 0),
                total=sale_data.get('total'),
                payment_method=sale_data.get('payment_method'),
                loyalty_points_earned=sale_data.get('loyalty_points_earned', 0),
                loyalty_points_used=sale_data.get('loyalty_points_used', 0)
            )
            session.add(new_sale)
            session.flush()
            
            for item in sale_data.get('items', []):
                sale_item = SaleItem(
                    sale_id=new_sale.id,
                    product_id=item.get('product_id'),
                    quantity=item.get('quantity'),
                    unit_price=item.get('unit_price'),
                    discount=item.get('discount', 0),
                    total=item.get('total')
                )
                session.add(sale_item)
                
                inventory = session.query(Inventory).filter(
                    Inventory.product_id == item.get('product_id'),
                    Inventory.branch_id == sale_data.get('branch_id')
                ).first()
                
                if inventory:
                    inventory.quantity -= item.get('quantity')
            
            if sale_data.get('customer_id') and sale_data.get('loyalty_points_earned', 0) > 0:
                customer = session.query(Customer).filter(
                    Customer.id == sale_data.get('customer_id')
                ).first()
                if customer:
                    customer.loyalty_points += sale_data.get('loyalty_points_earned', 0)
                    customer.total_spent += sale_data.get('total', 0)
                    customer.last_visit = datetime.now()
            
            session.commit()
            session.close()
            return {'success': True, 'invoice_number': invoice_number}
        except Exception as e:
            session.rollback()
            session.close()
            return {'success': False, 'error': str(e)}
    
    def get_sales(self, start_date=None, end_date=None, branch_id=None, cashier_id=None):
        session = self.db.get_session()
        try:
            query = session.query(Sale)
            
            if start_date:
                query = query.filter(Sale.created_at >= start_date)
            if end_date:
                query = query.filter(Sale.created_at <= end_date)
            if branch_id:
                query = query.filter(Sale.branch_id == branch_id)
            if cashier_id:
                query = query.filter(Sale.cashier_id == cashier_id)
            
            sales = query.order_by(Sale.created_at.desc()).limit(100).all()
            
            result = []
            for s in sales:
                result.append({
                    'id': s.id,
                    'invoice_number': s.invoice_number,
                    'branch_id': s.branch_id,
                    'cashier_name': s.cashier.full_name if s.cashier else None,
                    'customer_name': s.customer.name if s.customer else 'عميل عادي',
                    'subtotal': float(s.subtotal),
                    'discount': float(s.discount),
                    'tax': float(s.tax),
                    'total': float(s.total),
                    'payment_method': s.payment_method.value,
                    'created_at': s.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            session.close()
            return result
        except Exception as e:
            session.close()
            return []
    
    def get_sale_by_id(self, sale_id):
        session = self.db.get_session()
        try:
            sale = session.query(Sale).filter(Sale.id == sale_id).first()
            if sale:
                result = {
                    'id': sale.id,
                    'invoice_number': sale.invoice_number,
                    'branch_id': sale.branch_id,
                    'cashier_id': sale.cashier_id,
                    'cashier_name': sale.cashier.full_name if sale.cashier else None,
                    'customer_id': sale.customer_id,
                    'customer_name': sale.customer.name if sale.customer else 'عميل عادي',
                    'subtotal': float(sale.subtotal),
                    'discount': float(sale.discount),
                    'tax': float(sale.tax),
                    'total': float(sale.total),
                    'payment_method': sale.payment_method.value,
                    'created_at': sale.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'items': []
                }
                
                for item in sale.items:
                    result['items'].append({
                        'product_id': item.product_id,
                        'product_name': item.product.name if item.product else None,
                        'quantity': float(item.quantity),
                        'unit_price': float(item.unit_price),
                        'discount': float(item.discount),
                        'total': float(item.total)
                    })
                
                session.close()
                return result
            
            session.close()
            return None
        except Exception as e:
            session.close()
            return None
    
    def get_daily_report(self, date=None, branch_id=None):
        session = self.db.get_session()
        try:
            if not date:
                date = datetime.now().date()
            
            query = session.query(Sale).filter(
                Sale.created_at >= datetime(date.year, date.month, date.day),
                Sale.created_at < datetime(date.year, date.month, date.day + 1)
            )
            
            if branch_id:
                query = query.filter(Sale.branch_id == branch_id)
            
            sales = query.all()
            
            total_sales = sum(float(s.total) for s in sales)
            total_discount = sum(float(s.discount) for s in sales)
            total_tax = sum(float(s.tax) for s in sales)
            
            session.close()
            return {
                'date': date.strftime('%Y-%m-%d'),
                'total_sales': total_sales,
                'total_discount': total_discount,
                'total_tax': total_tax,
                'net_sales': total_sales - total_discount,
                'transaction_count': len(sales),
                'cash_sales': sum(float(s.total) for s in sales if s.payment_method.value == 'cash'),
                'card_sales': sum(float(s.total) for s in sales if s.payment_method.value == 'card'),
                'mobile_sales': sum(float(s.total) for s in sales if s.payment_method.value == 'mobile')
            }
        except Exception as e:
            session.close()
            return None
    
    def void_sale(self, sale_id, reason):
        session = self.db.get_session()
        try:
            sale = session.query(Sale).filter(Sale.id == sale_id).first()
            if sale:
                for item in sale.items:
                    inventory = session.query(Inventory).filter(
                        Inventory.product_id == item.product_id,
                        Inventory.branch_id == sale.branch_id
                    ).first()
                    if inventory:
                        inventory.quantity += item.quantity
                
                session.delete(sale)
                session.commit()
                session.close()
                return True
            
            session.close()
            return False
        except Exception as e:
            session.rollback()
            session.close()
            return False

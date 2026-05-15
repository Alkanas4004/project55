# ============================================
# controller/report_controller.py
# ============================================

from model.database import Database
from model.models import Sale, SaleItem, Product, Inventory
from datetime import datetime, timedelta
from sqlalchemy import func, and_

class ReportController:
    
    def __init__(self):
        self.db = Database()
    
    def get_sales_report(self, start_date, end_date, branch_id=None):
        session = self.db.get_session()
        try:
            query = session.query(
                func.date(Sale.created_at).label('date'),
                func.count(Sale.id).label('count'),
                func.sum(Sale.total).label('total'),
                func.sum(Sale.discount).label('discount'),
                func.sum(Sale.tax).label('tax')
            ).filter(
                Sale.created_at >= start_date,
                Sale.created_at <= end_date
            )
            
            if branch_id:
                query = query.filter(Sale.branch_id == branch_id)
            
            results = query.group_by(func.date(Sale.created_at)).order_by(func.date(Sale.created_at)).all()
            
            report = []
            for r in results:
                report.append({
                    'date': r.date.strftime('%Y-%m-%d'),
                    'count': r.count,
                    'total': float(r.total) if r.total else 0,
                    'discount': float(r.discount) if r.discount else 0,
                    'tax': float(r.tax) if r.tax else 0,
                    'net': float(r.total) - float(r.discount) if r.total else 0
                })
            
            session.close()
            return report
        except Exception as e:
            session.close()
            return []
    
    def get_top_products(self, start_date, end_date, limit=10, branch_id=None):
        session = self.db.get_session()
        try:
            query = session.query(
                Product.name,
                func.sum(SaleItem.quantity).label('total_quantity'),
                func.sum(SaleItem.total).label('total_revenue')
            ).join(
                SaleItem, SaleItem.product_id == Product.id
            ).join(
                Sale, Sale.id == SaleItem.sale_id
            ).filter(
                Sale.created_at >= start_date,
                Sale.created_at <= end_date,
                Product.is_active == True
            )
            
            if branch_id:
                query = query.filter(Sale.branch_id == branch_id)
            
            results = query.group_by(Product.id).order_by(func.sum(SaleItem.total).desc()).limit(limit).all()
            
            products = []
            for r in results:
                products.append({
                    'name': r.name,
                    'total_quantity': float(r.total_quantity),
                    'total_revenue': float(r.total_revenue)
                })
            
            session.close()
            return products
        except Exception as e:
            session.close()
            return []
    
    def get_inventory_report(self, branch_id):
        session = self.db.get_session()
        try:
            results = session.query(
                Product.name,
                Product.barcode,
                Product.selling_price,
                Product.purchase_price,
                Product.min_stock,
                Inventory.quantity,
                ((Product.selling_price - Product.purchase_price) / Product.purchase_price * 100).label('margin')
            ).join(
                Inventory, Inventory.product_id == Product.id
            ).filter(
                Inventory.branch_id == branch_id,
                Product.is_active == True
            ).all()
            
            report = []
            for r in results:
                report.append({
                    'name': r.name,
                    'barcode': r.barcode,
                    'selling_price': float(r.selling_price),
                    'purchase_price': float(r.purchase_price),
                    'quantity': float(r.quantity),
                    'min_stock': r.min_stock,
                    'margin': float(r.margin) if r.margin else 0,
                    'status': 'منخفض' if float(r.quantity) <= r.min_stock else 'جيد'
                })
            
            session.close()
            return report
        except Exception as e:
            session.close()
            return []
    
    def get_profit_report(self, start_date, end_date, branch_id=None):
        session = self.db.get_session()
        try:
            query = session.query(
                func.sum(SaleItem.quantity * (Product.selling_price - Product.purchase_price)).label('profit')
            ).join(
                SaleItem, SaleItem.product_id == Product.id
            ).join(
                Sale, Sale.id == SaleItem.sale_id
            ).filter(
                Sale.created_at >= start_date,
                Sale.created_at <= end_date
            )
            
            if branch_id:
                query = query.filter(Sale.branch_id == branch_id)
            
            result = query.first()
            
            total_revenue = session.query(func.sum(Sale.total)).filter(
                Sale.created_at >= start_date,
                Sale.created_at <= end_date
            )
            
            if branch_id:
                total_revenue = total_revenue.filter(Sale.branch_id == branch_id)
            
            revenue_result = total_revenue.first()
            
            session.close()
            
            return {
                'total_revenue': float(revenue_result[0]) if revenue_result and revenue_result[0] else 0,
                'total_profit': float(result[0]) if result and result[0] else 0,
                'profit_margin': (float(result[0]) / float(revenue_result[0]) * 100) if result and result[0] and revenue_result and revenue_result[0] else 0
            }
        except Exception as e:
            session.close()
            return None
    
    def get_low_stock_products(self, branch_id):
        session = self.db.get_session()
        try:
            results = session.query(
                Product.name,
                Product.barcode,
                Product.min_stock,
                Inventory.quantity
            ).join(
                Inventory, Inventory.product_id == Product.id
            ).filter(
                Inventory.branch_id == branch_id,
                Inventory.quantity <= Product.min_stock,
                Product.is_active == True
            ).all()
            
            products = []
            for r in results:
                products.append({
                    'name': r.name,
                    'barcode': r.barcode,
                    'min_stock': r.min_stock,
                    'current_stock': float(r.quantity),
                    'needed': r.min_stock - float(r.quantity) if float(r.quantity) < r.min_stock else 0
                })
            
            session.close()
            return products
        except Exception as e:
            session.close()
            return []

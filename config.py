# ============================================
# config.py
# ============================================

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///supermarket.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    APP_NAME = "SuperMarket POS Pro"
    VERSION = "2.0.0"
    COMPANY_NAME = "شركة السوبر ماركت"
    TAX_RATE = float(os.getenv('TAX_RATE', '0.15'))
    CURRENCY = "₪"
    
    LOYALTY_POINTS_RATE = float(os.getenv('LOYALTY_POINTS_RATE', '0.01'))
    BACKUP_DIR = "backups"
    REPORTS_DIR = "reports"
    
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

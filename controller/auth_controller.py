# ============================================
# controller/auth_controller.py
# ============================================

import bcrypt
from model.database import Database
from model.models import User, UserRole

class AuthController:
    
    def __init__(self, parent):
        self.parent = parent
        self.db = Database()
    
    def login(self, username, password):
        session = self.db.get_session()
        try:
            user = session.query(User).filter(
                User.username == username,
                User.is_active == True
            ).first()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                session.close()
                return {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'role': user.role.value,
                    'branch_id': user.branch_id,
                    'email': user.email,
                    'phone': user.phone
                }
            session.close()
            return None
        except Exception as e:
            session.close()
            return None
    
    def logout(self):
        self.parent.current_user = None
        self.parent.logout()
    
    def change_password(self, user_id, old_password, new_password):
        session = self.db.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if bcrypt.checkpw(old_password.encode('utf-8'), user.password_hash.encode('utf-8')):
                hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                user.password_hash = hashed.decode('utf-8')
                session.commit()
                session.close()
                return True
            session.close()
            return False
        except Exception as e:
            session.rollback()
            session.close()
            return False

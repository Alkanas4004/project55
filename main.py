# ============================================
# main.py
# ============================================

import customtkinter as ctk
from controller.auth_controller import AuthController
from view.styles import AppStyles
import logging
import os
import sys

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/system.log'),
        logging.StreamHandler()
    ]
)

class SuperMarketPOSPro(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.title("سوبر ماركت POS - النظام المتكامل")
        self.geometry("1600x900")
        self.minsize(1280, 720)
        
        AppStyles.apply_theme("dark")
        self.configure(fg_color=AppStyles.BG_COLOR)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.auth_controller = AuthController(self)
        self.current_user = None
        self.current_branch_id = None
        
        self.show_login()
    
    def show_login(self):
        from view.windows.login_window import LoginWindow
        self.login_window = LoginWindow(self, self.auth_controller)
        self.login_window.grid(row=0, column=0, sticky="nsew")
    
    def on_login_success(self, user_data):
        self.current_user = user_data
        self.current_branch_id = user_data.get('branch_id', 1)
        self.login_window.destroy()
        self.show_main_app()
    
    def show_main_app(self):
        from view.windows.main_window import MainWindow
        self.main_window = MainWindow(self, self.current_user)
        self.main_window.grid(row=0, column=0, sticky="nsew")
    
    def logout(self):
        if hasattr(self, 'main_window'):
            self.main_window.destroy()
        self.show_login()

def main():
    app = SuperMarketPOSPro()
    app.mainloop()

if __name__ == "__main__":
    main()

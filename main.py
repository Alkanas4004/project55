# ============================================
# main.py
# ============================================

import customtkinter as ctk
from controller.auth_controller import AuthController
from view.styles import AppStyles
import logging
import os

# إنشاء مجلد السجلات إذا لم يكن موجودًا
if not os.path.exists('logs'):
    os.makedirs('logs')

# إعداد نظام التسجيل
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

        # إعدادات النافذة
        self.title("سوبر ماركت POS - النظام المتكامل")
        self.geometry("1600x900")
        self.minsize(1280, 720)

        # تطبيق الثيم
        AppStyles.apply_theme("dark")
        self.configure(fg_color=AppStyles.BG_COLOR)

        # إعداد الشبكة
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # المتغيرات الأساسية
        self.auth_controller = AuthController(self)
        self.current_user = None
        self.current_branch_id = None

        # دخول مباشر بدون تسجيل
        self.show_login()

    # ============================================
    # تخطي تسجيل الدخول والدخول مباشرة
    # ============================================
    def show_login(self):

        user_data = {
            "full_name": "المدير",
            "username": "admin",
            "branch_id": 1
        }

        self.current_user = user_data
        self.current_branch_id = user_data.get("branch_id", 1)

        self.show_main_app()

    # ============================================
    # تسجيل دخول عادي (في حال استخدامه لاحقًا)
    # ============================================
    def on_login_success(self, user_data):

        self.current_user = user_data
        self.current_branch_id = user_data.get('branch_id', 1)

        if hasattr(self, 'login_window'):
            self.login_window.destroy()

        self.show_main_app()

    # ============================================
    # عرض الواجهة الرئيسية
    # ============================================
    def show_main_app(self):

        from view.windows.main_window import MainWindow

        self.main_window = MainWindow(
            self,
            self.current_user
        )

        self.main_window.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    # ============================================
    # تسجيل الخروج
    # ============================================
    def logout(self):

        if hasattr(self, 'main_window'):
            self.main_window.destroy()

        self.show_login()


# ============================================
# تشغيل التطبيق
# ============================================
def main():

    app = SuperMarketPOSPro()
    app.mainloop()


if __name__ == "__main__":
    main()

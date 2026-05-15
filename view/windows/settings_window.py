# ============================================
# view/windows/settings_window.py
# ============================================

import customtkinter as ctk
from view.styles import AppStyles
from tkinter import messagebox
from controller.auth_controller import AuthController

class SettingsWindow(ctk.CTkFrame):
    
    def __init__(self, parent, user_data):
        super().__init__(parent, fg_color=AppStyles.BG_COLOR)
        
        self.parent = parent
        self.user_data = user_data
        self.auth_controller = AuthController(parent)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        
        profile_card = AppStyles.create_card(main_frame)
        profile_card.pack(fill="x", pady=10, padx=20)
        
        AppStyles.create_label(profile_card, text="الملف الشخصي", variant="heading").pack(anchor="w", padx=20, pady=(20, 10))
        
        info_frame = ctk.CTkFrame(profile_card, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=10)
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=2)
        
        ctk.CTkLabel(info_frame, text="اسم المستخدم:", font=AppStyles.BODY_FONT).grid(row=0, column=0, sticky="w", pady=5)
        ctk.CTkLabel(info_frame, text=self.user_data.get('username', ''), font=AppStyles.BODY_FONT).grid(row=0, column=1, sticky="w", pady=5)
        
        ctk.CTkLabel(info_frame, text="الاسم الكامل:", font=AppStyles.BODY_FONT).grid(row=1, column=0, sticky="w", pady=5)
        ctk.CTkLabel(info_frame, text=self.user_data.get('full_name', ''), font=AppStyles.BODY_FONT).grid(row=1, column=1, sticky="w", pady=5)
        
        ctk.CTkLabel(info_frame, text="البريد الإلكتروني:", font=AppStyles.BODY_FONT).grid(row=2, column=0, sticky="w", pady=5)
        ctk.CTkLabel(info_frame, text=self.user_data.get('email', ''), font=AppStyles.BODY_FONT).grid(row=2, column=1, sticky="w", pady=5)
        
        ctk.CTkLabel(info_frame, text="الهاتف:", font=AppStyles.BODY_FONT).grid(row=3, column=0, sticky="w", pady=5)
        ctk.CTkLabel(info_frame, text=self.user_data.get('phone', ''), font=AppStyles.BODY_FONT).grid(row=3, column=1, sticky="w", pady=5)
        
        ctk.CTkLabel(info_frame, text="الصلاحية:", font=AppStyles.BODY_FONT).grid(row=4, column=0, sticky="w", pady=5)
        ctk.CTkLabel(info_frame, text=self.user_data.get('role', ''), font=AppStyles.BODY_FONT).grid(row=4, column=1, sticky="w", pady=5)
        
        password_card = AppStyles.create_card(main_frame)
        password_card.pack(fill="x", pady=10, padx=20)
        
        AppStyles.create_label(password_card, text="تغيير كلمة المرور", variant="heading").pack(anchor="w", padx=20, pady=(20, 10))
        
        pass_frame = ctk.CTkFrame(password_card, fg_color="transparent")
        pass_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(pass_frame, text="كلمة المرور الحالية:").pack(anchor="w", pady=(0, 5))
        self.old_password_entry = AppStyles.create_entry(pass_frame, placeholder_text="كلمة المرور الحالية", show="*")
        self.old_password_entry.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(pass_frame, text="كلمة المرور الجديدة:").pack(anchor="w", pady=(0, 5))
        self.new_password_entry = AppStyles.create_entry(pass_frame, placeholder_text="كلمة المرور الجديدة", show="*")
        self.new_password_entry.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(pass_frame, text="تأكيد كلمة المرور:").pack(anchor="w", pady=(0, 5))
        self.confirm_password_entry = AppStyles.create_entry(pass_frame, placeholder_text="تأكيد كلمة المرور", show="*")
        self.confirm_password_entry.pack(fill="x", pady=(0, 10))
        
        change_btn = AppStyles.create_button(
            pass_frame, "تغيير كلمة المرور", self.change_password, variant="primary"
        )
        change_btn.pack(pady=10)
        
        theme_card = AppStyles.create_card(main_frame)
        theme_card.pack(fill="x", pady=10, padx=20)
        
        AppStyles.create_label(theme_card, text="المظهر", variant="heading").pack(anchor="w", padx=20, pady=(20, 10))
        
        theme_frame = ctk.CTkFrame(theme_card, fg_color="transparent")
        theme_frame.pack(fill="x", padx=20, pady=10)
        
        theme_var = ctk.StringVar(value="dark")
        
        dark_radio = ctk.CTkRadioButton(theme_frame, text="داكن", variable=theme_var, value="dark")
        dark_radio.pack(side="left", padx=10)
        
        light_radio = ctk.CTkRadioButton(theme_frame, text="فاتح", variable=theme_var, value="light")
        light_radio.pack(side="left", padx=10)
        
        def apply_theme():
            ctk.set_appearance_mode(theme_var.get())
            messagebox.showinfo("نجاح", "تم تغيير المظهر بنجاح")
        
        theme_btn = AppStyles.create_button(theme_frame, "تطبيق", apply_theme, variant="primary", width=100)
        theme_btn.pack(side="left", padx=10)
        
        about_card = AppStyles.create_card(main_frame)
        about_card.pack(fill="x", pady=10, padx=20)
        
        AppStyles.create_label(about_card, text="عن البرنامج", variant="heading").pack(anchor="w", padx=20, pady=(20, 10))
        
        AppStyles.create_label(about_card, text="نظام نقاط البيع المتكامل", variant="body").pack(anchor="w", padx=20, pady=5)
        AppStyles.create_label(about_card, text="الإصدار 2.0.0", variant="body").pack(anchor="w", padx=20, pady=5)
        AppStyles.create_label(about_card, text="جميع الحقوق محفوظة © 2024", variant="body").pack(anchor="w", padx=20, pady=5)
    
    def change_password(self):
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if not old_password or not new_password:
            messagebox.showwarning("تنبيه", "الرجاء إدخال كلمة المرور الحالية والجديدة")
            return
        
        if new_password != confirm_password:
            messagebox.showerror("خطأ", "كلمة المرور الجديدة وتأكيدها غير متطابقين")
            return
        
        if len(new_password) < 6:
            messagebox.showerror("خطأ", "كلمة المرور الجديدة يجب أن تكون 6 أحرف على الأقل")
            return
        
        result = self.auth_controller.change_password(self.user_data['id'], old_password, new_password)
        
        if result:
            messagebox.showinfo("نجاح", "تم تغيير كلمة المرور بنجاح")
            self.old_password_entry.delete(0, "end")
            self.new_password_entry.delete(0, "end")
            self.confirm_password_entry.delete(0, "end")
        else:
            messagebox.showerror("خطأ", "كلمة المرور الحالية غير صحيحة")

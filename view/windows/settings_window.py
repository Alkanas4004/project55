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
        ctk.CTkLabel(info_frame, text=self.user_data.get

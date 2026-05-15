# ============================================
# view/windows/customers_window.py
# ============================================

import customtkinter as ctk
from view.styles import AppStyles
from tkinter import messagebox

class CustomersWindow(ctk.CTkFrame):
    
    def __init__(self, parent, customer_controller, user_data):
        super().__init__(parent, fg_color=AppStyles.BG_COLOR)
        
        self.parent = parent
        self.customer_controller = customer_controller
        self.user_data = user_data
        self.current_customer = None
        
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_customers_list()
        self.setup_customer_form()
        self.load_customers()
    
    def setup_customers_list(self):
        list_frame = AppStyles.create_card(self)
        list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        list_frame.grid_rowconfigure(1, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        AppStyles.create_label(
            list_frame, text="العملاء", variant="heading"
        ).grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        search_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        search_frame.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = AppStyles.create_entry(search_frame, placeholder_text="بحث باسم العميل أو رقم الهاتف")
        self.search_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_customers())
        
        refresh_btn = AppStyles.create_button(
            search_frame, "تحديث", self.load_customers, variant="secondary", width=80
        )
        refresh_btn.grid(row=0, column=1)
        
        self.customers_tree = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        self.customers_tree.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="nsew")
    
    def setup_customer_form(self):
        form_frame = AppStyles.create_card(self)
        form_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        form_frame.grid_columnconfigure(0, weight=1)
        
        AppStyles.create_label(
            form_frame, text="بيانات العميل", variant="heading"
        ).grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        self.name_entry = AppStyles.create_entry(form_frame, placeholder_text="الاسم")
        self.name_entry.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        
        self.phone_entry = AppStyles.create_entry(form_frame, placeholder_text="رقم الهاتف")
        self.phone_entry.grid(row=2, column=0, padx=15, pady=(0, 10), sticky="ew")
        
        self.email_entry = AppStyles.create_entry(form_frame, placeholder_text="البريد الإلكتروني")
        self.email_entry.grid(row=3, column=0, padx=15, pady=(0, 10), sticky="ew")
        
        self.address_entry = AppStyles.create_entry(form_frame, placeholder_text="العنوان")
        self.address_entry.grid(row=4, column=0, padx=15, pady=(0, 10), sticky="ew")
        
        points_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        points_frame.grid(row=5, column=0, padx=15, pady=(0, 10), sticky="ew")
        points_frame.grid_columnconfigure(0, weight=1)
        points_frame.grid_columnconfigure(1, weight=1)
        
        self.points_label = AppStyles.create_label(points_frame, text="نقاط الولاء: 0", variant="body")
        self.points_label.grid(row=0, column=0, sticky="w")
        
        self.spent_label = AppStyles.create_label(points_frame, text="إجمالي المشتريات: 0 ₪", variant="body")
        self.spent_label.grid(row=0, column=1, sticky="e")
        
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="

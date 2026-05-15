# ============================================
# view/windows/products_window.py
# ============================================

import customtkinter as ctk
from view.styles import AppStyles
from tkinter import messagebox, filedialog
from PIL import Image
import os

class ProductsWindow(ctk.CTkFrame):
    
    def __init__(self, parent, product_controller, user_data):
        super().__init__(parent, fg_color=AppStyles.BG_COLOR)
        
        self.parent = parent
        self.product_controller = product_controller
        self.user_data = user_data
        self.current_product = None
        
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_products_list()
        self.setup_product_form()
        self.load_products()
    
    def setup_products_list(self):
        list_frame = AppStyles.create_card(self)
        list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        list_frame.grid_rowconfigure(1, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        AppStyles.create_label(
            list_frame, text="المنتجات", variant="heading"
        ).grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        search_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        search_frame.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = AppStyles.create_entry(search_frame, placeholder_text="بحث باسم المنتج أو الباركود")
        self.search_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_products())
        
        refresh_btn = AppStyles.create_button(
            search_frame, "تحديث", self.load_products, variant="secondary", width=80
        )
        refresh_btn.grid(row=0, column=1)
        
        self.products_tree = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        self.products_tree.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="nsew")
    
    def setup_product_form(self):
        form_frame = AppStyles.create_card(self)
        form_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        form_frame.grid_columnconfigure(0, weight=1)
        
        AppStyles.create_label(
            form_frame, text="بيانات المنتج", variant="heading"
        ).grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        self.name_entry = AppStyles.create_entry(form_frame, placeholder_text="اسم المنتج")
        self.name_entry.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        
        self.barcode_entry = AppStyles.create_entry(form_frame, placeholder_text="الباركود")
        self.barcode_entry.grid(row=2, column=0, padx=15, pady=(0, 10), sticky="ew")
        
        price_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        price_frame.grid(row=3, column=0, padx=15, pady=(0, 10), sticky="ew")
        price_frame.grid_columnconfigure(0, weight=1)
        price_frame.grid_columnconfigure(1, weight=1)
        
        self.purchase_price_entry = AppStyles.create_entry(price_frame, placeholder_text="سعر الشراء")
        self.purchase_price_entry.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        self.selling_price_entry = AppStyles.create_entry(price_frame, placeholder_text="سعر البيع")
        self.selling_price_entry.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        
        self.unit_entry = AppStyles.create_entry(form_frame, placeholder_text="الوحدة (قطعة، كجم، لتر)")
        self.unit_entry.grid(row=4, column=0, padx=15, pady=(0, 10), sticky="ew")
        
        self.min_stock_entry = AppStyles.create_entry(form_frame, placeholder_text="الحد الأدنى للمخزون")
        self.min_stock_entry.grid(row=5, column=0, padx=15, pady=(0, 10), sticky="ew")
        
        self.category_menu = ctk.CTkOptionMenu(
            form_frame,
            values=["خضار وفواكه", "معلبات", "مشروبات", "ألبان", "لحوم", "مخبوزات", "منظفات", "عناية شخصية"],
            height=AppStyles.INPUT_HEIGHT
        )
        self.category_menu.grid(row=6, column=0, padx=15, pady=(0, 10), sticky="ew")
        self.category_menu.set("اختر الفئة")
        
        self.weighted_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            form_frame, text="منتج بالوزن", variable=self.weighted_var
        ).grid(row=7, column=0, padx=15, pady=(0, 10), sticky="w")
        
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.grid(row=8, column=0, padx=15, pady=(0, 15), sticky="ew")
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        
        self.save_btn = AppStyles.create_button(
            buttons_frame, "حفظ", self.save_product, variant="success"
        )
        self.save_btn.grid(row=0, column=0, padx=5)
        
        self.delete_btn = AppStyles.create_button(
            buttons_frame, "حذف", self.delete_product, variant="danger"
        )
        self.delete_btn.grid(row=0, column=1, padx=5)
        self.delete_btn.configure(state="disabled")
    
    def load_products(self):
        for widget in self.products_tree.winfo_children():
            widget.destroy()
        
        products = self.product_controller.get_all_products()
        
        for product in products:
            card = ctk.CTkFrame(
                self.products_tree,
                fg_color=AppStyles.SECONDARY_COLOR,
                corner_radius=10
            )
            card.pack(fill="x", pady=5)
            
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)
            
            ctk.CTkLabel(
                info_frame,
                text=product['name'],
                font=AppStyles.BODY_FONT
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=f"باركود: {product['barcode']} | سعر: {product['selling_price']} ₪",
                font=AppStyles.SMALL_FONT,
                text_color=AppStyles.TEXT_SECONDARY
            ).pack(anchor="w")
            
            select_btn = AppStyles.create_button(
                card,
                text="تعديل",
                command=lambda p=product: self.select_product(p),
                variant="primary",
                width=60,
                height=30
            )
            select_btn.pack(side="right", padx=10)
    
    def search_products(self):
        query = self.search_entry.get()
        if not query:
            self.load_products()
            return
        
        for widget in self.products_tree.winfo_children():
            widget.destroy()
        
        products = self.product_controller.search_products(query)
        
        for product in products:
            card = ctk.CTkFrame(
                self.products_tree,
                fg_color=AppStyles.SECONDARY_COLOR,
                corner_radius=10
            )
            card.pack(fill="x", pady=5)
            
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)
            
            ctk.CTkLabel(
                info_frame,
                text=product['name'],
                font=AppStyles.BODY_FONT
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=f"سعر: {product['selling_price']} ₪",
                font=AppStyles.SMALL_FONT,
                text_color=AppStyles.TEXT_SECONDARY
            ).pack(anchor="w")
            
            select_btn = AppStyles.create_button(
                card,
                text="تعديل",
                command=lambda p=product: self.select_product(p),
                variant="primary",
                width=60,
                height=30
            )
            select_btn.pack(side="right", padx=10)
    
    def select_product(self, product):
        self.current_product = product
        
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, product.get('name', ''))
        
        self.barcode_entry.delete(0, "end")
        self.barcode_entry.insert(0, product.get('barcode', ''))
        
        self.purchase_price_entry.delete(0, "end")
        self.purchase_price_entry.insert(0, str(product.get('purchase_price', 0)))
        
        self.selling_price_entry.delete(0, "end")
        self.selling_price_entry.insert(0, str(product.get('selling_price', 0)))
        
        self.unit_entry.delete(0, "end")
        self.unit_entry.insert(0, product.get('unit', ''))
        
        self.min_stock_entry.delete(0, "end")
        self.min_stock_entry.insert(0, str(product.get('min_stock', 5)))
        
        if product.get('category_name'):
            self.category_menu.set(product['category_name'])
        
        self.weighted_var.set(product.get('is_weighted', False))
        
        self.delete_btn.configure(state="normal")
    
    def save_product(self):
        if not self.name_entry.get():
            messagebox.showwarning("تنبيه", "اسم المنتج مطلوب")
            return
        
        product_data = {
            'name': self.name_entry.get(),
            'barcode': self.barcode_entry.get(),
            'purchase_price': float(self.purchase_price_entry.get() or 0),
            'selling_price': float(self.selling_price_entry.get() or 0),
            'unit': self.unit_entry.get(),
            'min_stock': int(self.min_stock_entry.get() or 5),
            'is_weighted': self.weighted_var.get()
        }
        
        if self.current_product:
            result = self.product_controller.update_product(self.current_product['id'], product_data)
            if result:
                messagebox.showinfo("نجاح", "تم تحديث المنتج بنجاح")
                self.load_products()
                self.clear_form()
            else:
                messagebox.showerror("خطأ", "حدث خطأ أثناء تحديث المنتج")
        else:
            result = self.product_controller.add_product(product_data)
            if result:
                messagebox.showinfo("نجاح", "تم إضافة المنتج بنجاح")
                self.load_products()
                self.clear_form()
            else:
                messagebox.showerror("خطأ", "حدث خطأ أثناء إضافة المنتج")
    
    def delete_product(self):
        if self.current_product and messagebox.askyesno("تأكيد", "هل تريد حذف هذا المنتج؟"):
            result = self.product_controller.delete_product(self.current_product['id'])
            if result:
                messagebox.showinfo("نجاح", "تم حذف المنتج بنجاح")
                self.load_products()
                self.clear_form()
            else:
                messagebox.showerror("خطأ", "حدث خطأ أثناء حذف المنتج")
    
    def clear_form(self):
        self.current_product = None
        self.name_entry.delete(0, "end")
        self.barcode_entry.delete(0, "end")
        self.purchase_price_entry.delete(0, "end")
        self.selling_price_entry.delete(0, "end")
        self.unit_entry.delete(0, "end")
        self.min_stock_entry.delete(0, "end")
        self.category_menu.set("اختر الفئة")
        self.weighted_var.set(False)
        self.delete_btn.configure(state="disabled")

# ============================================
# view/windows/inventory_window.py
# ============================================

import customtkinter as ctk
from view.styles import AppStyles
from tkinter import messagebox

class InventoryWindow(ctk.CTkFrame):
    
    def __init__(self, parent, product_controller, branch_controller, user_data):
        super().__init__(parent, fg_color=AppStyles.BG_COLOR)
        
        self.parent = parent
        self.product_controller = product_controller
        self.branch_controller = branch_controller
        self.user_data = user_data
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()
        self.load_inventory()
    
    def setup_ui(self):
        main_frame = AppStyles.create_card(self)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        AppStyles.create_label(
            header_frame, text="إدارة المخزون", variant="heading"
        ).grid(row=0, column=0, sticky="w")
        
        self.branch_menu = ctk.CTkOptionMenu(
            header_frame,
            values=["الفرع الرئيسي"],
            height=AppStyles.INPUT_HEIGHT,
            width=200,
            command=self.on_branch_change
        )
        self.branch_menu.grid(row=0, column=1)
        
        self.load_branches()
        
        search_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        search_frame.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = AppStyles.create_entry(search_frame, placeholder_text="بحث باسم المنتج أو الباركود")
        self.search_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_inventory())
        
        refresh_btn = AppStyles.create_button(
            search_frame, "تحديث", self.load_inventory, variant="secondary", width=100
        )
        refresh_btn.grid(row=0, column=1)
        
        low_stock_btn = AppStyles.create_button(
            search_frame, "منتجات منخفضة", self.show_low_stock, variant="warning", width=120
        )
        low_stock_btn.grid(row=0, column=2, padx=(10, 0))
        
        columns_frame = ctk.CTkFrame(main_frame, fg_color=AppStyles.SECONDARY_COLOR, corner_radius=8)
        columns_frame.grid(row=2, column=0, padx=15, sticky="ew")
        
        headers = ["المنتج", "الباركود", "الكمية", "الحد الأدنى", "الحالة", "إجراءات"]
        widths = [200, 150, 100, 100, 100, 120]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(
                columns_frame,
                text=header,
                font=AppStyles.SUBHEADING_FONT,
                width=width
            ).grid(row=0, column=i, padx=10, pady=10)
        
        self.inventory_list = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        self.inventory_list.grid(row=3, column=0, padx=15, pady=(0, 15), sticky="nsew")
    
    def load_branches(self):
        branches = self.branch_controller.get_all_branches()
        branch_names = [b['name'] for b in branches]
        if branch_names:
            self.branch_menu.configure(values=branch_names)
            self.branch_menu.set(branch_names[0])
    
    def load_inventory(self):
        for widget in self.inventory_list.winfo_children():
            widget.destroy()
        
        branch_name = self.branch_menu.get()
        branches = self.branch_controller.get_all_branches()
        branch_id = None
        for b in branches:
            if b['name'] == branch_name:
                branch_id = b['id']
                break
        
        inventory = self.product_controller.get_all_products(branch_id)
        
        for item in inventory:
            row_frame = ctk.CTkFrame(self.inventory_list, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            status = "جيد"
            status_color = AppStyles.SUCCESS_COLOR
            if item['quantity'] <= item['min_stock']:
                status = "منخفض"
                status_color = AppStyles.DANGER_COLOR
            
            ctk.CTkLabel(row_frame, text=item['name'], width=200, anchor="w").grid(row=0, column=0, padx=10, pady=8)
            ctk.CTkLabel(row_frame, text=item['barcode'], width=150, anchor="w").grid(row=0, column=1, padx=10, pady=8)
            ctk.CTkLabel(row_frame, text=f"{item['quantity']} {item['unit']}", width=100, anchor="w").grid(row=0, column=2, padx=10, pady=8)
            ctk.CTkLabel(row_frame, text=str(item['min_stock']), width=100, anchor="w").grid(row=0, column=3, padx=10, pady=8)
            ctk.CTkLabel(row_frame, text=status, width=100, anchor="w", text_color=status_color).grid(row=0, column=4, padx=10, pady=8)
            
            adjust_btn = AppStyles.create_button(
                row_frame,
                text="تعديل",
                command=lambda p=item: self.adjust_stock(p),
                variant="primary",
                width=80,
                height=30
            )
            adjust_btn.grid(row=0, column=5, padx=10, pady=5)
    
    def search_inventory(self):
        query = self.search_entry.get()
        if not query:
            self.load_inventory()
            return
        
        for widget in self.inventory_list.winfo_children():
            widget.destroy()
        
        branch_name = self.branch_menu.get()
        branches = self.branch_controller.get_all_branches()
        branch_id = None
        for b in branches:
            if b['name'] == branch_name:
                branch_id = b['id']
                break
        
        products = self.product_controller.search_products(query, branch_id)
        
        for item in products:
            row_frame = ctk.CTkFrame(self.inventory_list, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row_frame, text=item['name'], width=300, anchor="w").grid(row=0, column=0, padx=10, pady=8)
            ctk.CTkLabel(row_frame, text=f"{item.get('quantity', 0)} {item.get('unit', '')}", width=150, anchor="w").grid(row=0, column=1, padx=10, pady=8)
            
            adjust_btn = AppStyles.create_button(
                row_frame,
                text="تعديل",
                command=lambda p=item: self.adjust_stock(p),
                variant="primary",
                width=80,
                height=30
            )
            adjust_btn.grid(row=0, column=2, padx=10, pady=5)
    
    def adjust_stock(self, product):
        dialog = ctk.CTkToplevel(self)
        dialog.title("تعديل المخزون")
        dialog.geometry("400x350")
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text=product['name'], font=AppStyles.HEADING_FONT).pack(pady=20)
        
        ctk.CTkLabel(dialog, text=f"الكمية الحالية: {product.get('quantity', 0)} {product.get('unit', '')}").pack()
        
        operation = ctk.StringVar(value="add")
        
        ops_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        ops_frame.pack(pady=10)
        
        ctk.CTkRadioButton(ops_frame, text="إضافة", variable=operation, value="add").pack(side="left", padx=10)
        ctk.CTkRadioButton(ops_frame, text="خصم", variable=operation, value="subtract").pack(side="left", padx=10)
        ctk.CTkRadioButton(ops_frame, text="تعيين", variable=operation, value="set").pack(side="left", padx=10)
        
        ctk.CTkLabel(dialog, text="الكمية:").pack()
        quantity_entry = AppStyles.create_entry(dialog, placeholder_text="الكمية")
        quantity_entry.pack(padx=20, pady=10, fill="x")
        
        ctk.CTkLabel(dialog, text="سبب التعديل:").pack()
        reason_entry = AppStyles.create_entry(dialog, placeholder_text="السبب")
        reason_entry.pack(padx=20, pady=10, fill="x")
        
        def save_adjustment():
            try:
                quantity = float(quantity_entry.get())
                if quantity <= 0:
                    messagebox.showwarning("تنبيه", "الكمية يجب أن تكون أكبر من صفر")
                    return
                
                branch_name = self.branch_menu.get()
                branches = self.branch_controller.get_all_branches()
                branch_id = None
                for b in branches:
                    if b['name'] == branch_name:
                        branch_id = b['id']
                        break
                
                if operation.get() == "add":
                    new_quantity = product.get('quantity', 0) + quantity
                elif operation.get() == "subtract":
                    if quantity > product.get('quantity', 0):
                        messagebox.showwarning("تنبيه", "الكمية المراد خصمها أكبر من المتوفر")
                        return
                    new_quantity = product.get('quantity', 0) - quantity
                else:
                    new_quantity = quantity
                
                result = self.product_controller.update_stock(
                    product['id'], branch_id, new_quantity, operation.get()
                )
                
                if result:
                    messagebox.showinfo("نجاح", "تم تحديث المخزون بنجاح")
                    dialog.destroy()
                    self.load_inventory()
                else:
                    messagebox.showerror("خطأ", "حدث خطأ أثناء تحديث المخزون")
            except ValueError:
                messagebox.showerror("خطأ", "الرجاء إدخال كمية صحيحة")
        
        AppStyles.create_button(dialog, text="حفظ", command=save_adjustment, variant="success").pack(pady=20)
    
    def show_low_stock(self):
        for widget in self.inventory_list.winfo_children():
            widget.destroy()
        
        branch_name = self.branch_menu.get()
        branches = self.branch_controller.get_all_branches()
        branch_id = None
        for b in branches:
            if b['name'] == branch_name:
                branch_id = b['id']
                break
        
        inventory = self.product_controller.get_all_products(branch_id)
        low_stock_items = [i for i in inventory if i['quantity'] <= i['min_stock']]
        
        if not low_stock_items:
            ctk.CTkLabel(
                self.inventory_list,
                text="لا توجد منتجات منخفضة المخزون",
                font=AppStyles.BODY_FONT
            ).pack(pady=20)
            return
        
        for item in low_stock_items:
            row_frame = ctk.CTkFrame(self.inventory_list, fg_color=AppStyles.DANGER_COLOR, corner_radius=8)
            row_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row_frame, text=item['name'], width=200, anchor="w").grid(row=0, column=0, padx=10, pady=8)
            ctk.CTkLabel(row_frame, text=item['barcode'], width=150, anchor="w").grid(row=0, column=1, padx=10, pady=8)
            ctk.CTkLabel(row_frame, text=f"{item['quantity']} {item['unit']}", width=100, anchor="w").grid(row=0, column=2, padx=10, pady=8)
            ctk.CTkLabel(row_frame, text=str(item['min_stock']), width=100, anchor="w").grid(row=0, column=3, padx=10, pady=8)
            
            adjust_btn = AppStyles.create_button(
                row_frame,
                text="تعديل",
                command=lambda p=item: self.adjust_stock(p),
                variant="primary",
                width=80,
                height=30
            )
            adjust_btn.grid(row=0, column=4, padx=10, pady=5)
    
    def on_branch_change(self, choice):
        self.load_inventory()

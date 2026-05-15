# ============================================
# view/windows/pos_window.py
# ============================================

import customtkinter as ctk
from view.styles import AppStyles
from tkinter import messagebox
from datetime import datetime

class POSWindow(ctk.CTkFrame):
    
    def __init__(self, parent, sale_controller, product_controller, customer_controller, user_data):
        super().__init__(parent, fg_color=AppStyles.BG_COLOR)
        
        self.parent = parent
        self.sale_controller = sale_controller
        self.product_controller = product_controller
        self.customer_controller = customer_controller
        self.user_data = user_data
        
        self.cart = []
        self.total = 0
        self.discount = 0
        self.tax = 0
        self.current_customer = None
        
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_cart_section()
        self.setup_products_section()
        self.bind_shortcuts()
    
    def setup_products_section(self):
        products_frame = ctk.CTkFrame(self, fg_color=AppStyles.SECONDARY_COLOR, corner_radius=15)
        products_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        products_frame.grid_rowconfigure(2, weight=1)
        products_frame.grid_columnconfigure(0, weight=1)
        
        search_frame = ctk.CTkFrame(products_frame, fg_color="transparent")
        search_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = AppStyles.create_entry(
            search_frame,
            placeholder_text="مسح الباركود أو البحث باسم المنتج"
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.search_entry.bind("<Return>", lambda e: self.search_product())
        
        search_btn = AppStyles.create_button(
            search_frame, "بحث", self.search_product, variant="primary", width=100
        )
        search_btn.grid(row=0, column=1)
        
        self.category_frame = ctk.CTkScrollableFrame(
            products_frame, fg_color="transparent", height=60, orientation="horizontal"
        )
        self.category_frame.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        
        self.load_categories()
        
        self.products_grid = ctk.CTkScrollableFrame(products_frame, fg_color="transparent")
        self.products_grid.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="nsew")
        
        self.load_products()
    
    def setup_cart_section(self):
        cart_frame = AppStyles.create_card(self)
        cart_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        cart_frame.grid_rowconfigure(1, weight=1)
        cart_frame.grid_columnconfigure(0, weight=1)
        
        header_frame = ctk.CTkFrame(cart_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        AppStyles.create_label(
            header_frame, text="سلة المشتريات", variant="heading"
        ).grid(row=0, column=0, sticky="w")
        
        self.customer_label = AppStyles.create_label(
            header_frame, text="عميل: عادي", variant="small"
        )
        self.customer_label.grid(row=1, column=0, sticky="w")
        
        select_customer_btn = AppStyles.create_button(
            header_frame, "اختيار عميل", self.select_customer, variant="secondary", width=100, height=30
        )
        select_customer_btn.grid(row=0, column=1, rowspan=2)
        
        self.cart_text = ctk.CTkTextbox(cart_frame, font=AppStyles.BODY_FONT, height=350)
        self.cart_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        self.cart_text.configure(state="disabled")
        
        total_frame = ctk.CTkFrame(cart_frame, fg_color="transparent")
        total_frame.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="ew")
        total_frame.grid_columnconfigure(1, weight=1)
        
        AppStyles.create_label(total_frame, text="الإجمالي:", variant="subheading").grid(row=0, column=0, sticky="w")
        
        self.total_label = AppStyles.create_label(
            total_frame, text="0.00 ₪", variant="title", text_color=AppStyles.PRIMARY_COLOR
        )
        self.total_label.grid(row=0, column=1, sticky="e")
        
        buttons_frame = ctk.CTkFrame(cart_frame, fg_color="transparent")
        buttons_frame.grid(row=3, column=0, padx=15, pady=(0, 15), sticky="ew")
        buttons_frame.grid_columnconfigure((0,1,2), weight=1)
        
        AppStyles.create_button(
            buttons_frame, "مسح", self.clear_cart, variant="danger", width=100
        ).grid(row=0, column=0, padx=5)
        
        AppStyles.create_button(
            buttons_frame, "خصم", self.apply_discount, variant="warning", width=100
        ).grid(row=0, column=1, padx=5)
        
        AppStyles.create_button(
            buttons_frame, "دفع", self.process_payment, variant="success", width=100
        ).grid(row=0, column=2, padx=5)
    
    def load_categories(self):
        categories = [{"id": 0, "name": "الكل"}]
        categories.extend(self.product_controller.get_categories())
        
        for cat in categories:
            btn = ctk.CTkButton(
                self.category_frame,
                text=cat['name'],
                command=lambda c=cat['id']: self.filter_by_category(c),
                height=35,
                width=100
            )
            btn.pack(side="left", padx=5)
    
    def load_products(self, category_id=None):
        for widget in self.products_grid.winfo_children():
            widget.destroy()
        
        products = self.product_controller.get_all_products(self.user_data.get('branch_id'))
        
        if category_id and category_id != 0:
            products = [p for p in products if p.get('category_id') == category_id]
        
        for i, product in enumerate(products):
            row = i // 4
            col = i % 4
            
            card = ctk.CTkFrame(
                self.products_grid,
                fg_color=AppStyles.SECONDARY_COLOR,
                corner_radius=10
            )
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            ctk.CTkLabel(
                card,
                text=product['name'],
                font=AppStyles.BODY_FONT
            ).pack(pady=(10, 5))
            
            ctk.CTkLabel(
                card,
                text=f"{product['selling_price']:.2f} ₪",
                font=AppStyles.HEADING_FONT,
                text_color=AppStyles.PRIMARY_COLOR
            ).pack(pady=5)
            
            stock_text = f"المتبقي: {product['quantity']} {product['unit']}"
            stock_color = AppStyles.DANGER_COLOR if product['quantity'] <= product.get('min_stock', 5) else AppStyles.TEXT_SECONDARY
            
            ctk.CTkLabel(
                card,
                text=stock_text,
                font=AppStyles.SMALL_FONT,
                text_color=stock_color
            ).pack(pady=5)
            
            AppStyles.create_button(
                card,
                text="إضافة",
                command=lambda p=product: self.add_to_cart(p),
                variant="primary",
                height=35
            ).pack(pady=(5, 10), padx=10, fill="x")
    
    def filter_by_category(self, category_id):
        self.load_products(category_id)
    
    def search_product(self):
        query = self.search_entry.get()
        if not query:
            self.load_products()
            return
        
        products = self.product_controller.search_products(query, self.user_data.get('branch_id'))
        
        for widget in self.products_grid.winfo_children():
            widget.destroy()
        
        for i, product in enumerate(products):
            row = i // 4
            col = i % 4
            
            card = ctk.CTkFrame(
                self.products_grid,
                fg_color=AppStyles.SECONDARY_COLOR,
                corner_radius=10
            )
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            ctk.CTkLabel(
                card,
                text=product['name'],
                font=AppStyles.BODY_FONT
            ).pack(pady=(10, 5))
            
            ctk.CTkLabel(
                card,
                text=f"{product['selling_price']:.2f} ₪",
                font=AppStyles.HEADING_FONT,
                text_color=AppStyles.PRIMARY_COLOR
            ).pack(pady=5)
            
            AppStyles.create_button(
                card,
                text="إضافة",
                command=lambda p=product: self.add_to_cart(p),
                variant="primary",
                height=35
            ).pack(pady=(5, 10), padx=10, fill="x")
    
    def add_to_cart(self, product):
        if product.get('quantity', 0) <= 0:
            messagebox.showwarning("تنبيه", f"المنتج {product['name']} غير متوفر في المخزون")
            return
        
        for item in self.cart:
            if item['product_id'] == product['id']:
                if item['quantity'] + 1 > product.get('quantity', 0):
                    messagebox.showwarning("تنبيه", "الكمية المطلوبة أكبر من المتوفر في المخزون")
                    return
                item['quantity'] += 1
                item['total'] = item['quantity'] * item['unit_price']
                self.update_cart_display()
                return
        
        self.cart.append({
            'product_id': product['id'],
            'name': product['name'],
            'unit_price': product['selling_price'],
            'quantity': 1,
            'total': product['selling_price']
        })
        
        self.update_cart_display()
    
    def update_cart_display(self):
        self.cart_text.configure(state="normal")
        self.cart_text.delete("1.0", "end")
        
        total = 0
        for i, item in enumerate(self.cart, 1):
            line = f"{i}. {item['name']}\n"
            line += f"   الكمية: {item['quantity']}  ×  {item['unit_price']:.2f} = {item['total']:.2f} ₪\n\n"
            self.cart_text.insert("end", line)
            total += item['total']
        
        self.cart_text.configure(state="disabled")
        self.total = total
        after_discount = self.total - self.discount
        after_tax = after_discount + (after_discount * 0.15)
        
        self.total_label.configure(text=f"{after_tax:.2f} ₪")
    
    def clear_cart(self):
        if messagebox.askyesno("تأكيد", "هل تريد مسح السلة بالكامل؟"):
            self.cart = []
            self.discount = 0
            self.update_cart_display()
    
    def apply_discount(self):
        dialog = ctk.CTkInputDialog(text="أدخل قيمة الخصم (₪):", title="خصم")
        discount_value = dialog.get_input()
        
        if discount_value:
            try:
                self.discount = float(discount_value)
                if self.discount > self.total:
                    messagebox.showwarning("تنبيه", "الخصم لا يمكن أن يزيد عن الإجمالي")
                    self.discount = 0
                self.update_cart_display()
            except ValueError:
                messagebox.showerror("خطأ", "الرجاء إدخال رقم صحيح")
    
    def select_customer(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("اختيار عميل")
        dialog.geometry("400x500")
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="بحث عن عميل", font=AppStyles.HEADING_FONT).pack(pady=20)
        
        search_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        search_frame.pack(padx=20, pady=10, fill="x")
        
        search_entry = AppStyles.create_entry(search_frame, placeholder_text="رقم الهاتف أو الاسم")
        search_entry.pack(fill="x")
        
        results_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        results_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        def do_search():
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            query = search_entry.get()
            if not query:
                return
            
            customers = self.customer_controller.search_customer(query)
            
            for customer in customers:
                card = ctk.CTkFrame(results_frame, fg_color=AppStyles.SECONDARY_COLOR, corner_radius=10)
                card.pack(fill="x", pady=5)
                
                ctk.CTkLabel(
                    card,
                    text=customer['name'],
                    font=AppStyles.BODY_FONT
                ).pack(side="left", padx=10, pady=10)
                
                ctk.CTkLabel(
                    card,
                    text=f"نقاط الولاء: {customer['loyalty_points']}",
                    font=AppStyles.SMALL_FONT
                ).pack(side="left", padx=10)
                
                AppStyles.create_button(
                    card,
                    text="اختيار",
                    command=lambda c=customer: self.set_customer(c, dialog),
                    variant="primary",
                    width=80,
                    height=30
                ).pack(side="right", padx=10)
        
        search_entry.bind("<Return>", lambda e: do_search())
        
        ctk.CTkButton(dialog, text="بحث", command=do_search).pack(pady=10)
        
        AppStyles.create_button(
            dialog,
            text="عميل جديد",
            command=lambda: self.add_new_customer(dialog),
            variant="success"
        ).pack(pady=10)
    
    def set_customer(self, customer, dialog):
        self.current_customer = customer
        self.customer_label.configure(text=f"عميل: {customer['name']} (نقاط: {customer['loyalty_points']})")
        dialog.destroy()
    
    def add_new_customer(self, parent_dialog):
        dialog = ctk.CTkToplevel(self)
        dialog.title("إضافة عميل جديد")
        dialog.geometry("400x500")
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="بيانات العميل", font=AppStyles.HEADING_FONT).pack(pady=20)
        
        name_entry = AppStyles.create_entry(dialog, placeholder_text="الاسم")
        name_entry.pack(padx=20, pady=10, fill="x")
        
        phone_entry = AppStyles.create_entry(dialog, placeholder_text="رقم الهاتف")
        phone_entry.pack(padx=20, pady=10, fill="x")
        
        email_entry = AppStyles.create_entry(dialog, placeholder_text="البريد الإلكتروني")
        email_entry.pack(padx=20, pady=10, fill="x")
        
        address_entry = AppStyles.create_entry(dialog, placeholder_text="العنوان")
        address_entry.pack(padx=20, pady=10, fill="x")
        
        def save_customer():
            if not name_entry.get() or not phone_entry.get():
                messagebox.showwarning("تنبيه", "الاسم ورقم الهاتف مطلوبان")
                return
            
            customer_data = {
                'name': name_entry.get(),
                'phone': phone_entry.get(),
                'email': email_entry.get(),
                'address': address_entry.get()
            }
            
            customer_id = self.customer_controller.add_customer(customer_data)
            if customer_id:
                messagebox.showinfo("نجاح", "تم إضافة العميل بنجاح")
                dialog.destroy()
                parent_dialog.destroy()
                
                new_customer = self.customer_controller.get_customer_by_phone(phone_entry.get())
                if new_customer:
                    self.set_customer(new_customer, None)
            else:
                messagebox.showerror("خطأ", "رقم الهاتف موجود مسبقاً")
        
        AppStyles.create_button(dialog, text="حفظ", command=save_customer, variant="success").pack(pady=20)
    
    def process_payment(self):
        if not self.cart:
            messagebox.showwarning("تنبيه", "السلة فارغة")
            return
        
        payment_window = ctk.CTkToplevel(self)
        payment_window.title("الدفع")
        payment_window.geometry("450x600")
        payment_window.grab_set()
        
        ctk.CTkLabel(
            payment_window,
            text=f"الإجمالي: {self.total - self.discount + ((self.total - self.discount) * 0.15):.2f} ₪",
            font=AppStyles.TITLE_FONT
        ).pack(pady=20)
        
        payment_method = ctk.StringVar(value="cash")
        
        methods_frame = ctk.CTkFrame(payment_window, fg_color="transparent")
        methods_frame.pack(pady=10)
        
        ctk.CTkRadioButton(methods_frame, text="نقدي", variable=payment_method, value="cash").pack(anchor="w", pady=5)
        ctk.CTkRadioButton(methods_frame, text="بطاقة ائتمان", variable=payment_method, value="card").pack(anchor="w", pady=5)
        ctk.CTkRadioButton(methods_frame, text="محفظة رقمية", variable=payment_method, value="mobile").pack(anchor="w", pady=5)
        
        if self.current_customer and self.current_customer.get('loyalty_points', 0) > 0:
            points_frame = ctk.CTkFrame(payment_window, fg_color="transparent")
            points_frame.pack(pady=10, fill="x", padx=20)
            
            ctk.CTkLabel(points_frame, text="نقاط الولاء المتاحة:").pack(side="left")
            ctk.CTkLabel(points_frame, text=str(self.current_customer.get('loyalty_points', 0))).pack(side="left", padx=5)
            
            use_points = ctk.BooleanVar(value=False)
            ctk.CTkCheckBox(
                points_frame, 
                text="استخدام نقاط الولاء (100 نقطة = 1₪)",
                variable=use_points
            ).pack(pady=5)
        
        amount_frame = ctk.CTkFrame(payment_window, fg_color="transparent")
        amount_frame.pack(pady=20, fill="x", padx=20)
        
        ctk.CTkLabel(amount_frame, text="المبلغ المدفوع:").pack(anchor="w")
        paid_entry = AppStyles.create_entry(amount_frame, placeholder_text="0.00")
        paid_entry.pack(fill="x", pady=5)
        
        def calculate_change(*args):
            try:
                paid = float(paid_entry.get() or 0)
                total_amount = self.total - self.discount + ((self.total - self.discount) * 0.15)
                if paid >= total_amount:
                    change = paid - total_amount
                    change_label.configure(text=f"الباقي: {change:.2f} ₪", text_color=AppStyles.SUCCESS_COLOR)
                else:
                    change_label.configure(text=f"المتبقي: {total_amount - paid:.2f} ₪", text_color=AppStyles.DANGER_COLOR)
            except:
                pass
        
        paid_entry.bind("<KeyRelease>", calculate_change)
        
        change_label = ctk.CTkLabel(amount_frame, text="", font=AppStyles.BODY_FONT)
        change_label.pack(pady=5)
        
        def confirm_payment():
            method = payment_method.get()
            
            if method == "cash":
                try:
                    paid_amount = float(paid_entry.get() or 0)
                    total_amount = self.total - self.discount + ((self.total - self.discount) * 0.15)
                    if paid_amount < total_amount:
                        messagebox.showerror("خطأ", "المبلغ المدفوع أقل من الإجمالي")
                        return
                except ValueError:
                    messagebox.showerror("خطأ", "الرجاء إدخال مبلغ صحيح")
                    return
            
            points_used = 0
            if self.current_customer and 'use_points' in locals() and use_points.get():
                max_points_value = self.current_customer.get('loyalty_points', 0) / 100
                points_used = min(self.current_customer.get('loyalty_points', 0), (self.total - self.discount) * 100)
                if points_used > 0:
                    self.customer_controller.use_loyalty_points(self.current_customer['id'], int(points_used))
            
            total_after_discount = self.total - self.discount
            tax_amount = total_after_discount * 0.15
            final_total = total_after_discount + tax_amount
            
            sale_data = {
                'branch_id': self.user_data.get('branch_id'),
                'cashier_id': self.user_data.get('id'),
                'customer_id': self.current_customer.get('id') if self.current_customer else None,
                'subtotal': self.total,
                'discount': self.discount,
                'tax': tax_amount,
                'total': final_total,
                'payment_method': method,
                'loyalty_points_earned': int(final_total * 10),
                'loyalty_points_used': int(points_used),
                'items': self.cart
            }
            
            result = self.sale_controller.create_sale(sale_data)
            
            if result['success']:
                change = paid_amount - final_total if method == "cash" else 0
                messagebox.showinfo(
                    "نجاح",
                    f"تمت عملية البيع بنجاح!\nرقم الفاتورة: {result['invoice_number']}\n" +
                    (f"الباقي: {change:.2f} ₪" if change > 0 else "")
                )
                payment_window.destroy()
                self.cart = []
                self.discount = 0
                self.current_customer = None
                self.customer_label.configure(text="عميل: عادي")
                self.update_cart_display()
                self.load_products()
            else:
                messagebox.showerror("خطأ", f"حدث خطأ: {result.get('error', 'غير معروف')}")
        
        AppStyles.create_button(payment_window, text="تأكيد الدفع", command=confirm_payment, variant="success").pack(pady=20, fill="x", padx=20)
    
    def bind_shortcuts(self):
        self.bind("<F1>", lambda e: self.process_payment())
        self.bind("<F2>", lambda e: self.clear_cart())
        self.bind("<F3>", lambda e: self.apply_discount())
        self.bind("<Control-d>", lambda e: self.apply_discount())
        self.bind("<Control-c>", lambda e: self.clear_cart())
        self.bind("<Control-p>", lambda e: self.process_payment())
        self.bind("<Control-f>", lambda e: self.search_entry.focus())

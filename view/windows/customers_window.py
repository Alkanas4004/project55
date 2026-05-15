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
        
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.grid(row=6, column=0, padx=15, pady=(0, 15), sticky="ew")
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        
        self.save_btn = AppStyles.create_button(
            buttons_frame, "حفظ", self.save_customer, variant="success"
        )
        self.save_btn.grid(row=0, column=0, padx=5)
        
        self.delete_btn = AppStyles.create_button(
            buttons_frame, "حذف", self.delete_customer, variant="danger"
        )
        self.delete_btn.grid(row=0, column=1, padx=5)
        self.delete_btn.configure(state="disabled")
        
        self.add_points_btn = AppStyles.create_button(
            form_frame, "إضافة نقاط ولاء", self.add_loyalty_points, variant="warning"
        )
        self.add_points_btn.grid(row=7, column=0, padx=15, pady=(0, 15))
        self.add_points_btn.configure(state="disabled")
    
    def load_customers(self):
        for widget in self.customers_tree.winfo_children():
            widget.destroy()
        
        customers = self.customer_controller.get_all_customers()
        
        for customer in customers:
            card = ctk.CTkFrame(
                self.customers_tree,
                fg_color=AppStyles.SECONDARY_COLOR,
                corner_radius=10
            )
            card.pack(fill="x", pady=5)
            
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)
            
            ctk.CTkLabel(
                info_frame,
                text=customer['name'],
                font=AppStyles.BODY_FONT
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=f"هاتف: {customer['phone']} | نقاط: {customer['loyalty_points']} | مشتريات: {customer['total_spent']:.2f} ₪",
                font=AppStyles.SMALL_FONT,
                text_color=AppStyles.TEXT_SECONDARY
            ).pack(anchor="w")
            
            select_btn = AppStyles.create_button(
                card,
                text="تعديل",
                command=lambda c=customer: self.select_customer(c),
                variant="primary",
                width=60,
                height=30
            )
            select_btn.pack(side="right", padx=10)
    
    def search_customers(self):
        query = self.search_entry.get()
        if not query:
            self.load_customers()
            return
        
        for widget in self.customers_tree.winfo_children():
            widget.destroy()
        
        customers = self.customer_controller.search_customer(query)
        
        for customer in customers:
            card = ctk.CTkFrame(
                self.customers_tree,
                fg_color=AppStyles.SECONDARY_COLOR,
                corner_radius=10
            )
            card.pack(fill="x", pady=5)
            
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)
            
            ctk.CTkLabel(
                info_frame,
                text=customer['name'],
                font=AppStyles.BODY_FONT
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=f"هاتف: {customer['phone']} | نقاط: {customer['loyalty_points']}",
                font=AppStyles.SMALL_FONT,
                text_color=AppStyles.TEXT_SECONDARY
            ).pack(anchor="w")
            
            full_customer = self.customer_controller.get_customer_by_phone(customer['phone'])
            
            select_btn = AppStyles.create_button(
                card,
                text="تعديل",
                command=lambda c=full_customer: self.select_customer(c),
                variant="primary",
                width=60,
                height=30
            )
            select_btn.pack(side="right", padx=10)
    
    def select_customer(self, customer):
        self.current_customer = customer
        
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, customer.get('name', ''))
        
        self.phone_entry.delete(0, "end")
        self.phone_entry.insert(0, customer.get('phone', ''))
        
        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, customer.get('email', ''))
        
        self.address_entry.delete(0, "end")
        self.address_entry.insert(0, customer.get('address', ''))
        
        self.points_label.configure(text=f"نقاط الولاء: {customer.get('loyalty_points', 0)}")
        self.spent_label.configure(text=f"إجمالي المشتريات: {customer.get('total_spent', 0):.2f} ₪")
        
        self.delete_btn.configure(state="normal")
        self.add_points_btn.configure(state="normal")
    
    def save_customer(self):
        if not self.name_entry.get() or not self.phone_entry.get():
            messagebox.showwarning("تنبيه", "الاسم ورقم الهاتف مطلوبان")
            return
        
        customer_data = {
            'name': self.name_entry.get(),
            'phone': self.phone_entry.get(),
            'email': self.email_entry.get(),
            'address': self.address_entry.get()
        }
        
        if self.current_customer:
            result = self.customer_controller.update_customer(self.current_customer['id'], customer_data)
            if result:
                messagebox.showinfo("نجاح", "تم تحديث بيانات العميل بنجاح")
                self.load_customers()
                self.clear_form()
            else:
                messagebox.showerror("خطأ", "حدث خطأ أثناء تحديث البيانات")
        else:
            result = self.customer_controller.add_customer(customer_data)
            if result:
                messagebox.showinfo("نجاح", "تم إضافة العميل بنجاح")
                self.load_customers()
                self.clear_form()
            else:
                messagebox.showerror("خطأ", "رقم الهاتف موجود مسبقاً")
    
    def delete_customer(self):
        if self.current_customer and messagebox.askyesno("تأكيد", "هل تريد حذف هذا العميل؟"):
            result = self.customer_controller.delete_customer(self.current_customer['id'])
            if result:
                messagebox.showinfo("نجاح", "تم حذف العميل بنجاح")
                self.load_customers()
                self.clear_form()
            else:
                messagebox.showerror("خطأ", "حدث خطأ أثناء حذف العميل")
    
    def add_loyalty_points(self):
        if not self.current_customer:
            return
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("إضافة نقاط ولاء")
        dialog.geometry("300x200")
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text=f"العميل: {self.current_customer['name']}", font=AppStyles.HEADING_FONT).pack(pady=20)
        ctk.CTkLabel(dialog, text=f"النقاط الحالية: {self.current_customer['loyalty_points']}").pack()
        
        ctk.CTkLabel(dialog, text="عدد النقاط المراد إضافتها:").pack(pady=(20, 5))
        points_entry = AppStyles.create_entry(dialog, placeholder_text="نقاط")
        points_entry.pack(padx=20, fill="x")
        
        def add_points():
            try:
                points = int(points_entry.get())
                if points <= 0:
                    messagebox.showwarning("تنبيه", "يجب إدخال عدد نقاط أكبر من صفر")
                    return
                
                new_points = self.current_customer['loyalty_points'] + points
                result = self.customer_controller.update_customer(self.current_customer['id'], {'loyalty_points': new_points})
                
                if result:
                    messagebox.showinfo("نجاح", f"تم إضافة {points} نقطة ولاء بنجاح")
                    self.current_customer['loyalty_points'] = new_points
                    self.points_label.configure(text=f"نقاط الولاء: {new_points}")
                    dialog.destroy()
                    self.load_customers()
                else:
                    messagebox.showerror("خطأ", "حدث خطأ أثناء إضافة النقاط")
            except ValueError:
                messagebox.showerror("خطأ", "الرجاء إدخال رقم صحيح")
        
        AppStyles.create_button(dialog, text="إضافة", command=add_points, variant="success").pack(pady=20)
    
    def clear_form(self):
        self.current_customer = None
        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.address_entry.delete(0, "end")
        self.points_label.configure(text="نقاط الولاء: 0")
        self.spent_label.configure(text="إجمالي المشتريات: 0 ₪")
        self.delete_btn.configure(state="disabled")
        self.add_points_btn.configure(state="disabled")

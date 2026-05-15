# ============================================
# view/windows/reports_window.py
# ============================================

import customtkinter as ctk
from view.styles import AppStyles
from tkinter import messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class ReportsWindow(ctk.CTkFrame):
    
    def __init__(self, parent, report_controller, sale_controller, user_data):
        super().__init__(parent, fg_color=AppStyles.BG_COLOR)
        
        self.parent = parent
        self.report_controller = report_controller
        self.sale_controller = sale_controller
        self.user_data = user_data
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()
        self.load_daily_report()
    
    def setup_ui(self):
        main_frame = AppStyles.create_card(self)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        AppStyles.create_label(
            header_frame, text="التقارير والإحصائيات", variant="heading"
        ).grid(row=0, column=0, sticky="w")
        
        tab_view = ctk.CTkTabview(main_frame, fg_color="transparent")
        tab_view.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        
        tab_view.add("التقرير اليومي")
        tab_view.add("المبيعات")
        tab_view.add("المنتجات الأكثر مبيعاً")
        tab_view.add("تقرير المخزون")
        tab_view.add("الربح والخسارة")
        
        self.setup_daily_tab(tab_view.tab("التقرير اليومي"))
        self.setup_sales_tab(tab_view.tab("المبيعات"))
        self.setup_products_tab(tab_view.tab("المنتجات الأكثر مبيعاً"))
        self.setup_inventory_tab(tab_view.tab("تقرير المخزون"))
        self.setup_profit_tab(tab_view.tab("الربح والخسارة"))
    
    def setup_daily_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        
        control_frame = ctk.CTkFrame(parent, fg_color="transparent")
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        control_frame.grid_columnconfigure(0, weight=1)
        
        self.daily_date = ctk.CTkEntry(control_frame, placeholder_text="YYYY-MM-DD", width=150)
        self.daily_date.grid(row=0, column=0, padx=5)
        self.daily_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        load_btn = AppStyles.create_button(
            control_frame, "عرض", self.load_daily_report, variant="primary", width=100
        )
        load_btn.grid(row=0, column=1, padx=5)
        
        self.daily_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.daily_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    
    def setup_sales_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(2, weight=1)
        
        control_frame = ctk.CTkFrame(parent, fg_color="transparent")
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        control_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        ctk.CTkLabel(control_frame, text="من تاريخ:").grid(row=0, column=0)
        self.sales_start_date = ctk.CTkEntry(control_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.sales_start_date.grid(row=0, column=1, padx=5)
        self.sales_start_date.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        
        ctk.CTkLabel(control_frame, text="إلى تاريخ:").grid(row=0, column=2)
        self.sales_end_date = ctk.CTkEntry(control_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.sales_end_date.grid(row=0, column=3, padx=5)
        self.sales_end_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        load_btn = AppStyles.create_button(
            control_frame, "عرض", self.load_sales_report, variant="primary", width=100
        )
        load_btn.grid(row=0, column=4, padx=5)
        
        self.sales_tree = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.sales_tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.sales_chart_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.sales_chart_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
    
    def setup_products_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        
        control_frame = ctk.CTkFrame(parent, fg_color="transparent")
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        control_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        ctk.CTkLabel(control_frame, text="من تاريخ:").grid(row=0, column=0)
        self.products_start_date = ctk.CTkEntry(control_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.products_start_date.grid(row=0, column=1, padx=5)
        self.products_start_date.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        
        ctk.CTkLabel(control_frame, text="إلى تاريخ:").grid(row=0, column=2)
        self.products_end_date = ctk.CTkEntry(control_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.products_end_date.grid(row=0, column=3, padx=5)
        self.products_end_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        load_btn = AppStyles.create_button(
            control_frame, "عرض", self.load_top_products, variant="primary", width=100
        )
        load_btn.grid(row=0, column=4, padx=5)
        
        self.products_tree = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.products_tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    
    def setup_inventory_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        refresh_btn = AppStyles.create_button(
            parent, "تحديث", self.load_inventory_report, variant="primary"
        )
        refresh_btn.pack(pady=10)
        
        self.inventory_tree = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.inventory_tree.pack(padx=10, pady=10, fill="both", expand=True)
    
    def setup_profit_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        
        control_frame = ctk.CTkFrame(parent, fg_color="transparent")
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        control_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        ctk.CTkLabel(control_frame, text="من تاريخ:").grid(row=0, column=0)
        self.profit_start_date = ctk.CTkEntry(control_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.profit_start_date.grid(row=0, column=1, padx=5)
        self.profit_start_date.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        
        ctk.CTkLabel(control_frame, text="إلى تاريخ:").grid(row=0, column=2)
        self.profit_end_date = ctk.CTkEntry(control_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.profit_end_date.grid(row=0, column=3, padx=5)
        self.profit_end_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        load_btn = AppStyles.create_button(
            control_frame, "عرض", self.load_profit_report, variant="primary", width=100
        )
        load_btn.grid(row=0, column=4, padx=5)
        
        self.profit_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.profit_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    
    def load_daily_report(self):
        for widget in self.daily_frame.winfo_children():
            widget.destroy()
        
        try:
            date = datetime.strptime(self.daily_date.get(), "%Y-%m-%d")
        except:
            messagebox.showerror("خطأ", "تاريخ غير صحيح")
            return
        
        report = self.sale_controller.get_daily_report(date, self.user_data.get('branch_id'))
        
        if report:
            stats_frame = ctk.CTkFrame(self.daily_frame, fg_color=AppStyles.SECONDARY_COLOR, corner_radius=10)
            stats_frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(stats_frame, text=f"التاريخ: {report['date']}", font=AppStyles.HEADING_FONT).pack(pady=10)
            
            row1 = ctk.CTkFrame(stats_frame, fg_color="transparent")
            row1.pack(fill="x", pady=5)
            row1.grid_columnconfigure((0,1), weight=1)
            
            AppStyles.create_label(row1, text=f"إجمالي المبيعات: {report['total_sales']:.2f} ₪", variant="body").grid(row=0, column=0)
            AppStyles.create_label(row1, text=f"الخصومات: {report['total_discount']:.2f} ₪", variant="body").grid(row=0, column=1)
            
            row2 = ctk.CTkFrame(stats_frame, fg_color="transparent")
            row2.pack(fill="x", pady=5)
            row2.grid_columnconfigure((0,1), weight=1)
            
            AppStyles.create_label(row2, text=f"الضرائب: {report['total_tax']:.2f} ₪", variant="body").grid(row=0, column=0)
            AppStyles.create_label(row2, text=f"صافي المبيعات: {report['net_sales']:.2f} ₪", variant="body").grid(row=0, column=1)
            
            row3 = ctk.CTkFrame(stats_frame, fg_color="transparent")
            row3.pack(fill="x", pady=5)
            row3.grid_columnconfigure((0,1), weight=1)
            
            AppStyles.create_label(row3, text=f"عدد المعاملات: {report['transaction_count']}", variant="body").grid(row=0, column=0)
            AppStyles.create_label(row3, text=f"نقدي: {report['cash_sales']:.2f} ₪", variant="body").grid(row=0, column=1)
            
            row4 = ctk.CTkFrame(stats_frame, fg_color="transparent")
            row4.pack(fill="x", pady=5)
            row4.grid_columnconfigure((0,1), weight=1)
            
            AppStyles.create_label(row4, text=f"بطاقة: {report['card_sales']:.2f} ₪", variant="body").grid(row=0, column=0)
            AppStyles.create_label(row4, text=f"محفظة: {report['mobile_sales']:.2f} ₪", variant="body").grid(row=0, column=1)
    
    def load_sales_report(self):
        for widget in self.sales_tree.winfo_children():
            widget.destroy()
        
        try:
            start_date = datetime.strptime(self.sales_start_date.get(), "%Y-%m-%d")
            end_date = datetime.strptime(self.sales_end_date.get(), "%Y-%m-%d")
        except:
            messagebox.showerror("خطأ", "تاريخ غير صحيح")
            return
        
        sales = self.sale_controller.get_sales(start_date, end_date, self.user_data.get('branch_id'))
        
        if sales:
            headers_frame = ctk.CTkFrame(self.sales_tree, fg_color=AppStyles.SECONDARY_COLOR, corner_radius=8)
            headers_frame.pack(fill="x", pady=5)
            
            headers = ["رقم الفاتورة", "الكاشير", "العميل", "الإجمالي", "طريقة الدفع", "التاريخ"]
            widths = [150, 150, 150, 100, 100, 150]
            
            for i, (header, width) in enumerate(zip(headers, widths)):
                ctk.CTkLabel(headers_frame, text=header, font=AppStyles.SUBHEADING_FONT, width=width).grid(row=0, column=i, padx=5, pady=10)
            
            for sale in sales:
                row_frame = ctk.CTkFrame(self.sales_tree, fg_color="transparent")
                row_frame.pack(fill="x", pady=2)
                
                ctk.CTkLabel(row_frame, text=sale['invoice_number'], width=150).grid(row=0, column=0, padx=5, pady=5)
                ctk.CTkLabel(row_frame, text=sale['cashier_name'], width=150).grid(row=0, column=1, padx=5, pady=5)
                ctk.CTkLabel(row_frame, text=sale['customer_name'], width=150).grid(row=0, column=2, padx=5, pady=5)
                ctk.CTkLabel(row_frame, text=f"{sale['total']:.2f} ₪", width=100).grid(row=0, column=3, padx=5, pady=5)
                ctk.CTkLabel(row_frame, text=sale['payment_method'], width=100).grid(row=0, column=4, padx=5, pady=5)
                ctk.CTkLabel(row_frame, text=sale['created_at'], width=150).grid(row=0, column=5, padx=5, pady=5)
        
        try:
            for widget in self.sales_chart_frame.winfo_children():
                widget.destroy()
            
            df = pd.DataFrame(sales)
            if not df.empty:
                fig, ax = plt.subplots(figsize=(10, 4))
                df_daily = df.groupby(pd.to_datetime(df['created_at']).dt.date)['total'].sum()
                ax.plot(df_daily.index, df_daily.values, marker='o')
                ax.set_title('المبيعات اليومية')
                ax.set_xlabel('التاريخ')
                ax.set_ylabel('المبيعات (₪)')
                ax.tick_params(axis='x', rotation=45)
                
                canvas = FigureCanvasTkAgg(fig, master=self.sales_chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)
        except:
            pass
    
    def load_top_products(self):
        for widget in self.products_tree.winfo_children():
            widget.destroy()
        
        try:
            start_date = datetime.strptime(self.products_start_date.get(), "%Y-%m-%d")
            end_date = datetime.strptime(self.products_end_date.get(), "%Y-%m-%d")
        except:
            messagebox.showerror("خطأ", "تاريخ غير صحيح")
            return
        
        products = self.report_controller.get_top_products(start_date, end_date, 20, self.user_data.get('branch_id'))
        
        if products:
            headers_frame = ctk.CTkFrame(self.products_tree, fg_color=AppStyles.SECONDARY_COLOR, corner_radius=8)
            headers_frame.pack(fill="x", pady=5)
            
            headers = ["المنتج", "الكمية المباعة", "الإيرادات"]
            widths = [200, 100, 120]
            
            for i, (header, width) in enumerate(zip(headers, widths)):
                ctk.CTkLabel(headers_frame, text=header, font=AppStyles.SUBHEADING_FONT, width=width).grid(row=0, column=i, padx=5, pady=10)
            
            for product in products:
                row_frame = ctk.CTkFrame(self.products_tree, fg_color="transparent")
                row_frame.pack(fill="x", pady=2)
                
                ctk.CTkLabel(row_frame, text=product['name'], width=200).grid(row=0, column=0, padx=5, pady=5)
                ctk.CTkLabel(row_frame, text=f"{product['total_quantity']:.2f}", width=100).grid(row=0, column=1, padx=5, pady=5)
                ctk.CTkLabel(row_frame, text=f"{product['total_revenue']:.2f} ₪", width=120).grid(row=0, column=2, padx=5, pady=5)
    
    def load_inventory_report(self):
        for widget in self.inventory_tree.winfo_children():
            widget.destroy()
        
        inventory = self.report_controller.get_inventory_report(self.user_data.get('branch_id'))
        
        if inventory:
            headers_frame = ctk.CTkFrame(self.inventory_tree, fg_color=AppStyles.SECONDARY_COLOR, corner_radius=8)
            headers_frame.pack(fill="x", pady=5)
            
            headers = ["المنتج", "الباركود", "الكمية", "الحد الأدنى", "سعر البيع", "سعر الشراء", "الحالة"]
            widths = [200, 120, 80, 80, 100, 100, 80]
            
            for i, (header, width) in enumerate(zip(headers, widths)):
                ctk.CTkLabel(headers_frame, text=header, font=AppStyles.SUBHEADING_FONT, width=width).grid(row=0, column=i, padx=5, pady=10)
            
            for item in inventory:
                row_frame = ctk.CTkFrame(self.inventory_tree, fg_color="transparent")
                row_frame.pack(fill="x", pady=2)
                
                status_color = AppStyles.DANGER_COLOR if item['status'] == "منخفض" else AppStyles.SUCCESS_COLOR
                
                ctk.CTkLabel(row_frame, text=item['name'], width=200).grid(row=0, column=0, padx=5, pady=5)
                ctk.CTkLabel(row_frame, text=item['barcode'], width=120).grid(row=0, column=1, padx=5, pady=5)
                ctk.CTkLabel(row_frame, text=f"{item['quantity']:.0f}", width=80).grid(row=0, column=2, padx=5, pady=5)
                ctk.CTkLabel(row_frame, text=item['min_stock'], width=80).grid(row=0, column=3, padx=5, pady=5)
                ctk.CTkLabel(row_frame, text=f"{item['selling_price']:.2f}", width=100).grid(row=0, column=4, padx=5, pady=5)
                ctk.CTkLabel(row_frame, text=f"{item['purchase_price']:.2f}", width=100).grid(row=0, column=5, padx=5, pady=5)
                ctk.CTkLabel(row_frame, text=item['status'], width=80, text_color=status_color).grid(row=0, column=6, padx=5, pady=5)
    
    def load_profit_report(self):
        for widget in self.profit_frame.winfo_children():
            widget.destroy()
        
        try:
            start_date = datetime.strptime(self.profit_start_date.get(), "%Y-%m-%d")
            end_date = datetime.strptime(self.profit_end_date.get(), "%Y-%m-%d")
        except:
            messagebox.showerror("خطأ", "تاريخ غير صحيح")
            return
        
        report = self.report_controller.get_profit_report(start_date, end_date, self.user_data.get('branch_id'))
        
        if report:
            card = ctk.CTkFrame(self.profit_frame, fg_color=AppStyles.SECONDARY_COLOR, corner_radius=10)
            card.pack(fill="both", expand=True, pady=50)
            
            ctk.CTkLabel(card, text="تقرير الربح والخسارة", font=AppStyles.TITLE_FONT).pack(pady=30)
            
            ctk.CTkLabel(card, text=f"إجمالي الإيرادات: {report['total_revenue']:.2f} ₪", font=AppStyles.HEADING_FONT).pack(pady=10)
            ctk.CTkLabel(card, text=f"إجمالي الأرباح: {report['total_profit']:.2f} ₪", font=AppStyles.HEADING_FONT).pack(pady=10)
            ctk.CTkLabel(card, text=f"هامش الربح: {report['profit_margin']:.2f}%", font=AppStyles.HEADING_FONT, text_color=AppStyles.PRIMARY_COLOR).pack(pady=10)

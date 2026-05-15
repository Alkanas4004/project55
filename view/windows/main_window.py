# ============================================
# view/windows/main_window.py
# ============================================

import customtkinter as ctk
from view.styles import AppStyles
from view.windows.pos_window import POSWindow
from view.windows.products_window import ProductsWindow
from view.windows.inventory_window import InventoryWindow
from view.windows.customers_window import CustomersWindow
from view.windows.reports_window import ReportsWindow
from view.windows.settings_window import SettingsWindow

class MainWindow(ctk.CTkFrame):
    
    def __init__(self, parent, user_data):
        super().__init__(parent, fg_color=AppStyles.BG_COLOR)
        
        self.parent = parent
        self.user_data = user_data
        self.current_frame = None
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_sidebar()
        self.show_pos()
    
    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, 
            width=250, 
            fg_color=AppStyles.SECONDARY_COLOR,
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        ctk.CTkLabel(
            self.sidebar,
            text="سوبر ماركت POS",
            font=AppStyles.HEADING_FONT,
            text_color=AppStyles.PRIMARY_COLOR
        ).pack(pady=30)
        
        ctk.CTkLabel(
            self.sidebar,
            text=self.user_data.get('full_name', 'موظف'),
            font=AppStyles.BODY_FONT
        ).pack(pady=(0, 20))
        
        buttons = [
            ("💰 نقطة البيع", self.show_pos),
            ("📦 المنتجات", self.show_products),
            ("📊 المخزون", self.show_inventory),
            ("👥 العملاء", self.show_customers),
            ("📈 التقارير", self.show_reports),
            ("⚙️ الإعدادات", self.show_settings),
            ("🚪 تسجيل خروج", self.logout)
        ]
        
        for text, command in buttons:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=45,
                fg_color="transparent",
                anchor="w",
                font=AppStyles.BODY_FONT
            )
            btn.pack(fill="x", padx=15, pady=5)
    
    def clear_content(self):
        if self.current_frame:
            self.current_frame.destroy()
    
    def show_pos(self):
        self.clear_content()
        from controller.sale_controller import SaleController
        from controller.product_controller import ProductController
        from controller.customer_controller import CustomerController
        
        sale_controller = SaleController()
        product_controller = ProductController()
        customer_controller = CustomerController()
        
        self.current_frame = POSWindow(
            self, 
            sale_controller,
            product_controller,
            customer_controller,
            self.user_data
        )
        self.current_frame.grid(row=0, column=1, sticky="nsew")
    
    def show_products(self):
        self.clear_content()
        from controller.product_controller import ProductController
        product_controller = ProductController()
        self.current_frame = ProductsWindow(self, product_controller, self.user_data)
        self.current_frame.grid(row=0, column=1, sticky="nsew")
    
    def show_inventory(self):
        self.clear_content()
        from controller.product_controller import ProductController
        from controller.branch_controller import BranchController
        product_controller = ProductController()
        branch_controller = BranchController()
        self.current_frame = InventoryWindow(
            self, 
            product_controller, 
            branch_controller, 
            self.user_data
        )
        self.current_frame.grid(row=0, column=1, sticky="nsew")
    
    def show_customers(self):
        self.clear_content()
        from controller.customer_controller import CustomerController
        customer_controller = CustomerController()
        self.current_frame = CustomersWindow(self, customer_controller, self.user_data)
        self.current_frame.grid(row=0, column=1, sticky="nsew")
    
    def show_reports(self):
        self.clear_content()
        from controller.report_controller import ReportController
        from controller.sale_controller import SaleController
        report_controller = ReportController()
        sale_controller = SaleController()
        self.current_frame = ReportsWindow(
            self, 
            report_controller, 
            sale_controller,
            self.user_data
        )
        self.current_frame.grid(row=0, column=1, sticky="nsew")
    
    def show_settings(self):
        self.clear_content()
        self.current_frame = SettingsWindow(self, self.user_data)
        self.current_frame.grid(row=0, column=1, sticky="nsew")
    
    def logout(self):
        self.parent.logout()

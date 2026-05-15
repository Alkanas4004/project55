import customtkinter as ctk
from view.styles import AppStyles


class LoginWindow(ctk.CTkFrame):

    def __init__(self, master, auth_controller):
        super().__init__(master)

        self.master = master
        self.auth_controller = auth_controller

        self.pack(fill="both", expand=True)

        self.build_ui()

    # =====================================
    # UI
    # =====================================
    def build_ui(self):

        self.configure(
            fg_color=AppStyles.BG_COLOR
        )

        # =====================================
        # Login Card
        # =====================================
        self.card = ctk.CTkFrame(
            self,
            width=450,
            height=520,
            corner_radius=20,
            fg_color=AppStyles.SECONDARY_COLOR
        )

        self.card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # =====================================
        # Title
        # =====================================
        self.title = ctk.CTkLabel(
            self.card,
            text="سوبر ماركت POS",
            font=("Arial", 28, "bold"),
            text_color=AppStyles.PRIMARY_COLOR
        )

        self.title.pack(
            pady=(40, 10)
        )

        # =====================================
        # Subtitle
        # =====================================
        self.subtitle = ctk.CTkLabel(
            self.card,
            text="تسجيل الدخول للمتابعة",
            font=("Arial", 16),
            text_color="gray"
        )

        self.subtitle.pack(
            pady=(0, 30)
        )

        # =====================================
        # Username Entry
        # =====================================
        self.username_entry = ctk.CTkEntry(
            self.card,
            placeholder_text="اسم المستخدم",
            width=350,
            height=45,
            corner_radius=12
        )

        self.username_entry.pack(
            pady=10
        )

        # =====================================
        # Password Entry
        # =====================================
        self.password_entry = ctk.CTkEntry(
            self.card,
            placeholder_text="كلمة المرور",
            show="●",
            width=350,
            height=45,
            corner_radius=12
        )

        self.password_entry.pack(
            pady=10
        )

        # =====================================
        # Login Button
        # =====================================
        self.login_button = ctk.CTkButton(
            self.card,
            text="تسجيل الدخول",
            width=350,
            height=50,
            corner_radius=12,
            fg_color=AppStyles.PRIMARY_COLOR,
            command=self.login
        )

        self.login_button.pack(
            pady=25
        )

        # =====================================
        # Demo Button
        # =====================================
        self.demo_button = ctk.CTkButton(
            self.card,
            text="دخول تجريبي",
            width=350,
            height=45,
            corner_radius=12,
            fg_color="gray",
            command=self.demo_login
        )

        self.demo_button.pack(
            pady=5
        )

        # =====================================
        # Status Label
        # =====================================
        self.status_label = ctk.CTkLabel(
            self.card,
            text="",
            font=("Arial", 13),
            text_color="red"
        )

        self.status_label.pack(
            pady=5
        )

        # =====================================
        # Footer
        # =====================================
        self.footer = ctk.CTkLabel(
            self.card,
            text="© 2026 SuperMarket POS",
            font=("Arial", 12),
            text_color="gray"
        )

        self.footer.pack(
            side="bottom",
            pady=20
        )

        # =====================================
        # Enter Key Login
        # =====================================
        self.password_entry.bind(
            "<Return>",
            lambda event: self.login()
        )

    # =====================================
    # Login Function
    # =====================================
    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.show_error("يرجى إدخال اسم المستخدم وكلمة المرور")
            return

        self.login_button.configure(
            state="disabled",
            text="جاري التحقق..."
        )

        try:
            user = self.auth_controller.login(username, password)

            if user:
                self.master.on_login_success(user)

            else:
                self.show_error("اسم المستخدم أو كلمة المرور غير صحيحة")

        except Exception as e:
            self.show_error(f"خطأ: {str(e)}")

        self.login_button.configure(
            state="normal",
            text="تسجيل الدخول"
        )

    # =====================================
    # Demo Login
    # =====================================
    def demo_login(self):

        user_data = {
            "full_name": "المدير",
            "username": "admin",
            "branch_id": 1
        }

        self.master.on_login_success(user_data)

    # =====================================
    # Error Handler
    # =====================================
    def show_error(self, message):

        self.status_label.configure(
            text=message
        )

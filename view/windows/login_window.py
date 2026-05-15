# ============================================
# view/windows/login_window.py
# ============================================
# صفحة تسجيل دخول احترافية لنظام نقاط البيع

import customtkinter as ctk
from view.styles import AppStyles
from tkinter import messagebox
from PIL import Image
import os

class LoginWindow(ctk.CTkFrame):
    """صفحة تسجيل دخول احترافية مع تصميم عصري"""
    
    def __init__(self, parent, auth_controller):
        super().__init__(parent, fg_color=AppStyles.BG_COLOR)
        
        self.parent = parent
        self.auth_controller = auth_controller
        self.attempts = 0  # عدد محاولات الدخول الخاطئة
        
        # تكوين الشبكة الرئيسية لتوسيط المحتوى
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # إنشاء الإطار الرئيسي
        self.setup_main_frame()
        
        # إضافة تأثيرات حركية
        self.fade_in_animation()
        
        # ربط اختصارات لوحة المفاتيح
        self.bind_shortcuts()
    
    def setup_main_frame(self):
        """إعداد الإطار الرئيسي للتسجيل"""
        
        # الإطار الخارجي (Card)
        self.login_frame = AppStyles.create_card(self)
        self.login_frame.grid(row=1, column=1, padx=40, pady=40, sticky="nsew")
        self.login_frame.grid_columnconfigure(0, weight=1)
        
        # صورة الشعار (إذا وجدت)
        self.setup_logo()
        
        # عنوان التطبيق
        self.setup_title()
        
        # رسالة ترحيبية
        self.setup_welcome_message()
        
        # إدخال اسم المستخدم
        self.setup_username_field()
        
        # إدخال كلمة المرور
        self.setup_password_field()
        
        # خيارات إضافية
        self.setup_options()
        
        # زر تسجيل الدخول
        self.setup_login_button()
        
        # زر تسجيل الدخول كضيف
        self.setup_guest_button()
        
        # رسالة حقوق الملكية
        self.setup_footer()
    
    def setup_logo(self):
        """إعداد شعار التطبيق"""
        logo_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=40, pady=(30, 10))
        
        # أيقونة افتراضية (يمكن استبدالها بصورة)
        ctk.CTkLabel(
            logo_frame,
            text="🛒",
            font=("Arial", 60),
            text_color=AppStyles.PRIMARY_COLOR
        ).pack()
    
    def setup_title(self):
        """إعداد عنوان التطبيق"""
        self.title_label = ctk.CTkLabel(
            self.login_frame,
            text="سوبر ماركت POS",
            font=AppStyles.TITLE_FONT,
            text_color=AppStyles.PRIMARY_COLOR
        )
        self.title_label.grid(row=1, column=0, padx=40, pady=(0, 5))
        
        # نص فرعي
        ctk.CTkLabel(
            self.login_frame,
            text="نظام نقاط البيع المتكامل",
            font=AppStyles.SUBHEADING_FONT,
            text_color=AppStyles.TEXT_SECONDARY
        ).grid(row=2, column=0, padx=40, pady=(0, 5))
    
    def setup_welcome_message(self):
        """إعداد رسالة ترحيبية"""
        from datetime import datetime
        hour = datetime.now().hour
        
        if hour < 12:
            greeting = "صباح الخير 🌅"
        elif hour < 18:
            greeting = "مساء الخير ☀️"
        else:
            greeting = "مساء الخير 🌙"
        
        self.welcome_label = ctk.CTkLabel(
            self.login_frame,
            text=greeting,
            font=AppStyles.BODY_FONT,
            text_color=AppStyles.SUCCESS_COLOR
        )
        self.welcome_label.grid(row=3, column=0, padx=40, pady=(20, 30))
    
    def setup_username_field(self):
        """إعداد حقل اسم المستخدم"""
        # إطار لاسم المستخدم
        username_container = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        username_container.grid(row=4, column=0, padx=40, pady=(0, 10), sticky="ew")
        username_container.grid_columnconfigure(0, weight=1)
        
        # أيقونة المستخدم
        ctk.CTkLabel(
            username_container,
            text="👤",
            font=("Arial", 18),
            text_color=AppStyles.TEXT_SECONDARY
        ).grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        # حقل الإدخال
        self.username_entry = AppStyles.create_entry(
            username_container,
            placeholder_text="اسم المستخدم"
        )
        self.username_entry.grid(row=0, column=1, sticky="ew")
        
        # إضافة تأثير عند التركيز
        self.username_entry.bind("<FocusIn>", lambda e: self.on_focus_in(self.username_entry))
        self.username_entry.bind("<FocusOut>", lambda e: self.on_focus_out(self.username_entry))
    
    def setup_password_field(self):
        """إعداد حقل كلمة المرور"""
        # إطار لكلمة المرور
        password_container = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        password_container.grid(row=5, column=0, padx=40, pady=(0, 10), sticky="ew")
        password_container.grid_columnconfigure(0, weight=1)
        
        # أيقونة القفل
        ctk.CTkLabel(
            password_container,
            text="🔒",
            font=("Arial", 18),
            text_color=AppStyles.TEXT_SECONDARY
        ).grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        # حقل الإدخال
        self.password_entry = AppStyles.create_entry(
            password_container,
            placeholder_text="كلمة المرور",
            show="*"
        )
        self.password_entry.grid(row=0, column=1, sticky="ew")
        
        # زر إظهار/إخفاء كلمة المرور
        self.show_password = False
        self.toggle_btn = ctk.CTkButton(
            password_container,
            text="👁️",
            width=40,
            height=40,
            command=self.toggle_password_visibility,
            fg_color="transparent",
            hover_color=AppStyles.SECONDARY_COLOR
        )
        self.toggle_btn.grid(row=0, column=2, padx=(10, 0))
        
        # ربط Enter
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
    
    def setup_options(self):
        """إعداد الخيارات الإضافية"""
        options_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        options_frame.grid(row=6, column=0, padx=40, pady=(10, 20), sticky="ew")
        options_frame.grid_columnconfigure(0, weight=1)
        options_frame.grid_columnconfigure(1, weight=1)
        
        # تذكرني
        self.remember_var = ctk.BooleanVar(value=False)
        self.remember_check = ctk.CTkCheckBox(
            options_frame,
            text="تذكرني",
            variable=self.remember_var,
            text_color=AppStyles.TEXT_COLOR
        )
        self.remember_check.grid(row=0, column=0, sticky="w")
        
        # نسيت كلمة المرور
        self.forgot_btn = ctk.CTkButton(
            options_frame,
            text="نسيت كلمة المرور؟",
            command=self.forgot_password,
            fg_color="transparent",
            text_color=AppStyles.INFO_COLOR,
            font=AppStyles.SMALL_FONT,
            height=30
        )
        self.forgot_btn.grid(row=0, column=1, sticky="e")
    
    def setup_login_button(self):
        """إعداد زر تسجيل الدخول"""
        self.login_button = AppStyles.create_button(
            self.login_frame,
            text="تسجيل الدخول",
            command=self.handle_login,
            variant="primary"
        )
        self.login_button.grid(row=7, column=0, padx=40, pady=(0, 15), sticky="ew")
        
        # إضافة أيقونة على الزر
        self.login_button.configure(
            text="🚀  تسجيل الدخول",
            height=50,
            font=AppStyles.HEADING_FONT
        )
    
    def setup_guest_button(self):
        """إعداد زر تسجيل الدخول كضيف"""
        self.guest_button = AppStyles.create_button(
            self.login_frame,
            text="دخول كضيف",
            command=self.guest_login,
            variant="secondary"
        )
        self.guest_button.grid(row=8, column=0, padx=40, pady=(0, 20), sticky="ew")
    
    def setup_footer(self):
        """إعداد تذييل الصفحة"""
        footer_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        footer_frame.grid(row=9, column=0, padx=40, pady=(0, 20), sticky="ew")
        
        ctk.CTkLabel(
            footer_frame,
            text=f"© 2024 {self.parent.auth_controller.__class__.__name__}",
            font=AppStyles.SMALL_FONT,
            text_color=AppStyles.TEXT_SECONDARY
        ).pack()
        
        # مؤشر الإصدار
        ctk.CTkLabel(
            footer_frame,
            text="الإصدار 2.0.0",
            font=("Arial", 9),
            text_color=AppStyles.TEXT_SECONDARY
        ).pack()
    
    def toggle_password_visibility(self):
        """تبديل إظهار/إخفاء كلمة المرور"""
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.configure(show="")
            self.toggle_btn.configure(text="🙈")
        else:
            self.password_entry.configure(show="*")
            self.toggle_btn.configure(text="👁️")
    
    def on_focus_in(self, entry):
        """تأثير عند التركيز على الحقل"""
        entry.configure(border_color=AppStyles.PRIMARY_COLOR, border_width=2)
    
    def on_focus_out(self, entry):
        """تأثير عند مغادرة الحقل"""
        entry.configure(border_color=AppStyles.SECONDARY_COLOR, border_width=1)
    
    def handle_login(self):
        """معالجة عملية تسجيل الدخول"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # التحقق من صحة الإدخال
        if not username:
            self.show_error("الرجاء إدخال اسم المستخدم", self.username_entry)
            return
        
        if not password:
            self.show_error("الرجاء إدخال كلمة المرور", self.password_entry)
            return
        
        # تعطيل الزر أثناء المعالجة
        self.login_button.configure(state="disabled", text="⏳ جاري التحقق...")
        
        # محاكاة طلب الخادم
        self.parent.after(500, lambda: self.authenticate(username, password))
    
    def authenticate(self, username, password):
        """التحقق من بيانات المستخدم"""
        
        # محاولة تسجيل الدخول
        user = self.auth_controller.login(username, password)
        
        if user:
            # حفظ جلسة المستخدم إذا تم اختيار تذكرني
            if self.remember_var.get():
                self.save_session(username)
            
            # إعادة تعيين عدد المحاولات
            self.attempts = 0
            
            # عرض رسالة نجاح
            messagebox.showinfo(
                "مرحباً بك",
                f"تم تسجيل الدخول بنجاح\nمرحباً {user.get('full_name', username)}"
            )
            
            # الانتقال إلى الواجهة الرئيسية
            self.parent.on_login_success(user)
        else:
            self.attempts += 1
            remaining = 3 - self.attempts
            
            if remaining <= 0:
                # تعطيل الزر بعد 3 محاولات خاطئة
                self.login_button.configure(state="disabled")
                messagebox.showerror(
                    "تم حظر الدخول",
                    "تم تجاوز عدد المحاولات المسموحة.\nالرجاء المحاولة لاحقاً أو الاتصال بالدعم."
                )
                self.parent.after(30000, lambda: self.login_button.configure(state="normal"))
            else:
                self.show_error(
                    f"اسم المستخدم أو كلمة المرور غير صحيحة\nتبقى {remaining} محاولة",
                    self.password_entry
                )
            
            self.login_button.configure(state="normal", text="🚀  تسجيل الدخول")
            
            # مسح حقل كلمة المرور
            self.password_entry.delete(0, "end")
    
    def guest_login(self):
        """تسجيل الدخول كضيف بصلاحيات محدودة"""
        result = messagebox.askyesno(
            "دخول كضيف",
            "الدخول كضيف سيمنحك صلاحيات محدودة للعرض فقط.\nهل تريد المتابعة؟"
        )
        
        if result:
            guest_data = {
                'id': 0,
                'username': 'guest',
                'full_name': 'زائر',
                'role': 'guest',
                'branch_id': 1,
                'email': '',
                'phone': ''
            }
            
            messagebox.showinfo(
                "مرحباً ضيفنا العزيز",
                "أنت الآن في وضع الزائر\nيمكنك تصفح النظام فقط دون تعديل"
            )
            
            self.parent.on_login_success(guest_data)
    
    def forgot_password(self):
        """نافذة استعادة كلمة المرور"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("استعادة كلمة المرور")
        dialog.geometry("400x350")
        dialog.grab_set()
        
        # جعل النافذة في المنتصف
        dialog.transient(self)
        
        ctk.CTkLabel(
            dialog,
            text="استعادة كلمة المرور",
            font=AppStyles.HEADING_FONT,
            text_color=AppStyles.PRIMARY_COLOR
        ).pack(pady=20)
        
        ctk.CTkLabel(
            dialog,
            text="الرجاء إدخال البريد الإلكتروني المسجل",
            font=AppStyles.BODY_FONT
        ).pack(pady=5)
        
        email_entry = AppStyles.create_entry(dialog, placeholder_text="البريد الإلكتروني")
        email_entry.pack(padx=40, pady=20, fill="x")
        
        def send_reset():
            email = email_entry.get()
            if email:
                messagebox.showinfo(
                    "تم الإرسال",
                    f"تم إرسال رابط استعادة كلمة المرور إلى:\n{email}"
                )
                dialog.destroy()
            else:
                messagebox.showwarning("تنبيه", "الرجاء إدخال البريد الإلكتروني")
        
        AppStyles.create_button(
            dialog, "إرسال رابط الاستعادة", send_reset, "primary"
        ).pack(pady=20, padx=40, fill="x")
    
    def save_session(self, username):
        """حفظ جلسة المستخدم"""
        import json
        session_data = {
            'username': username,
            'timestamp': str(__import__('datetime').datetime.now())
        }
        try:
            with open('session.json', 'w') as f:
                json.dump(session_data, f)
        except:
            pass
    
    def load_session(self):
        """تحميل الجلسة المحفوظة"""
        import json
        import os
        try:
            if os.path.exists('session.json'):
                with open('session.json', 'r') as f:
                    session = json.load(f)
                    return session.get('username')
        except:
            pass
        return None
    
    def show_error(self, message, field=None):
        """عرض رسالة خطأ بجوار الحقل"""
        error_label = ctk.CTkLabel(
            self.login_frame,
            text=f"⚠ {message}",
            font=AppStyles.SMALL_FONT,
            text_color=AppStyles.DANGER_COLOR
        )
        
        if field == self.username_entry:
            error_label.grid(row=4, column=0, padx=40, pady=(40, 0))
        elif field == self.password_entry:
            error_label.grid(row=5, column=0, padx=40, pady=(45, 0))
        else:
            # رسالة عامة
            error_label = ctk.CTkLabel(
                self,
                text=f"⚠ {message}",
                font=AppStyles.SMALL_FONT,
                text_color=AppStyles.DANGER_COLOR
            )
            error_label.place(relx=0.5, rely=0.85, anchor="center")
            self.after(3000, error_label.destroy)
            return
        
        # إخفاء الرسالة بعد 3 ثوانٍ
        self.after(3000, error_label.destroy)
        
        # تأثير اهتزاز للحقل
        self.shake_widget(field)
    
    def shake_widget(self, widget, count=5):
        """تأثير اهتزاز للحقل عند الخطأ"""
        original_x = widget.winfo_x()
        for i in range(count):
            offset = 5 if i % 2 == 0 else -5
            self.after(i * 30, lambda: widget.place_configure(x=original_x + offset))
        self.after(count * 30, lambda: widget.place_configure(x=original_x))
    
    def fade_in_animation(self):
        """تأثير ظهور تدريجي"""
        self.alpha = 0
        self.login_frame.configure(fg_color=AppStyles.SECONDARY_COLOR)
        
        def animate():
            if self.alpha < 1:
                self.alpha += 0.05
                self.login_frame.configure(
                    fg_color=self.interpolate_color(
                        AppStyles.SECONDARY_COLOR,
                        AppStyles.SECONDARY_COLOR,
                        self.alpha
                    )
                )
                self.after(20, animate)
        
        animate()
    
    def interpolate_color(self, color1, color2, factor):
        """تدرج لوني للتأثيرات"""
        return color2
    
    def bind_shortcuts(self):
        """ربط اختصارات لوحة المفاتيح"""
        self.bind("<F1>", lambda e: self.show_help())
        self.bind("<Escape>", lambda e: self.parent.quit())
    
    def show_help(self):
        """عرض صفحة المساعدة"""
        help_text = """🔧 المساعدة السريعة:

• اسم المستخدم الافتراضي: admin
• كلمة المرور الافتراضية: admin123

💡 نصائح:
• يمكنك تسجيل الدخول كضيف للتصفح فقط
• اتصل بالدعم إذا واجهت أي مشكلة
• تأكد من صحة بيانات الدخول
"""
        messagebox.showinfo("المساعدة", help_text)


# ============================================
# إضافة تأثيرات CSS-like للواجهة
# ============================================

class AnimatedButton(ctk.CTkButton):
    """زر مع تأثيرات حركية"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
    
    def on_hover(self, event):
        self.configure(transform="scale(1.02)")
    
    def on_leave(self, event):
        self.configure(transform="scale(1)")


# ============================================
# ملاحظات للتخصيص:
# ============================================
"""
يمكنك تخصيص صفحة تسجيل الدخول عن طريق:

1. تغيير الألوان في AppStyles
2. إضافة صورة شعار حقيقية بدلاً من الأيقونة
3. تغيير رسائل الترحيب
4. إضافة كابتشا بعد 3 محاولات خاطئة
5. ربطها بقاعدة بيانات حقيقية للتحقق من المستخدمين
6. إضافة دعم للغة الإنجليزية
7. إضافة خيار تسجيل الدخول باستخدام البصمة أو الوجه
"""

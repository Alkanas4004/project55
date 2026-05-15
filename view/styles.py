# ============================================
# view/styles.py
# ============================================

import customtkinter as ctk

class AppStyles:
    
    BG_COLOR = "#0F172A"
    PRIMARY_COLOR = "#3B82F6"
    SECONDARY_COLOR = "#1E293B"
    SUCCESS_COLOR = "#10B981"
    DANGER_COLOR = "#EF4444"
    WARNING_COLOR = "#F59E0B"
    INFO_COLOR = "#06B6D4"
    TEXT_COLOR = "#F8FAFC"
    TEXT_SECONDARY = "#94A3B8"
    
    LIGHT_BG_COLOR = "#F1F5F9"
    LIGHT_TEXT_COLOR = "#0F172A"
    
    TITLE_FONT = ("Cairo", 24, "bold")
    HEADING_FONT = ("Cairo", 18, "bold")
    SUBHEADING_FONT = ("Cairo", 15, "bold")
    BODY_FONT = ("Cairo", 13)
    SMALL_FONT = ("Cairo", 11)
    
    BUTTON_HEIGHT = 40
    INPUT_HEIGHT = 45
    CARD_RADIUS = 15
    TABLE_ROW_HEIGHT = 35
    
    @classmethod
    def apply_theme(cls, mode="dark"):
        ctk.set_appearance_mode(mode)
        ctk.set_default_color_theme("blue")
    
    @classmethod
    def create_card(cls, parent, **kwargs):
        return ctk.CTkFrame(
            parent,
            fg_color=cls.SECONDARY_COLOR,
            corner_radius=cls.CARD_RADIUS,
            **kwargs
        )
    
    @classmethod
    def create_button(cls, parent, text, command, variant="primary", **kwargs):
        colors = {
            "primary": cls.PRIMARY_COLOR,
            "success": cls.SUCCESS_COLOR,
            "danger": cls.DANGER_COLOR,
            "warning": cls.WARNING_COLOR,
            "info": cls.INFO_COLOR,
            "secondary": cls.SECONDARY_COLOR
        }
        
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            height=cls.BUTTON_HEIGHT,
            fg_color=colors.get(variant, cls.PRIMARY_COLOR),
            hover_color=colors.get(variant, cls.PRIMARY_COLOR),
            font=cls.BODY_FONT,
            corner_radius=8,
            **kwargs
        )
    
    @classmethod
    def create_entry(cls, parent, placeholder="", **kwargs):
        return ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            height=cls.INPUT_HEIGHT,
            font=cls.BODY_FONT,
            corner_radius=8,
            **kwargs
        )
    
    @classmethod
    def create_label(cls, parent, text, variant="body", **kwargs):
        fonts = {
            "title": cls.TITLE_FONT,
            "heading": cls.HEADING_FONT,
            "subheading": cls.SUBHEADING_FONT,
            "body": cls.BODY_FONT,
            "small": cls.SMALL_FONT
        }
        
        return ctk.CTkLabel(
            parent,
            text=text,
            font=fonts.get(variant, cls.BODY_FONT),
            **kwargs
        )

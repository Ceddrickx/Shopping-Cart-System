# ============================================================
# gui.py
# NUmart - Study smart. Shop smart.
# CustomTkinter GUI entry point.
# Run this file to launch the graphical interface.
# Requires: customtkinter, Pillow (pip install customtkinter pillow)
# ============================================================

import customtkinter as ctk
from tkinter import messagebox, StringVar
import tkinter as tk

import os
import datetime
import math

from system import NUmart
from structures import Stack

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ─────────────────────────────────────────
# THEME & PALETTE
# ─────────────────────────────────────────

THEME = {
    "bg": ("#F0F4F8", "#0B0E14"),
    "surface": ("#FFFFFF", "#151A22"),
    "card": ("#F8FAFC", "#1E2530"),
    "border": ("#E2E8F0", "#334155"),
    "text": ("#0F172A", "#F8FAFC"),
    "sub": ("#64748B", "#94A3B8"),
    "navy": ("#0B3D91", "#0B3D91"),
    "navy_dark": ("#072458", "#072458"),
    "navy_hover": ("#1A52B5", "#1A52B5"),
    "gold": ("#FFC72C", "#FFC72C"),
    "gold_hover": ("#FFD659", "#FFD659"),
    "gold_dim": ("#E5A91A", "#E5A91A"),
    "white": ("#FFFFFF", "#FFFFFF"),
    "success": ("#10B981", "#10B981"),
    "error": ("#EF4444", "#EF4444"),
    "warning": ("#F59E0B", "#F59E0B"),
    "info": ("#3B82F6", "#3B82F6"),
    "transparent": "transparent",
    # Static dark keys for screens that are forced dark
    "dark_bg": ("#0B0E14", "#0B0E14"),
    "dark_surface": ("#151A22", "#151A22"),
    "dark_card": ("#1E2530", "#1E2530"),
    "dark_border": ("#334155", "#334155"),
    "dark_text": ("#F8FAFC", "#F8FAFC"),
    "dark_sub": ("#94A3B8", "#94A3B8"),
}

FONT_FAMILY = "Segoe UI"

def get_font(size, weight="normal"):
    return ctk.CTkFont(family=FONT_FAMILY, size=size, weight=weight)


# ─────────────────────────────────────────
# UTILITY HELPERS
# ─────────────────────────────────────────



# ─────────────────────────────────────────
# REUSABLE WIDGET COMPONENTS
# ─────────────────────────────────────────

class StatusLabel(ctk.CTkLabel):
    """Inline colored status/feedback label that auto-clears after a delay."""

    def __init__(self, master, **kwargs):
        super().__init__(master, text="", font=get_font(12), **kwargs)
        self._after_id = None

    def show(self, message, kind="info", duration=4000):
        if not self.winfo_exists(): return
        color_map = {
            "success": THEME["success"],
            "error":   THEME["error"],
            "warning": THEME["warning"],
            "info":    THEME["info"],
        }
        self.configure(text=message, text_color=color_map.get(kind, THEME["info"]))
        if self._after_id:
            self.after_cancel(self._after_id)
        self._after_id = self.after(duration, self.clear)

    def clear(self):
        if self.winfo_exists():
            self.configure(text="")


class SectionHeader(ctk.CTkLabel):
    """Bold page section title."""

    def __init__(self, master, text, **kwargs):
        super().__init__(
            master,
            text=text,
            font=get_font(24, "bold"),
            text_color=THEME["navy"],
            **kwargs
        )


class DashboardSummary(ctk.CTkFrame):
    """Row of statistical cards to fill empty space and display POS summary statistics."""

    def __init__(self, master, store, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.store = store
        self._build()

    def _build(self):
        # Compute stats dynamically from the linked list
        total_items = 0
        low_stock = 0
        categories = set()

        node = self.store.inventory.head
        while node:
            total_items += 1
            if node.quantity <= 10:
                low_stock += 1
            if node.category:
                categories.add(node.category)
            node = node.next

        # 3 slick modern cards side-by-side
        card1 = ctk.CTkFrame(self, fg_color=THEME["card"], corner_radius=16, border_width=1, border_color=THEME["border"])
        card1.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ctk.CTkLabel(card1, text="📦 Total Products", font=get_font(14, "bold"), text_color=THEME["sub"]).pack(anchor="w", padx=20, pady=(15, 2))
        ctk.CTkLabel(card1, text=str(total_items), font=get_font(32, "bold"), text_color=THEME["navy"]).pack(anchor="w", padx=20, pady=(0, 15))

        card2 = ctk.CTkFrame(self, fg_color=THEME["card"], corner_radius=16, border_width=1, border_color=THEME["border"])
        card2.pack(side="left", fill="both", expand=True, padx=10)
        ctk.CTkLabel(card2, text="⚠️ Low Stock Items", font=get_font(14, "bold"), text_color=THEME["sub"]).pack(anchor="w", padx=20, pady=(15, 2))
        ctk.CTkLabel(card2, text=str(low_stock), font=get_font(32, "bold"), text_color=THEME["error"] if low_stock > 0 else THEME["success"]).pack(anchor="w", padx=20, pady=(0, 15))

        card3 = ctk.CTkFrame(self, fg_color=THEME["card"], corner_radius=16, border_width=1, border_color=THEME["border"])
        card3.pack(side="left", fill="both", expand=True, padx=(10, 0))
        ctk.CTkLabel(card3, text="🏷️ Categories", font=get_font(14, "bold"), text_color=THEME["sub"]).pack(anchor="w", padx=20, pady=(15, 2))
        ctk.CTkLabel(card3, text=str(len(categories)), font=get_font(32, "bold"), text_color=THEME["text"]).pack(anchor="w", padx=20, pady=(0, 15))


class GoldButton(ctk.CTkButton):
    """Primary gold action button."""

    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", THEME["gold"])
        kwargs.setdefault("hover_color", THEME["gold_hover"])
        kwargs.setdefault("text_color", THEME["navy_dark"])
        kwargs.setdefault("font", (FONT_FAMILY, 14, "bold"))
        kwargs.setdefault("corner_radius", 18)
        kwargs.setdefault("height", 40)
        super().__init__(master, **kwargs)


class NavyButton(ctk.CTkButton):
    """Secondary navy action button."""

    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", THEME["navy"])
        kwargs.setdefault("hover_color", THEME["navy_hover"])
        kwargs.setdefault("text_color", THEME["white"])
        kwargs.setdefault("font", (FONT_FAMILY, 14, "bold"))
        kwargs.setdefault("corner_radius", 18)
        kwargs.setdefault("height", 40)
        super().__init__(master, **kwargs)


class DangerButton(ctk.CTkButton):
    """Red destructive action button."""

    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", THEME["error"])
        kwargs.setdefault("hover_color", "#DC2626")
        kwargs.setdefault("text_color", THEME["white"])
        kwargs.setdefault("font", (FONT_FAMILY, 14, "bold"))
        kwargs.setdefault("corner_radius", 18)
        kwargs.setdefault("height", 40)
        super().__init__(master, **kwargs)


class StatCard(ctk.CTkFrame):
    """Small stat display card with label and value."""

    def __init__(self, master, label, value, icon="", mode="dark", **kwargs):
        kwargs.setdefault("fg_color", THEME["card"])
        kwargs.setdefault("corner_radius", 10)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", THEME["border"])
        super().__init__(master, **kwargs)

        ctk.CTkLabel(self, text=f"{icon}  {label}", font=get_font(11),
                     text_color=THEME["sub"]).pack(anchor="w", padx=14, pady=(10, 0))
        self.value_label = ctk.CTkLabel(self, text=value,
                                        font=get_font(18, "bold"),
                                        text_color=THEME["gold"])
        self.value_label.pack(anchor="w", padx=14, pady=(2, 10))

    def update_value(self, value):
        self.value_label.configure(text=value)


# ─────────────────────────────────────────
# LANDING SCREEN
# ─────────────────────────────────────────

class LandingScreen(ctk.CTkFrame):
    """Role-selection screen shown at startup and on logout."""

    def __init__(self, master, on_customer, on_admin, mode_var):
        super().__init__(master, fg_color="transparent")
        self.on_customer = on_customer
        self.on_admin    = on_admin
        self.mode_var    = mode_var
        self._build()

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ── Branding block ──
        brand_frame = ctk.CTkFrame(self, fg_color="transparent")
        brand_frame.grid(row=1, column=0, pady=(0, 10))

        # Gold top accent line
        ctk.CTkFrame(brand_frame, height=5, width=200,
                     fg_color=THEME["gold"], corner_radius=3).pack(pady=(0, 18))

        self._logo_placeholder(brand_frame)

        ctk.CTkLabel(brand_frame, text="NUmart",
                     font=get_font(42, "bold"),
                     text_color=THEME["gold"]).pack()
        ctk.CTkLabel(brand_frame, text="Study smart. Shop smart.",
                     font=get_font(14),
                     text_color=THEME["sub"]).pack(pady=(2, 0))

        ctk.CTkFrame(brand_frame, height=2, width=200,
                     fg_color=THEME["gold"], corner_radius=1).pack(pady=(18, 0))

        # ── Role cards ──
        role_frame = ctk.CTkFrame(self, fg_color="transparent")
        role_frame.grid(row=2, column=0, pady=28)

        self._role_card(role_frame, 0, "🛍️", "Shop as Customer",
                        "Browse and purchase school supplies",
                        self.on_customer)

        # divider
        ctk.CTkFrame(role_frame, width=2, height=120,
                     fg_color=THEME["border"]).grid(row=0, column=1, padx=24)

        self._role_card(role_frame, 2, "🔧", "Manage as Admin",
                        "Inventory and store management",
                        self._prompt_admin_pin)

        # ── Mode toggle ──
        toggle_frame = ctk.CTkFrame(self, fg_color="transparent")
        toggle_frame.grid(row=3, column=0, pady=(0, 30), sticky="s")

        ctk.CTkLabel(toggle_frame, text="☀️",
                     font=get_font(14)).pack(side="left", padx=(0, 6))
        ctk.CTkSwitch(toggle_frame, text="", variable=self.mode_var,
                      onvalue="dark", offvalue="light",
                      command=self._on_toggle,
                      width=46, height=22,
                      fg_color=THEME["navy"],
                      progress_color=THEME["navy_dark"],
                      button_color=THEME["gold"],
                      button_hover_color=THEME["gold_hover"]).pack(side="left")
        ctk.CTkLabel(toggle_frame, text="🌙",
                     font=get_font(14)).pack(side="left", padx=(6, 0))

    def _logo_placeholder(self, parent):
        """Draw a simple NU placeholder badge when no logo image is found."""
        badge = ctk.CTkFrame(parent, width=80, height=80,
                             fg_color=THEME["navy"], corner_radius=40)
        badge.pack(pady=(0, 12))
        badge.pack_propagate(False)
        ctk.CTkLabel(badge, text="NU", font=get_font(26, "bold"),
                     text_color=THEME["gold"]).place(relx=0.5, rely=0.5, anchor="center")

    def _role_card(self, parent, col, icon, title, subtitle, command):
        """Build a clickable role selection card."""
        card = ctk.CTkFrame(parent, width=220, height=150,
                            fg_color=THEME["card"],
                            corner_radius=14,
                            border_width=2,
                            border_color=THEME["border"],
                            cursor="hand2")
        card.grid(row=0, column=col, padx=4)
        card.pack_propagate(False)

        ctk.CTkLabel(card, text=icon, font=get_font(32)).pack(pady=(22, 6))
        ctk.CTkLabel(card, text=title, font=get_font(14, "bold"),
                     text_color=THEME["text"]).pack()
        ctk.CTkLabel(card, text=subtitle, font=get_font(11),
                     text_color=THEME["sub"]).pack(pady=(3, 0))

        # hover effect
        def on_enter(e):
            card.configure(border_color=THEME["gold"], fg_color=THEME["navy"])
        def on_leave(e):
            card.configure(border_color=THEME["border"], fg_color=THEME["card"])

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card.bind("<Button-1>", lambda e: command())
        for child in card.winfo_children():
            child.bind("<Button-1>", lambda e: command())

    def _on_toggle(self):
        mode = self.mode_var.get()
        ctk.set_appearance_mode(mode)

    def _prompt_admin_pin(self):
        """Show PIN dialog before entering admin mode."""
        dialog = PinDialog(self, on_success=self.on_admin)
        dialog.grab_set()


# ─────────────────────────────────────────
# PIN DIALOG
# ─────────────────────────────────────────

class PinDialog(ctk.CTkToplevel):
    """Modal PIN entry dialog for Admin login. 3 attempts max."""

    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.transient(parent)
        self.attributes("-topmost", True)
        self.focus_force()
        self.on_success = on_success
        self.attempts   = 3
        self.title("Admin Login")
        self.geometry("340x260")
        self.resizable(False, False)
        self._build()
        # center on parent
        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width()  // 2 - 170
        py = parent.winfo_rooty() + parent.winfo_height() // 2 - 130
        self.geometry(f"+{px}+{py}")

    def _build(self):
        self.configure(fg_color=THEME["dark_surface"])

        ctk.CTkFrame(self, height=5, fg_color=THEME["gold"],
                     corner_radius=0).pack(fill="x")

        ctk.CTkLabel(self, text="🔒  Admin Login",
                     font=get_font(16, "bold"),
                     text_color=THEME["white"]).pack(pady=(20, 4))
        ctk.CTkLabel(self, text="Enter your 4-digit Admin PIN",
                     font=get_font(12),
                     text_color=THEME["dark_sub"]).pack()

        self.pin_var = StringVar()
        self.entry = ctk.CTkEntry(self, textvariable=self.pin_var,
                                  show="●", width=160,
                                  font=get_font(18),
                                  justify="center",
                                  height=42)
        self.entry.pack(pady=18)
        self.entry.bind("<Return>", lambda e: self._submit())
        self.entry.focus()

        self.status = StatusLabel(self, fg_color="transparent")
        self.status.pack()

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=(10, 0))

        GoldButton(btn_row, text="Login", width=100,
                   command=self._submit).pack(side="left", padx=6)
        NavyButton(btn_row, text="Cancel", width=100,
                   command=self.destroy).pack(side="left", padx=6)

    def _submit(self):
        from system import ADMIN_PIN
        pin = self.pin_var.get().strip()
        if pin == ADMIN_PIN:
            self.destroy()
            self.on_success()
        else:
            self.attempts -= 1
            self.pin_var.set("")
            if self.attempts > 0:
                self.status.show(
                    f"❌  Incorrect PIN — {self.attempts} attempt(s) left.", "error")
            else:
                self.status.show("🚫  Access denied.", "error")
                self.after(1500, lambda: self.destroy() if self.winfo_exists() else None)


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────

class Sidebar(ctk.CTkFrame):
    """
    Left navigation sidebar.
    Slim (60px) with icon + hover-expand to full (160px).
    Hides admin items in customer mode.
    """

    NAV_ITEMS_CUSTOMER = [
        ("🏪", "Browse",  "browse"),
        ("🛒", "Cart",    "cart"),
        ("🎁", "Promo",   "promo"),
        ("💳", "Payment", "payment"),
        ("📋", "History", "history"),
    ]
    NAV_ITEMS_ADMIN = [
        ("📦", "Inventory", "inventory"),
        ("➕", "Add Item",  "add_item"),
        ("✏️",  "Update",   "update_item"),
        ("🗑️", "Delete",   "delete_item"),
        ("🔍", "Search",   "search_item"),
    ]

    def __init__(self, master, role, mode_var, on_navigate, on_logout, **kwargs):
        super().__init__(master, width=160, fg_color=THEME["navy"],
                         corner_radius=0, **kwargs)
        self.role         = role
        self.mode_var     = mode_var
        self.on_navigate  = on_navigate
        self.on_logout    = on_logout
        self.active_page  = None
        self._buttons     = {}
        self._build()

    def _build(self):
        self.pack_propagate(False)

        logo_frame = ctk.CTkFrame(self, fg_color=THEME["navy_dark"],
                                  height=70, corner_radius=0)
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)

        self._logo_lbl = ctk.CTkLabel(logo_frame, text="NUmart", font=get_font(18, "bold"),
                     text_color=THEME["gold"])
        self._logo_lbl.place(relx=0.5, rely=0.5, anchor="center")

        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="both", expand=True, pady=(8, 0))

        items = (self.NAV_ITEMS_CUSTOMER if self.role == "customer"
                 else self.NAV_ITEMS_ADMIN)

        for icon, label, page in items:
            btn = self._make_nav_btn(nav_frame, icon, label, page)
            btn.pack(fill="x", pady=2, padx=6)
            self._buttons[page] = btn

        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(fill="x", pady=(0, 10))

        toggle_row = ctk.CTkFrame(bottom, fg_color="transparent", height=36)
        toggle_row.pack(fill="x", padx=6, pady=(0, 4))
        toggle_row.pack_propagate(False)
        self._toggle_sw = ctk.CTkSwitch(
            toggle_row, text=" Dark" if self.mode_var.get() == "dark" else " Light", variable=self.mode_var,
            onvalue="dark", offvalue="light",
            command=self._on_toggle,
            width=38, height=18,
            fg_color=THEME["navy_dark"],
            progress_color=THEME["navy_dark"],
            button_color=THEME["gold"],
            button_hover_color=THEME["gold_hover"])
        self._toggle_sw.place(relx=0.5, rely=0.5, anchor="center")

        logout_btn = ctk.CTkButton(
            bottom, text="⏻", font=get_font(18),
            fg_color="transparent", hover_color=THEME["navy_hover"],
            text_color=THEME["white"], height=36,
            command=self._confirm_logout, corner_radius=8)
        logout_btn.pack(fill="x", padx=6)

        if self.role == "customer":
            self._cart_strip = ctk.CTkFrame(self, fg_color=THEME["navy_dark"],
                                            height=38, corner_radius=0)
            self._cart_strip.pack(fill="x", side="bottom")
            self._cart_strip.pack_propagate(False)
            self.cart_lbl = ctk.CTkLabel(
                self._cart_strip, text="₱0.00",
                font=get_font(12, "bold"),
                text_color=THEME["gold"])
            self.cart_lbl.place(relx=0.5, rely=0.5, anchor="center")

    def _nav_logo_text(self, parent):
        ctk.CTkLabel(parent, text="NU", font=get_font(18, "bold"),
                     text_color=THEME["gold"]).place(relx=0.5, rely=0.5, anchor="center")

    def _make_nav_btn(self, parent, icon, label, page):
        padding = "    " if len(icon) == 1 else "  "
        btn = ctk.CTkButton(
            parent,
            text=f"{icon}{padding}{label}",
            font=get_font(14, "bold"),
            fg_color="transparent",
            hover_color=THEME["navy_hover"],
            text_color=THEME["sub"],
            anchor="w",
            height=44,
            corner_radius=12,
            command=lambda p=page: self.on_navigate(p)
        )
        self._buttons[page] = btn
        return btn

    def set_active(self, page):
        """Highlight the active nav button."""
        for p, btn in self._buttons.items():
            if p == page:
                btn.configure(fg_color=THEME["gold"],
                              text_color=THEME["navy_dark"])
            else:
                btn.configure(fg_color="transparent",
                              text_color=THEME["sub"])
        self.active_page = page

    def update_cart_total(self, total):
        if hasattr(self, "cart_lbl"):
            self.cart_lbl.configure(text=f"₱{total:.2f}")

    def _on_toggle(self):
        mode = self.mode_var.get()
        ctk.set_appearance_mode(mode)
        if hasattr(self, "_toggle_sw"):
            self._toggle_sw.configure(text=" Dark" if mode == "dark" else " Light")

    def _confirm_logout(self):
        dialog = LogoutConfirmDialog(self, on_confirm=self.on_logout)
        dialog.grab_set()


# ─────────────────────────────────────────
# LOGOUT CONFIRMATION DIALOG
# ─────────────────────────────────────────

class LogoutConfirmDialog(ctk.CTkToplevel):
    """Confirmation popup before logout to prevent accidental misclick."""

    def __init__(self, parent, on_confirm):
        super().__init__(parent)
        self.transient(parent)
        self.attributes("-topmost", True)
        self.focus_force()
        self.on_confirm = on_confirm
        self.title("Confirm Logout")
        self.geometry("320x180")
        self.resizable(False, False)
        self._build()
        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width()  // 2 - 160
        py = parent.winfo_rooty() + parent.winfo_height() // 2 - 90
        self.geometry(f"+{px}+{py}")

    def _build(self):
        self.configure(fg_color=THEME["dark_surface"])
        ctk.CTkFrame(self, height=5, fg_color=THEME["gold"],
                     corner_radius=0).pack(fill="x")
        ctk.CTkLabel(self, text="⏻  Logout",
                     font=get_font(16, "bold"),
                     text_color=THEME["white"]).pack(pady=(20, 6))
        ctk.CTkLabel(self, text="Are you sure you want to go back\nto the role selection screen?",
                     font=get_font(12),
                     text_color=THEME["dark_sub"],
                     justify="center").pack()
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(pady=20)
        GoldButton(row, text="Yes, Logout", width=120,
                   command=self._confirm).pack(side="left", padx=8)
        NavyButton(row, text="Cancel", width=100,
                   command=self.destroy).pack(side="left", padx=8)

    def _confirm(self):
        self.destroy()
        self.on_confirm()


# ─────────────────────────────────────────
# CONTENT PAGES — BASE
# ─────────────────────────────────────────

class BasePage(ctk.CTkFrame):
    """Base class for all content pages. Handles theming."""

    def __init__(self, master, store, mode_var, refresh_cart_cb=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.store          = store
        self.mode_var       = mode_var
        self.refresh_cart   = refresh_cart_cb or (lambda: None)



    def on_show(self):
        """Called each time the page becomes visible. Override to refresh data."""
        pass


# ─────────────────────────────────────────
# PAGE: BROWSE INVENTORY
# ─────────────────────────────────────────

class BrowsePage(BasePage):

    def __init__(self, master, store, mode_var, refresh_cart_cb, **kwargs):
        super().__init__(master, store, mode_var, refresh_cart_cb, **kwargs)
        self._build()

    def _build(self):

        SectionHeader(self, text="🏪  Browse Inventory").pack(anchor="w", padx=24, pady=(20, 4))
        ctk.CTkLabel(self, text="All available school supplies",
                     font=get_font(12), text_color=THEME["sub"]).pack(anchor="w", padx=24)

        # Statistical summary section to eliminate blank spaces
        DashboardSummary(self, self.store).pack(fill="x", padx=24, pady=(12, 4))

        # Search bar
        search_row = ctk.CTkFrame(self, fg_color="transparent")
        search_row.pack(fill="x", padx=24, pady=(12, 8))
        self.search_var = StringVar()
        ctk.CTkEntry(search_row, textvariable=self.search_var,
                     placeholder_text="Search by name or ID...",
                     width=300, height=36,
                     font=get_font(13)).pack(side="left")
        GoldButton(search_row, text="🔍 Search", width=100,
                   command=self._refresh_table).pack(side="left", padx=8)
        NavyButton(search_row, text="↺ Reset", width=80,
                   command=self._reset_search).pack(side="left")

        # Table frame
        table_frame = ctk.CTkFrame(self, fg_color=THEME["surface"],
                                   corner_radius=10, border_width=1,
                                   border_color=THEME["border"])
        table_frame.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        # Column headers
        headers = ["ID", "Name", "Category", "Price", "Qty", "Expiration", "Action"]
        widths   = [50, 190, 100, 90, 60, 110, 80]
        hdr_row  = ctk.CTkFrame(table_frame, fg_color=THEME["navy"], corner_radius=8)
        hdr_row.pack(fill="x", padx=6, pady=(6, 0))
        for h, w in zip(headers, widths):
            ctk.CTkLabel(hdr_row, text=h, width=w,
                         font=get_font(12, "bold"),
                         text_color=THEME["gold"]).pack(side="left", padx=4, pady=6)

        # Scrollable rows
        self.scroll_frame = ctk.CTkScrollableFrame(table_frame,
                                                   fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=6, pady=6)

        self.status = StatusLabel(self, fg_color="transparent")
        self.status.pack(anchor="w", padx=24, pady=(0, 8))

        self._refresh_table()

    def _reset_search(self):
        self.search_var.set("")
        self._refresh_table()

    def on_show(self):
        pass

    def _refresh_table(self):
        # clear existing rows
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        keyword = self.search_var.get().strip().lower()
        items   = []
        node    = self.store.inventory.head
        while node:
            if (not keyword or
                    keyword in node.name.lower() or
                    keyword in node.item_id):
                items.append(node)
            node = node.next

        if not items:
            ctk.CTkLabel(self.scroll_frame, text="No items found.",
                         font=get_font(13),
                         text_color=THEME["sub"]).pack(pady=20)
            return

        widths = [50, 190, 100, 90, 60, 110, 80]
        for i, item in enumerate(items):
            row_color = THEME["card"] if i % 2 == 0 else THEME["surface"]
            row = ctk.CTkFrame(self.scroll_frame, fg_color=row_color,
                               corner_radius=12, height=46)
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)

            price_str = (f"₱{item.price:.2f}/10" if "Bond Paper" in item.name
                         else f"₱{item.price:.2f}")
            qty_color = THEME["error"] if item.quantity == 0 else THEME["text"]

            values = [item.item_id, item.name, item.category,
                      price_str, str(item.quantity), item.expiration]
            colors = [THEME["sub"], THEME["text"], THEME["sub"],
                      THEME["gold"], qty_color, THEME["sub"]]

            for val, w, col in zip(values, widths, colors):
                ctk.CTkLabel(row, text=val, width=w,
                             font=get_font(12),
                             text_color=col,
                             anchor="w").pack(side="left", padx=4)

            # ADD button per row
            add_btn = ctk.CTkButton(
                row, text="+ Add", width=widths[-1] - 10, height=32,
                fg_color="transparent",
                border_width=2, border_color=THEME["gold"],
                text_color=THEME["gold"],
                hover_color=THEME["gold_hover"],
                font=get_font(12, "bold"),
                corner_radius=16,
                command=lambda it=item: self._add_dialog(it)
            )
            add_btn.pack(side="left", padx=4)
            if item.quantity == 0:
                add_btn.configure(state="disabled",
                                  border_color=THEME["border"],
                                  text_color=THEME["sub"],
                                  text="Out")

    def _add_dialog(self, item):
        dialog = AddToCartDialog(self, item, self.store,
                                 on_done=self._on_add_done)
        dialog.grab_set()

    def _on_add_done(self, msg, kind):
        self.status.show(msg, kind)
        self.refresh_cart()
        self._refresh_table()


# ─────────────────────────────────────────
# ADD TO CART DIALOG
# ─────────────────────────────────────────

class AddToCartDialog(ctk.CTkToplevel):
    """Quantity input dialog for adding an item to cart."""

    def __init__(self, parent, item, store, on_done):
        super().__init__(parent)
        self.transient(parent)
        self.attributes("-topmost", True)
        self.focus_force()
        self.item    = item
        self.store   = store
        self.on_done = on_done
        self.title(f"Add — {item.name}")
        self.geometry("340x260")
        self.resizable(False, False)
        self._build()
        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width()  // 2 - 170
        py = parent.winfo_rooty() + parent.winfo_height() // 2 - 130
        self.geometry(f"+{px}+{py}")

    def _build(self):
        self.configure(fg_color=THEME["dark_surface"])
        ctk.CTkFrame(self, height=5, fg_color=THEME["gold"],
                     corner_radius=0).pack(fill="x")

        ctk.CTkLabel(self, text=f"➕  Add to Cart",
                     font=get_font(16, "bold"),
                     text_color=THEME["white"]).pack(pady=(16, 2))

        ctk.CTkLabel(self, text=self.item.name,
                     font=get_font(13),
                     text_color=THEME["gold"]).pack()

        cart_item  = self.store.cart.search(self.item.item_id)
        in_cart    = cart_item.quantity if cart_item else 0
        available  = self.item.quantity - in_cart

        info = f"₱{self.item.price:.2f}  ·  Available: {available}"
        ctk.CTkLabel(self, text=info, font=get_font(11),
                     text_color=THEME["dark_sub"]).pack(pady=(2, 12))

        self.qty_var = StringVar(value="1")
        ctk.CTkEntry(self, textvariable=self.qty_var,
                     width=140, height=44, justify="center",
                     font=get_font(20, "bold"),
                     corner_radius=22, border_width=2,
                     border_color=THEME["gold"]).pack(pady=(4, 0))
        self.update_idletasks()

        self.status = StatusLabel(self, fg_color="transparent")
        self.status.pack(pady=(8, 0))

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(pady=14)
        GoldButton(row, text="Add to Cart", width=120,
                   command=self._submit).pack(side="left", padx=6)
        NavyButton(row, text="Cancel", width=90,
                   command=self.destroy).pack(side="left", padx=6)

        self.bind("<Return>", lambda e: self._submit())

    def _submit(self):
        raw = self.qty_var.get().strip()
        try:
            qty = int(raw)
            if qty <= 0:
                self.status.show("Quantity must be at least 1.", "error")
                return
        except ValueError:
            self.status.show("Please enter a whole number.", "error")
            return

        result = self.store.add_to_cart(self.item.item_id, qty)
        if result is True:
            self.destroy()
            self.on_done(f"✓  {qty}x '{self.item.name}' added to cart.", "success")
        elif result == "maxed":
            self.on_done(f"✗  '{self.item.name}' is maxed out in your cart.", "error")
            self.destroy()
        else:
            cart_item = self.store.cart.search(self.item.item_id)
            in_cart   = cart_item.quantity if cart_item else 0
            avail     = self.item.quantity - in_cart
            self.status.show(
                f"Only {avail} available. Try a smaller quantity.", "error")


# ─────────────────────────────────────────
# PAGE: SHOPPING CART
# ─────────────────────────────────────────

class CartPage(BasePage):

    def __init__(self, master, store, mode_var, refresh_cart_cb, **kwargs):
        super().__init__(master, store, mode_var, refresh_cart_cb, **kwargs)
        self._build()

    def _build(self):
        SectionHeader(self, text="🛒  Shopping Cart").pack(anchor="w", padx=24, pady=(20, 4))
        ctk.CTkLabel(self, text="Items you've selected",
                     font=get_font(12),
                     text_color=THEME["sub"]).pack(anchor="w", padx=24)

        # Action bar
        action_row = ctk.CTkFrame(self, fg_color="transparent")
        action_row.pack(fill="x", padx=24, pady=(12, 8))
        NavyButton(action_row, text="↩ Undo Last", width=120,
                   command=self._undo).pack(side="left", padx=(0, 8))
        DangerButton(action_row, text="🗑 Remove Item", width=130,
                     command=self._remove_dialog).pack(side="left")

        # Cart table
        table_frame = ctk.CTkFrame(self, fg_color=THEME["surface"],
                                   corner_radius=10, border_width=1,
                                   border_color=THEME["border"])
        table_frame.pack(fill="both", expand=True, padx=24, pady=(0, 10))

        headers = ["ID", "Name", "Category", "Unit Price", "Qty", "Subtotal"]
        widths   = [50, 190, 100, 100, 60, 110]
        hdr_row  = ctk.CTkFrame(table_frame, fg_color=THEME["navy"], corner_radius=8)
        hdr_row.pack(fill="x", padx=6, pady=(6, 0))
        for h, w in zip(headers, widths):
            ctk.CTkLabel(hdr_row, text=h, width=w,
                         font=get_font(12, "bold"),
                         text_color=THEME["gold"]).pack(side="left", padx=4, pady=6)

        self.scroll_frame = ctk.CTkScrollableFrame(table_frame,
                                                   fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=6, pady=6)

        # Total bar
        self.total_bar = ctk.CTkFrame(self, fg_color=THEME["navy_dark"],
                                      height=48, corner_radius=10)
        self.total_bar.pack(fill="x", padx=24, pady=(0, 6))
        self.total_bar.pack_propagate(False)
        self.total_lbl = ctk.CTkLabel(self.total_bar, text="Cart Total: ₱0.00",
                                      font=get_font(14, "bold"),
                                      text_color=THEME["gold"])
        self.total_lbl.pack(side="right", padx=20)
        self.promo_lbl = ctk.CTkLabel(self.total_bar, text="",
                                      font=get_font(12),
                                      text_color=THEME["white"])
        self.promo_lbl.pack(side="left", padx=20)

        self.status = StatusLabel(self, fg_color="transparent")
        self.status.pack(anchor="w", padx=24, pady=(0, 8))

    def on_show(self):
        self._refresh_table()

    def _refresh_table(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()
        items = list(self.store.cart.iter_items())

        if not items:
            ctk.CTkLabel(self.scroll_frame, text="Your cart is empty.",
                         font=get_font(13),
                         text_color=THEME["sub"]).pack(pady=20)
            self.total_lbl.configure(text="Cart Total: ₱0.00")
            self.promo_lbl.configure(text="")
            self.refresh_cart()
            return

        widths = [50, 190, 100, 100, 60, 110]
        for i, item in enumerate(items):
            row_color = THEME["card"] if i % 2 == 0 else THEME["surface"]
            row = ctk.CTkFrame(self.scroll_frame, fg_color=row_color,
                               corner_radius=6, height=38)
            row.pack(fill="x", pady=1)
            row.pack_propagate(False)
            values = [item["item_id"], item["name"], item["category"],
                      f"₱{item['price']:.2f}", str(item["qty"]),
                      f"₱{item['subtotal']:.2f}"]
            colors = [THEME["sub"], THEME["text"], THEME["sub"],
                      THEME["text"], THEME["text"], THEME["gold"]]
            for val, w, col in zip(values, widths, colors):
                ctk.CTkLabel(row, text=val, width=w,
                             font=get_font(12),
                             text_color=col,
                             anchor="w").pack(side="left", padx=4)

        total, disc, final = self.store.get_final_total()
        self.total_lbl.configure(
            text=f"Total: ₱{final:.2f}" + (f"  (after {self.store.discount}% off)" if self.store.discount else ""))
        if self.store.promo_used:
            self.promo_lbl.configure(
                text=f"Promo: {self.store.promo_used} (-₱{disc:.2f})")
        else:
            self.promo_lbl.configure(text="")
        self.refresh_cart()

    def _undo(self):
        if self.store.undo_stack.is_empty():
            self.status.show("Nothing to undo.", "warning")
            return
        last = self.store.undo_stack.peek()
        action = last["action"]
        name   = last["name"]
        qty    = last["quantity"]

        self.store.undo_last_action()
        verb = f"removed {qty}x '{name}'" if action == "ADD" else f"restored '{name}'"
        self.status.show(f"↩  Undo: {verb}.", "success")
        self._refresh_table()

    def _remove_dialog(self):
        if self.store.cart.is_empty():
            self.status.show("Your cart is empty.", "warning")
            return
        dialog = RemoveFromCartDialog(self, self.store, on_done=self._on_removed)
        dialog.grab_set()

    def _on_removed(self, msg, kind):
        self.status.show(msg, kind)
        self._refresh_table()


# ─────────────────────────────────────────
# REMOVE FROM CART DIALOG
# ─────────────────────────────────────────

class RemoveFromCartDialog(ctk.CTkToplevel):
    """Dialog for choosing which cart item to remove."""

    def __init__(self, parent, store, on_done):
        super().__init__(parent)
        self.transient(parent)
        self.attributes("-topmost", True)
        self.focus_force()
        self.store   = store
        self.on_done = on_done
        self.title("Remove Item")
        self.geometry("380x300")
        self.resizable(False, False)
        self._build()
        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width()  // 2 - 190
        py = parent.winfo_rooty() + parent.winfo_height() // 2 - 150
        self.geometry(f"+{px}+{py}")

    def _build(self):
        self.configure(fg_color=THEME["dark_surface"])
        ctk.CTkFrame(self, height=5, fg_color=THEME["error"],
                     corner_radius=0).pack(fill="x")
        ctk.CTkLabel(self, text="🗑  Remove Item from Cart",
                     font=get_font(15, "bold"),
                     text_color=THEME["white"]).pack(pady=(16, 4))

        self.selected_id = StringVar()
        items = list(self.store.cart.iter_items())

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", height=150)
        scroll.pack(fill="x", padx=16, pady=4)

        for item in items:
            row = ctk.CTkFrame(scroll, fg_color=THEME["dark_card"],
                               corner_radius=6)
            row.pack(fill="x", pady=2)
            rb = ctk.CTkRadioButton(
                row,
                text=f"[{item['item_id']}] {item['name']}  ×{item['qty']}",
                variable=self.selected_id,
                value=item["item_id"],
                font=get_font(12),
                text_color=THEME["white"],
                fg_color=THEME["gold"],
                hover_color=THEME["gold_hover"])
            rb.pack(anchor="w", padx=10, pady=6)

        self.status = StatusLabel(self, fg_color="transparent")
        self.status.pack()

        row_btns = ctk.CTkFrame(self, fg_color="transparent")
        row_btns.pack(pady=12)
        DangerButton(row_btns, text="Remove", width=110,
                     command=self._confirm).pack(side="left", padx=6)
        NavyButton(row_btns, text="Cancel", width=90,
                   command=self.destroy).pack(side="left", padx=6)

    def _confirm(self):
        item_id = self.selected_id.get()
        if not item_id:
            self.status.show("Please select an item.", "warning")
            return
        node = self.store.cart.search(item_id)
        name = node.name if node else item_id
        self.store.remove_from_cart(item_id)
        self.destroy()
        self.on_done(f"🗑  '{name}' removed from cart.", "success")


# ─────────────────────────────────────────
# PAGE: PROMO CODE
# ─────────────────────────────────────────

class PromoPage(BasePage):

    def __init__(self, master, store, mode_var, refresh_cart_cb, **kwargs):
        super().__init__(master, store, mode_var, refresh_cart_cb, **kwargs)
        self._build()

    def _build(self):
        SectionHeader(self, text="🏷️  Promo Code").pack(anchor="w", padx=24, pady=(20, 4))
        ctk.CTkLabel(self, text="Apply discount codes from NUmart flyers and social media",
                     font=get_font(12), text_color=THEME["sub"]).pack(anchor="w", padx=24)

        # Active promo card
        self.active_card = ctk.CTkFrame(self, fg_color=THEME["card"],
                                        corner_radius=10, border_width=1,
                                        border_color=THEME["border"])
        self.active_card.pack(fill="x", padx=24, pady=(20, 0))
        self.active_lbl = ctk.CTkLabel(self.active_card, text="No promo code applied",
                                       font=get_font(13),
                                       text_color=THEME["sub"])
        self.active_lbl.pack(anchor="w", padx=16, pady=12)

        # Apply form
        form = ctk.CTkFrame(self, fg_color=THEME["card"], corner_radius=10,
                            border_width=1, border_color=THEME["border"])
        form.pack(fill="x", padx=24, pady=14)

        ctk.CTkLabel(form, text="Enter Promo Code",
                     font=get_font(13, "bold"),
                     text_color=THEME["gold"]).pack(anchor="w", padx=16, pady=(14, 4))

        input_row = ctk.CTkFrame(form, fg_color="transparent")
        input_row.pack(fill="x", padx=16, pady=(0, 4))
        self.code_var = StringVar()
        self.code_entry = ctk.CTkEntry(input_row, textvariable=self.code_var,
                                       placeholder_text="e.g. STUDENT15",
                                       width=220, height=38,
                                       font=get_font(14))
        self.code_entry.pack(side="left")
        GoldButton(input_row, text="Apply", width=90,
                   command=self._apply).pack(side="left", padx=8)
        DangerButton(input_row, text="Remove", width=90,
                     command=self._remove).pack(side="left")

        self.status = StatusLabel(form, fg_color="transparent")
        self.status.pack(anchor="w", padx=16, pady=(4, 10))

        # Price summary
        self.summary_frame = ctk.CTkFrame(self, fg_color=THEME["card"],
                                          corner_radius=10, border_width=1,
                                          border_color=THEME["border"])
        self.summary_frame.pack(fill="x", padx=24, pady=(0, 14))

    def on_show(self):
        self._refresh_summary()

    def _refresh_summary(self):
        # Active promo
        if self.store.promo_used:
            self.active_lbl.configure(
                text=f"✓  {self.store.promo_used}  —  {self.store.discount}% discount applied",
                text_color=THEME["success"])
        else:
            self.active_lbl.configure(text="No promo code applied",
                                      text_color=THEME["sub"])

        # Summary
        for w in self.summary_frame.winfo_children():
            w.destroy()
        if self.store.cart.is_empty():
            ctk.CTkLabel(self.summary_frame,
                         text="Add items to your cart to see the price summary.",
                         font=get_font(12),
                         text_color=THEME["sub"]).pack(padx=16, pady=12)
            return

        total, disc, final = self.store.get_final_total()
        ctk.CTkLabel(self.summary_frame, text="Price Summary",
                     font=get_font(13, "bold"),
                     text_color=THEME["gold"]).pack(anchor="w", padx=16, pady=(14, 4))

        rows = [("Subtotal", f"₱{total:.2f}", THEME["text"])]
        if self.store.discount > 0:
            rows.append((f"Discount ({self.store.promo_used})",
                         f"-₱{disc:.2f}", THEME["success"]))
        rows.append(("Total Due", f"₱{final:.2f}", THEME["gold"]))

        for label, value, color in rows:
            r = ctk.CTkFrame(self.summary_frame, fg_color="transparent")
            r.pack(fill="x", padx=16, pady=2)
            ctk.CTkLabel(r, text=label, font=get_font(12),
                         text_color=THEME["sub"]).pack(side="left")
            ctk.CTkLabel(r, text=value, font=get_font(13, "bold"),
                         text_color=color).pack(side="right")

        ctk.CTkFrame(self.summary_frame, height=1,
                     fg_color=THEME["border"]).pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(self.summary_frame, text="",
                     height=4).pack()  # bottom padding

    def _apply(self):
        code = self.code_var.get().strip()
        if not code:
            self.status.show("Please enter a promo code.", "warning")
            return
        if self.store.apply_promo(code):
            self.status.show(f"✓  Code '{code.upper()}' applied — {self.store.discount}% off!", "success")
            self.code_var.set("")
        else:
            self.status.show(f"✗  Invalid promo code '{code}'.", "error")
        self._refresh_summary()
        self.refresh_cart()

    def _remove(self):
        if not self.store.promo_used:
            self.status.show("No promo code is currently applied.", "warning")
            return
        code = self.store.promo_used
        self.store.remove_promo()
        self.status.show(f"Promo code '{code}' removed.", "info")
        self._refresh_summary()
        self.refresh_cart()


# ─────────────────────────────────────────
# PAGE: PAYMENT
# ─────────────────────────────────────────

class PaymentPage(BasePage):

    def __init__(self, master, store, mode_var, refresh_cart_cb, **kwargs):
        super().__init__(master, store, mode_var, refresh_cart_cb, **kwargs)
        self._build()

    def _build(self):
        # Centered modern card layout to eliminate blank spaces
        card = ctk.CTkFrame(self, fg_color=THEME["card"], border_width=1, border_color=THEME["border"], corner_radius=12, width=520)
        card.pack(pady=30, fill="y", expand=True)
        card.pack_propagate(False)

        SectionHeader(card, text="💳  Payment").pack(anchor="w", padx=30, pady=(25, 4))
        ctk.CTkLabel(card, text="Complete your purchase",
                     font=get_font(12),
                     text_color=THEME["sub"]).pack(anchor="w", padx=30)

        # Price summary card
        self.summary_frame = ctk.CTkFrame(card, fg_color=THEME["surface"],
                                          corner_radius=10, border_width=1,
                                          border_color=THEME["border"])
        self.summary_frame.pack(fill="x", padx=30, pady=(16, 12))

        # Payment method selector
        method_frame = ctk.CTkFrame(card, fg_color=THEME["surface"],
                                    corner_radius=10, border_width=1,
                                    border_color=THEME["border"])
        method_frame.pack(fill="x", padx=30, pady=(0, 12))

        ctk.CTkLabel(method_frame, text="Select Payment Method",
                     font=get_font(13, "bold"),
                     text_color=THEME["gold"]).pack(anchor="w", padx=16, pady=(14, 8))

        self.method_var = StringVar(value="Cash")
        methods = [("💵", "Cash"), ("💳", "Card"), ("📱", "E-Wallet")]
        btn_row = ctk.CTkFrame(method_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=(0, 14))

        for icon, method in methods:
            rb = ctk.CTkRadioButton(
                btn_row, text=f"{icon}  {method}",
                variable=self.method_var, value=method,
                font=get_font(13),
                fg_color=THEME["gold"],
                hover_color=THEME["gold_hover"],
                command=self._on_method_change)
            rb.pack(side="left", padx=10)

        # Dynamic input area
        self.input_frame = ctk.CTkFrame(card, fg_color=THEME["surface"],
                                        corner_radius=10, border_width=1,
                                        border_color=THEME["border"])
        self.input_frame.pack(fill="x", padx=30, pady=(0, 12))

        self.status = StatusLabel(card, fg_color="transparent")
        self.status.pack(anchor="w", padx=30)

        GoldButton(card, text="✓  Confirm Payment", height=44,
                   font=get_font(14, "bold"),
                   command=self._confirm_payment).pack(
            fill="x", padx=30, pady=(8, 20))

        self._build_cash_inputs()

    def on_show(self):
        self._refresh_summary()
        self._on_method_change()

    def _refresh_summary(self):
        for w in self.summary_frame.winfo_children():
            w.destroy()
        if self.store.cart.is_empty():
            ctk.CTkLabel(self.summary_frame,
                         text="Your cart is empty. Add items before paying.",
                         font=get_font(12),
                         text_color=THEME["sub"]).pack(padx=16, pady=12)
            return

        total, disc, final = self.store.get_final_total()
        ctk.CTkLabel(self.summary_frame, text="Order Summary",
                     font=get_font(13, "bold"),
                     text_color=THEME["gold"]).pack(anchor="w", padx=16, pady=(14, 4))
        rows = [("Subtotal", f"₱{total:.2f}", THEME["text"])]
        if self.store.discount > 0:
            rows.append((f"Discount ({self.store.promo_used})",
                         f"-₱{disc:.2f}", THEME["success"]))
        rows.append(("Amount Due", f"₱{final:.2f}", THEME["gold"]))
        for label, value, color in rows:
            r = ctk.CTkFrame(self.summary_frame, fg_color="transparent")
            r.pack(fill="x", padx=16, pady=2)
            ctk.CTkLabel(r, text=label, font=get_font(12),
                         text_color=THEME["sub"]).pack(side="left")
            ctk.CTkLabel(r, text=value, font=get_font(13, "bold"),
                         text_color=color).pack(side="right")
        ctk.CTkLabel(self.summary_frame, text="", height=8).pack()

    def _on_method_change(self):
        for w in self.input_frame.winfo_children():
            w.destroy()
        method = self.method_var.get()
        if method == "Cash":
            self._build_cash_inputs()
        elif method == "Card":
            self._build_card_inputs()
        elif method == "E-Wallet":
            self._build_ewallet_inputs()

    def _build_cash_inputs(self):
        ctk.CTkLabel(self.input_frame, text="💵  Cash Payment",
                     font=get_font(13, "bold"),
                     text_color=THEME["gold"]).pack(anchor="w", padx=16, pady=(14, 4))
        ctk.CTkLabel(self.input_frame, text="Enter amount tendered:",
                     font=get_font(12),
                     text_color=THEME["sub"]).pack(anchor="w", padx=16)
        self.cash_var = StringVar()
        ctk.CTkEntry(self.input_frame, textvariable=self.cash_var,
                     placeholder_text="₱0.00", width=200, height=38,
                     font=get_font(14)).pack(anchor="w", padx=16, pady=(6, 14))
        self.cash_var.trace_add("write", self._update_change_preview)
        self.change_lbl = ctk.CTkLabel(self.input_frame, text="",
                                       font=get_font(12),
                                       text_color=THEME["success"])
        self.change_lbl.pack(anchor="w", padx=16, pady=(0, 10))

    def _update_change_preview(self, *args):
        try:
            cash = float(self.cash_var.get())
            _, _, final = self.store.get_final_total()
            change = cash - final
            if change >= 0:
                self.change_lbl.configure(
                    text=f"Change: ₱{change:.2f}",
                    text_color=THEME["success"])
            else:
                self.change_lbl.configure(
                    text=f"Short by ₱{abs(change):.2f}",
                    text_color=THEME["error"])
        except (ValueError, AttributeError):
            if hasattr(self, "change_lbl"):
                self.change_lbl.configure(text="")

    def _build_card_inputs(self):
        ctk.CTkLabel(self.input_frame, text="💳  Card Payment",
                     font=get_font(13, "bold"),
                     text_color=THEME["gold"]).pack(anchor="w", padx=16, pady=(14, 4))
        ctk.CTkLabel(self.input_frame, text="16-digit card number:",
                     font=get_font(12),
                     text_color=THEME["sub"]).pack(anchor="w", padx=16)
        self.card_var = StringVar()
        ctk.CTkEntry(self.input_frame, textvariable=self.card_var,
                     placeholder_text="XXXX XXXX XXXX XXXX",
                     width=280, height=38,
                     font=get_font(14)).pack(anchor="w", padx=16, pady=(6, 14))

    def _build_ewallet_inputs(self):
        ctk.CTkLabel(self.input_frame, text="📱  E-Wallet Payment",
                     font=get_font(13, "bold"),
                     text_color=THEME["gold"]).pack(anchor="w", padx=16, pady=(14, 4))

        self.wallet_var = StringVar(value="GCash")
        wallets = ["GCash", "Maya", "ShopeePay"]
        w_row = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        w_row.pack(anchor="w", padx=16)
        for w in wallets:
            ctk.CTkRadioButton(w_row, text=w, variable=self.wallet_var, value=w,
                               font=get_font(13),
                               fg_color=THEME["gold"],
                               hover_color=THEME["gold_hover"]).pack(side="left", padx=10)

        ctk.CTkLabel(self.input_frame, text="Account number or email:",
                     font=get_font(12),
                     text_color=THEME["sub"]).pack(anchor="w", padx=16, pady=(8, 0))
        self.ewallet_acc_var = StringVar()
        ctk.CTkEntry(self.input_frame, textvariable=self.ewallet_acc_var,
                     placeholder_text="09xxxxxxxxx or email@example.com",
                     width=300, height=38,
                     font=get_font(13)).pack(anchor="w", padx=16, pady=(6, 14))

    def _confirm_payment(self):
        if self.store.cart.is_empty():
            self.status.show("Your cart is empty. Add items first.", "error")
            return

        total, disc, final = self.store.get_final_total()
        method = self.method_var.get()

        if method == "Cash":
            raw = getattr(self, "cash_var", StringVar()).get().strip()
            try:
                cash = float(raw)
                if math.isnan(cash) or math.isinf(cash) or cash <= 0:
                    raise ValueError
            except ValueError:
                self.status.show("Please enter a valid cash amount.", "error")
                return
            if cash < final:
                self.status.show(f"Insufficient amount. Need at least ₱{final:.2f}.", "error")
                return
            change    = cash - final
            method_lbl = "Cash"
            extra_info = f"Cash Tendered: ₱{cash:.2f}  |  Change: ₱{change:.2f}"

        elif method == "Card":
            card = getattr(self, "card_var", StringVar()).get().strip().replace(" ", "")
            if len(card) != 16 or not card.isdigit():
                self.status.show("Card number must be exactly 16 digits.", "error")
                return
            masked     = "*" * 12 + card[-4:]
            method_lbl = "Card"
            extra_info = f"Card: {masked}"

        else:  # E-Wallet
            wallet  = getattr(self, "wallet_var", StringVar()).get()
            account = getattr(self, "ewallet_acc_var", StringVar()).get().strip()
            if not account:
                self.status.show(f"Please enter your {wallet} number or email.", "error")
                return
            method_lbl = wallet
            extra_info = f"Account: {account}"

        # Process and show receipt
        self._finalize_payment(method_lbl, extra_info, total, disc, final)

    def _finalize_payment(self, method_lbl, extra_info, total, disc, final):
        """Deduct stock, record transaction, show receipt dialog."""
        now       = datetime.datetime.now()
        dt_string = now.strftime("%Y-%m-%d %I:%M:%S %p")

        items_record = []
        for item_data in self.store.cart.iter_items():
            items_record.append({
                "name"    : item_data["name"],
                "qty"     : item_data["qty"],
                "subtotal": item_data["subtotal"],
            })
            inv_item = self.store.inventory.search(item_data["item_id"])
            if inv_item:
                inv_item.quantity = max(0, inv_item.quantity - item_data["qty"])

        self.store.history.enqueue({
            "datetime"  : dt_string,
            "method"    : method_lbl,
            "total"     : total,
            "discount"  : self.store.discount,
            "amount_due": final,
            "items"     : items_record,
        })

        promo_used = self.store.promo_used
        discount   = self.store.discount

        self.store.cart.clear()
        self.store.discount   = 0
        self.store.promo_used = ""
        self.store.undo_stack = Stack()

        self.refresh_cart()

        # Show receipt popup
        ReceiptDialog(self, dt_string, method_lbl, extra_info,
                      items_record, total, discount, promo_used, final)

        self._refresh_summary()


# ─────────────────────────────────────────
# RECEIPT DIALOG
# ─────────────────────────────────────────

class ReceiptDialog(ctk.CTkToplevel):
    """Popup receipt shown after successful payment."""

    def __init__(self, parent, dt_string, method, extra_info,
                 items, total, discount, promo_used, final):
        super().__init__(parent)
        self.transient(parent)
        self.attributes("-topmost", True)
        self.focus_force()
        self.title("Payment Receipt")
        self.geometry("440x560")
        self.resizable(False, True)
        self._build(dt_string, method, extra_info, items,
                    total, discount, promo_used, final)
        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width()  // 2 - 220
        py = parent.winfo_rooty() + parent.winfo_height() // 2 - 280
        self.geometry(f"+{px}+{py}")

    def _build(self, dt_string, method, extra_info, items,
               total, discount, promo_used, final):
        self.configure(fg_color=THEME["dark_surface"])

        # Gold accent top
        ctk.CTkFrame(self, height=8, fg_color=THEME["gold"],
                     corner_radius=0).pack(fill="x")

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=12)

        ctk.CTkLabel(scroll, text="NUmart",
                     font=get_font(24, "bold"),
                     text_color=THEME["gold"]).pack()
        ctk.CTkLabel(scroll, text="Study smart. Shop smart.",
                     font=get_font(12),
                     text_color=THEME["dark_sub"]).pack()

        ctk.CTkFrame(scroll, height=1,
                     fg_color=THEME["dark_border"]).pack(fill="x", pady=12)

        info_rows = [
            ("Date/Time", dt_string),
            ("Payment",   method),
            ("Details",   extra_info),
        ]
        for label, value in info_rows:
            r = ctk.CTkFrame(scroll, fg_color="transparent")
            r.pack(fill="x", pady=2)
            ctk.CTkLabel(r, text=label + ":", width=90,
                         font=get_font(11),
                         text_color=THEME["dark_sub"],
                         anchor="w").pack(side="left")
            ctk.CTkLabel(r, text=value,
                         font=get_font(11),
                         text_color=THEME["white"],
                         anchor="w",
                         wraplength=280).pack(side="left")

        ctk.CTkFrame(scroll, height=1,
                     fg_color=THEME["dark_border"]).pack(fill="x", pady=10)

        # Items
        hdr = ctk.CTkFrame(scroll, fg_color="transparent")
        hdr.pack(fill="x")
        for text, w, anchor in [("Item", 200, "w"), ("Qty", 40, "e"), ("Amount", 90, "e")]:
            ctk.CTkLabel(hdr, text=text, width=w,
                         font=get_font(11, "bold"),
                         text_color=THEME["gold"],
                         anchor=anchor).pack(side="left")

        ctk.CTkFrame(scroll, height=1,
                     fg_color=THEME["dark_border"]).pack(fill="x", pady=4)

        for item in items:
            r = ctk.CTkFrame(scroll, fg_color="transparent")
            r.pack(fill="x", pady=1)
            ctk.CTkLabel(r, text=item["name"], width=200,
                         font=get_font(11),
                         text_color=THEME["white"],
                         anchor="w").pack(side="left")
            ctk.CTkLabel(r, text=str(item["qty"]), width=40,
                         font=get_font(11),
                         text_color=THEME["dark_sub"],
                         anchor="e").pack(side="left")
            ctk.CTkLabel(r, text=f"₱{item['subtotal']:.2f}", width=90,
                         font=get_font(11),
                         text_color=THEME["white"],
                         anchor="e").pack(side="left")

        ctk.CTkFrame(scroll, height=1,
                     fg_color=THEME["dark_border"]).pack(fill="x", pady=10)

        # Totals
        totals = [("Subtotal", f"₱{total:.2f}", THEME["white"])]
        if discount > 0:
            totals.append((f"Discount ({promo_used})", f"-₱{total * discount / 100:.2f}",
                           THEME["success"]))
        totals.append(("TOTAL PAID", f"₱{final:.2f}", THEME["gold"]))

        for label, value, color in totals:
            r = ctk.CTkFrame(scroll, fg_color="transparent")
            r.pack(fill="x", pady=2)
            bold = "bold" if label == "TOTAL PAID" else "normal"
            ctk.CTkLabel(r, text=label,
                         font=(FONT_FAMILY, 12, bold),
                         text_color=THEME["dark_sub"]).pack(side="left")
            ctk.CTkLabel(r, text=value,
                         font=get_font(13, "bold"),
                         text_color=color).pack(side="right")

        ctk.CTkFrame(scroll, height=1,
                     fg_color=THEME["dark_border"]).pack(fill="x", pady=12)
        ctk.CTkLabel(scroll, text="Thank you for shopping at NUmart!",
                     font=get_font(12, "bold"),
                     text_color=THEME["gold"]).pack()
        ctk.CTkLabel(scroll, text="Study smart. Shop smart.",
                     font=get_font(11),
                     text_color=THEME["dark_sub"]).pack(pady=(2, 0))

        GoldButton(self, text="Close", command=self.destroy,
                   width=140).pack(pady=14)


# ─────────────────────────────────────────
# PAGE: TRANSACTION HISTORY
# ─────────────────────────────────────────

class HistoryPage(BasePage):

    def __init__(self, master, store, mode_var, refresh_cart_cb, **kwargs):
        super().__init__(master, store, mode_var, refresh_cart_cb, **kwargs)
        self._build()

    def _build(self):
        # Centered modern card layout to eliminate blank spaces
        card = ctk.CTkFrame(self, fg_color=THEME["card"], border_width=1, border_color=THEME["border"], corner_radius=12, width=600)
        card.pack(pady=30, fill="y", expand=True)
        card.pack_propagate(False)

        SectionHeader(card, text="📋  Transaction History").pack(
            anchor="w", padx=30, pady=(25, 4))
        ctk.CTkLabel(card, text="All completed transactions this session",
                     font=get_font(12),
                     text_color=THEME["sub"]).pack(anchor="w", padx=30)

        self.scroll_frame = ctk.CTkScrollableFrame(card, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=24, pady=12)

    def on_show(self):
        self._refresh()

    def _refresh(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()
        if self.store.history.is_empty():
            ctk.CTkLabel(self.scroll_frame,
                         text="No transactions yet.",
                         font=get_font(13),
                         text_color=THEME["sub"]).pack(pady=30)
            return

        for i, txn in enumerate(self.store.history._data, 1):
            card = ctk.CTkFrame(self.scroll_frame, fg_color=THEME["surface"],
                                corner_radius=10, border_width=1,
                                border_color=THEME["border"])
            card.pack(fill="x", pady=6)

            # Header row
            hdr = ctk.CTkFrame(card, fg_color=THEME["navy"], corner_radius=8)
            hdr.pack(fill="x", padx=8, pady=(8, 0))
            ctk.CTkLabel(hdr, text=f"Transaction #{i}",
                         font=get_font(13, "bold"),
                         text_color=THEME["gold"]).pack(side="left", padx=12, pady=8)
            ctk.CTkLabel(hdr, text=txn["datetime"],
                         font=get_font(11),
                         text_color=THEME["white"]).pack(side="right", padx=12)

            # Info
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(fill="x", padx=12, pady=6)
            ctk.CTkLabel(info_frame, text=f"Payment: {txn['method']}",
                         font=get_font(12),
                         text_color=THEME["sub"]).pack(side="left")
            amount_text = f"₱{txn['amount_due']:.2f}"
            if txn["discount"] > 0:
                amount_text += f"  ({txn['discount']}% off)"
            ctk.CTkLabel(info_frame, text=amount_text,
                         font=get_font(13, "bold"),
                         text_color=THEME["gold"]).pack(side="right")

            # Items
            for item in txn["items"]:
                r = ctk.CTkFrame(card, fg_color="transparent")
                r.pack(fill="x", padx=20, pady=1)
                ctk.CTkLabel(r, text=item["name"],
                             font=get_font(11),
                             text_color=THEME["text"],
                             anchor="w").pack(side="left")
                ctk.CTkLabel(r, text=f"×{item['qty']}  ₱{item['subtotal']:.2f}",
                             font=get_font(11),
                             text_color=THEME["sub"]).pack(side="right")

            ctk.CTkLabel(card, text="", height=4).pack()


# ─────────────────────────────────────────
# ADMIN PAGES
# ─────────────────────────────────────────

class AdminInventoryPage(BasePage):
    """Admin: View full inventory."""

    def __init__(self, master, store, mode_var, **kwargs):
        super().__init__(master, store, mode_var, **kwargs)
        self._build()

    def _build(self):
        SectionHeader(self, text="📦  Inventory Management").pack(
            anchor="w", padx=24, pady=(20, 4))
        ctk.CTkLabel(self, text="Full view of all stock items",
                     font=get_font(12),
                     text_color=THEME["sub"]).pack(anchor="w", padx=24)

        # Stat cards row
        self.stats_row = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_row.pack(fill="x", padx=24, pady=(12, 4))

        self.card_total  = StatCard(self.stats_row, "Total Items", "—", "📦",
                                    mode=self.mode_var.get())
        self.card_total.pack(side="left", padx=(0, 8), ipadx=10)
        self.card_low    = StatCard(self.stats_row, "Low Stock (≤10)", "—", "⚠️",
                                    mode=self.mode_var.get())
        self.card_low.pack(side="left", padx=(0, 8), ipadx=10)
        self.card_out    = StatCard(self.stats_row, "Out of Stock", "—", "🚫",
                                    mode=self.mode_var.get())
        self.card_out.pack(side="left", ipadx=10)

        # Search
        search_row = ctk.CTkFrame(self, fg_color="transparent")
        search_row.pack(fill="x", padx=24, pady=(8, 4))
        self.search_var = StringVar()
        ctk.CTkEntry(search_row, textvariable=self.search_var,
                     placeholder_text="Search by name or ID...",
                     width=300, height=36,
                     font=get_font(13)).pack(side="left")
        GoldButton(search_row, text="🔍 Search", width=100,
                   command=self._refresh_table).pack(side="left", padx=8)
        NavyButton(search_row, text="↺ Reset", width=80,
                   command=self._reset).pack(side="left")

        # Table
        table_frame = ctk.CTkFrame(self, fg_color=THEME["surface"],
                                   corner_radius=10, border_width=1,
                                   border_color=THEME["border"])
        table_frame.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        headers = ["ID", "Name", "Category", "Price", "Qty", "Expiration"]
        widths   = [55, 200, 110, 100, 70, 120]
        hdr_row  = ctk.CTkFrame(table_frame, fg_color=THEME["navy"], corner_radius=8)
        hdr_row.pack(fill="x", padx=6, pady=(6, 0))
        for h, w in zip(headers, widths):
            ctk.CTkLabel(hdr_row, text=h, width=w,
                         font=get_font(12, "bold"),
                         text_color=THEME["gold"]).pack(side="left", padx=4, pady=6)

        self.scroll_frame = ctk.CTkScrollableFrame(table_frame, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=6, pady=6)

        self._refresh_table()

    def _reset(self):
        self.search_var.set("")
        self._refresh_table()

    def on_show(self):
        pass

    def _refresh_table(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()
        keyword = self.search_var.get().strip().lower()
        items   = []
        low = out = 0
        node = self.store.inventory.head
        total_count = 0
        while node:
            total_count += 1
            if node.quantity == 0:
                out += 1
            elif node.quantity <= 10:
                low += 1
            if not keyword or keyword in node.name.lower() or keyword in node.item_id:
                items.append(node)
            node = node.next

        self.card_total.update_value(str(total_count))
        self.card_low.update_value(str(low))
        self.card_out.update_value(str(out))

        if not items:
            ctk.CTkLabel(self.scroll_frame, text="No items found.",
                         font=get_font(13),
                         text_color=THEME["sub"]).pack(pady=20)
            return

        widths = [55, 200, 110, 100, 70, 120]
        for i, item in enumerate(items):
            row_color = THEME["card"] if i % 2 == 0 else THEME["surface"]
            row = ctk.CTkFrame(self.scroll_frame, fg_color=row_color,
                               corner_radius=6, height=38)
            row.pack(fill="x", pady=1)
            row.pack_propagate(False)

            price_str = (f"₱{item.price:.2f}/10" if "Bond Paper" in item.name
                         else f"₱{item.price:.2f}")
            qty_color = THEME["error"] if item.quantity == 0 else (
                THEME["warning"] if item.quantity <= 10 else THEME["text"])

            values = [item.item_id, item.name, item.category,
                      price_str, str(item.quantity), item.expiration]
            colors = [THEME["sub"], THEME["text"], THEME["sub"], THEME["text"], qty_color, THEME["sub"]]

            for val, w, col in zip(values, widths, colors):
                ctk.CTkLabel(row, text=val, width=w,
                             font=get_font(12),
                             text_color=col,
                             anchor="w").pack(side="left", padx=4)


class AdminAddItemPage(BasePage):
    """Admin: Add a new inventory item."""

    def __init__(self, master, store, mode_var, **kwargs):
        super().__init__(master, store, mode_var, **kwargs)
        self._build()

    def _build(self):
        # Centered visual card to eliminate blank spaces
        card = ctk.CTkFrame(self, fg_color=THEME["card"], border_width=1, border_color=THEME["border"], corner_radius=12)
        card.pack(pady=30, fill="y", expand=True)

        SectionHeader(card, text="➕  Add New Item").pack(
            anchor="w", padx=30, pady=(25, 4))
        ctk.CTkLabel(card, text="Add a new product to the inventory",
                     font=get_font(12),
                     text_color=THEME["sub"]).pack(anchor="w", padx=30)

        form = ctk.CTkScrollableFrame(card, fg_color="transparent", width=360)
        form.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        self.fields = {}
        field_defs = [
            ("item_id",    "Item ID (3 digits)",           "e.g. 026"),
            ("name",       "Item Name",                    "e.g. Pencil Case"),
            ("category",   "Category",                     "e.g. Tools"),
            ("price",      "Price (₱)",                    "e.g. 49.00"),
            ("quantity",   "Quantity",                     "e.g. 100"),
            ("expiration", "Expiration (YYYY-MM-DD / None)","e.g. 2027-12-31"),
        ]

        for key, label, placeholder in field_defs:
            ctk.CTkLabel(form, text=label,
                         font=get_font(12, "bold"),
                         text_color=THEME["gold"]).pack(anchor="w", pady=(10, 2))
            var = StringVar()
            entry = ctk.CTkEntry(form, textvariable=var,
                                 placeholder_text=placeholder,
                                 width=320, height=38,
                                 font=get_font(13))
            entry.pack(anchor="w")
            self.fields[key] = var

        self.status = StatusLabel(form, fg_color="transparent")
        self.status.pack(anchor="w", pady=(10, 0))

        GoldButton(form, text="➕  Add Item", width=160, height=40,
                   command=self._submit).pack(anchor="w", pady=(10, 0))
        NavyButton(form, text="↺ Clear Form", width=120,
                   command=self._clear).pack(anchor="w", pady=(8, 0))

    def _clear(self):
        for var in self.fields.values():
            var.set("")
        self.status.clear()

    def _submit(self):
        item_id    = self.fields["item_id"].get().strip()
        name       = self.fields["name"].get().strip()
        category   = self.fields["category"].get().strip()
        price_str  = self.fields["price"].get().strip()
        qty_str    = self.fields["quantity"].get().strip()
        expiration = self.fields["expiration"].get().strip() or "None"

        if not item_id:
            self.status.show("Item ID cannot be empty.", "error"); return
        if not item_id.isdigit() or len(item_id) != 3:
            self.status.show("Item ID must be exactly 3 digits (e.g. 026).", "error"); return
        if self.store.inventory.search(item_id):
            self.status.show(f"Item ID '{item_id}' already exists.", "error"); return
        if not name:
            self.status.show("Item name cannot be empty.", "error"); return
        if not category:
            self.status.show("Category cannot be empty.", "error"); return
        try:
            price = float(price_str)
            if math.isnan(price) or math.isinf(price) or price <= 0:
                raise ValueError
        except ValueError:
            self.status.show("Price must be a positive number.", "error"); return
        try:
            qty = int(qty_str)
            if qty < 0:
                raise ValueError
        except ValueError:
            self.status.show("Quantity must be a non-negative whole number.", "error"); return

        self.store.inventory.insert(item_id, name, category, price, qty, expiration)
        self.status.show(f"✓  '{name}' added to inventory successfully.", "success")
        self._clear()


class AdminUpdateItemPage(BasePage):
    """Admin: Update an existing inventory item."""

    def __init__(self, master, store, mode_var, nav_to_inventory_cb=None, **kwargs):
        super().__init__(master, store, mode_var, **kwargs)
        self.nav_to_inventory = nav_to_inventory_cb
        self._build()

    def _build(self):
        # Centered modern card layout to eliminate blank spaces
        card = ctk.CTkFrame(self, fg_color=THEME["card"], border_width=1, border_color=THEME["border"], corner_radius=12)
        card.pack(pady=30, fill="y", expand=True)

        SectionHeader(card, text="✏️  Update Item").pack(
            anchor="w", padx=30, pady=(25, 4))
        ctk.CTkLabel(card, text="Edit an existing item's details",
                     font=get_font(12),
                     text_color=THEME["sub"]).pack(anchor="w", padx=30)

        # Search area inside the card
        search_row = ctk.CTkFrame(card, fg_color="transparent")
        search_row.pack(fill="x", padx=30, pady=(14, 6))
        ctk.CTkLabel(search_row, text="Item ID:",
                     font=get_font(12),
                     text_color=THEME["text"]).pack(side="left", padx=(0, 8))
        self.lookup_var = StringVar()
        ctk.CTkEntry(search_row, textvariable=self.lookup_var,
                     placeholder_text="e.g. 001",
                     width=100, height=36,
                     font=get_font(13)).pack(side="left")
        GoldButton(search_row, text="Load", width=80,
                   command=self._load_item).pack(side="left", padx=8)

        # Form inside the card (hidden until item loaded)
        self.form_frame = ctk.CTkScrollableFrame(card, fg_color="transparent", width=360)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=4)

        self.status = StatusLabel(card, fg_color="transparent")
        self.status.pack(anchor="w", padx=30, pady=(0, 15))

        self._current_item = None
        self.fields = {}

    def _load_item(self):
        item_id = self.lookup_var.get().strip()
        if not item_id:
            self.status.show("Please enter an Item ID.", "warning")
            return
        item = self.store.inventory.search(item_id)
        if not item:
            self.status.show(f"Item ID '{item_id}' not found.", "error")
            return

        self._current_item = item
        self.fields = {}
        for w in self.form_frame.winfo_children():
            w.destroy()
        ctk.CTkLabel(self.form_frame,
                     text=f"Editing: [{item.item_id}]  {item.name}",
                     font=get_font(13, "bold"),
                     text_color=THEME["gold"]).pack(anchor="w", pady=(8, 10))
        ctk.CTkLabel(self.form_frame, text="Leave a field blank to keep its current value.",
                     font=get_font(11),
                     text_color=THEME["sub"]).pack(anchor="w", pady=(0, 8))

        field_defs = [
            ("name",       "Name",       item.name),
            ("category",   "Category",   item.category),
            ("price",      "Price (₱)",  str(item.price)),
            ("quantity",   "Quantity",   str(item.quantity)),
            ("expiration", "Expiration", item.expiration),
        ]
        for key, label, current in field_defs:
            ctk.CTkLabel(self.form_frame,
                         text=f"{label}  [current: {current}]",
                         font=get_font(12, "bold"),
                         text_color=THEME["gold"]).pack(anchor="w", pady=(8, 2))
            var = StringVar()
            ctk.CTkEntry(self.form_frame, textvariable=var,
                         placeholder_text=current,
                         width=320, height=36,
                         font=get_font(13)).pack(anchor="w")
            self.fields[key] = var

        GoldButton(self.form_frame, text="✓  Save Changes", width=160, height=40,
                   command=self._submit).pack(anchor="w", pady=(16, 0))
        self.status.show(f"Loaded '{item.name}'. Edit fields above.", "info")

    def _submit(self):
        if not self._current_item:
            self.status.show("Load an item first.", "warning")
            return

        item    = self._current_item
        new_name = self.fields["name"].get().strip() or None
        new_cat  = self.fields["category"].get().strip() or None
        new_exp  = self.fields["expiration"].get().strip() or None

        price_raw = self.fields["price"].get().strip()
        new_price = None
        if price_raw:
            try:
                new_price = float(price_raw)
                if math.isnan(new_price) or math.isinf(new_price) or new_price <= 0:
                    self.status.show("Price must be a positive number.", "error"); return
            except ValueError:
                self.status.show("Invalid price.", "error"); return

        qty_raw = self.fields["quantity"].get().strip()
        new_qty = None
        if qty_raw:
            try:
                new_qty = int(qty_raw)
                if new_qty < 0:
                    self.status.show("Quantity cannot be negative.", "error"); return
            except ValueError:
                self.status.show("Quantity must be a whole number.", "error"); return

        self.store.inventory.update(
            item.item_id,
            new_name=new_name, new_category=new_cat,
            new_price=new_price, new_quantity=new_qty,
            new_expiration=new_exp)

        self.status.show(f"✓  '{item.name}' updated successfully.", "success")
        self._current_item = None
        for w in self.form_frame.winfo_children():
            w.destroy()
        self.lookup_var.set("")


class AdminDeleteItemPage(BasePage):
    """Admin: Delete an inventory item."""

    def __init__(self, master, store, mode_var, **kwargs):
        super().__init__(master, store, mode_var, **kwargs)
        self._build()

    def _build(self):
        # Centered modern card layout to eliminate blank spaces
        card = ctk.CTkFrame(self, fg_color=THEME["card"], border_width=1, border_color=THEME["border"], corner_radius=12, width=420)
        card.pack(pady=30, fill="y", expand=True)
        card.pack_propagate(False)

        SectionHeader(card, text="🗑️  Delete Item").pack(
            anchor="w", padx=30, pady=(25, 4))
        ctk.CTkLabel(card, text="Permanently remove an item from inventory",
                     font=get_font(12),
                     text_color=THEME["sub"]).pack(anchor="w", padx=30)

        search_row = ctk.CTkFrame(card, fg_color="transparent")
        search_row.pack(fill="x", padx=30, pady=(16, 6))
        ctk.CTkLabel(search_row, text="Item ID:",
                     font=get_font(12),
                     text_color=THEME["text"]).pack(side="left", padx=(0, 8))
        self.lookup_var = StringVar()
        ctk.CTkEntry(search_row, textvariable=self.lookup_var,
                     placeholder_text="e.g. 001",
                     width=100, height=36,
                     font=get_font(13)).pack(side="left")
        GoldButton(search_row, text="Find", width=80,
                   command=self._load_item).pack(side="left", padx=8)

        self.preview_frame = ctk.CTkFrame(card, fg_color=THEME["surface"],
                                          corner_radius=10, border_width=1,
                                          border_color=THEME["border"])
        self.preview_frame.pack(fill="x", padx=30, pady=8)
        self.preview_lbl = ctk.CTkLabel(self.preview_frame,
                                        text="Enter an Item ID above to load a preview.",
                                        font=get_font(12),
                                        text_color=THEME["sub"])
        self.preview_lbl.pack(padx=16, pady=14)

        self.status = StatusLabel(card, fg_color="transparent")
        self.status.pack(anchor="w", padx=30, pady=(4, 0))

        self._delete_btn = DangerButton(card, text="🗑  Delete This Item",
                                        width=180, height=40,
                                        state="disabled",
                                        command=self._confirm_delete)
        self._delete_btn.pack(anchor="w", padx=30, pady=12)
        self._item = None

    def _load_item(self):
        item_id = self.lookup_var.get().strip()
        if not item_id:
            self.status.show("Enter an Item ID.", "warning"); return
        item = self.store.inventory.search(item_id)
        if not item:
            self.status.show(f"Item ID '{item_id}' not found.", "error")
            self._item = None
            self._delete_btn.configure(state="disabled")
            return

        self._item = item
        for w in self.preview_frame.winfo_children():
            w.destroy()
        details = [
            ("ID",         item.item_id),
            ("Name",       item.name),
            ("Category",   item.category),
            ("Price",      f"₱{item.price:.2f}"),
            ("Quantity",   str(item.quantity)),
            ("Expiration", item.expiration),
        ]
        for label, value in details:
            r = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
            r.pack(fill="x", padx=16, pady=2)
            ctk.CTkLabel(r, text=label + ":", width=90,
                         font=get_font(12),
                         text_color=THEME["sub"],
                         anchor="w").pack(side="left")
            ctk.CTkLabel(r, text=value,
                         font=get_font(12),
                         text_color=THEME["text"]).pack(side="left")
        ctk.CTkLabel(self.preview_frame, text="", height=6).pack()

        self._delete_btn.configure(state="normal")
        self.status.show(f"Loaded '{item.name}'. Press Delete to remove.", "warning")

    def _confirm_delete(self):
        if not self._item:
            return
        dialog = DeleteConfirmDialog(self, self._item.name, on_confirm=self._do_delete)
        dialog.grab_set()

    def _do_delete(self):
        name = self._item.name
        self.store.inventory.delete(self._item.item_id)
        self.status.show(f"✓  '{name}' deleted from inventory.", "success")
        for w in self.preview_frame.winfo_children():
            w.destroy()
        ctk.CTkLabel(self.preview_frame,
                     text="Enter an Item ID above to load a preview.",
                     font=get_font(12),
                     text_color=THEME["sub"]).pack(padx=16, pady=14)
        self._item = None
        self.lookup_var.set("")
        self._delete_btn.configure(state="disabled")


class DeleteConfirmDialog(ctk.CTkToplevel):
    def __init__(self, parent, item_name, on_confirm):
        super().__init__(parent)
        self.transient(parent)
        self.attributes("-topmost", True)
        self.focus_force()
        self.on_confirm = on_confirm
        self.title("Confirm Delete")
        self.geometry("340x190")
        self.resizable(False, False)
        self.configure(fg_color=THEME["dark_surface"])
        ctk.CTkFrame(self, height=5, fg_color=THEME["error"],
                     corner_radius=0).pack(fill="x")
        ctk.CTkLabel(self, text="🗑️  Confirm Deletion",
                     font=get_font(15, "bold"),
                     text_color=THEME["white"]).pack(pady=(16, 6))
        ctk.CTkLabel(self, text=f"Delete '{item_name}' from inventory?\nThis cannot be undone.",
                     font=get_font(12),
                     text_color=THEME["dark_sub"],
                     justify="center").pack()
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(pady=18)
        DangerButton(row, text="Yes, Delete", width=120,
                     command=self._do).pack(side="left", padx=8)
        NavyButton(row, text="Cancel", width=100,
                   command=self.destroy).pack(side="left", padx=8)
        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width()  // 2 - 170
        py = parent.winfo_rooty() + parent.winfo_height() // 2 - 95
        self.geometry(f"+{px}+{py}")

    def _do(self):
        self.destroy()
        self.on_confirm()


class AdminSearchItemPage(BasePage):
    """Admin: Search inventory by ID or name keyword."""

    def __init__(self, master, store, mode_var, **kwargs):
        super().__init__(master, store, mode_var, **kwargs)
        self._build()

    def _build(self):
        SectionHeader(self, text="🔍  Search Item").pack(
            anchor="w", padx=24, pady=(20, 4))
        ctk.CTkLabel(self, text="Find items by exact ID or partial name",
                     font=get_font(12),
                     text_color=THEME["sub"]).pack(anchor="w", padx=24)

        search_row = ctk.CTkFrame(self, fg_color="transparent")
        search_row.pack(fill="x", padx=24, pady=(14, 6))
        self.query_var = StringVar()
        ctk.CTkEntry(search_row, textvariable=self.query_var,
                     placeholder_text="Item ID or name keyword...",
                     width=300, height=38,
                     font=get_font(13)).pack(side="left")
        GoldButton(search_row, text="🔍 Search", width=100,
                   command=self._search).pack(side="left", padx=8)
        NavyButton(search_row, text="↺ Clear", width=80,
                   command=self._clear).pack(side="left")

        self.results_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.results_frame.pack(fill="both", expand=True, padx=24, pady=8)

        self.status = StatusLabel(self, fg_color="transparent")
        self.status.pack(anchor="w", padx=24, pady=(0, 8))

        # bind Enter key
        self.query_var.trace_add("write", lambda *a: None)

    def on_show(self):
        pass

    def _clear(self):
        self.query_var.set("")
        for w in self.results_frame.winfo_children():
            w.destroy()
        self.status.clear()

    def _search(self):
        for w in self.results_frame.winfo_children():
            w.destroy()

        query = self.query_var.get().strip()
        if not query:
            self.status.show("Enter a search query.", "warning")
            return

        # exact ID match first
        item = self.store.inventory.search(query)
        if item:
            self._render_detail_card(item)
            self.status.show(f"Found exact match: [{item.item_id}] {item.name}", "success")
            return

        # partial name match
        matches = self.store.inventory.search_by_name(query)
        if matches:
            self.status.show(f"{len(matches)} item(s) matching '{query}'.", "success")
            widths = [55, 200, 110, 100, 70, 120]
            headers = ["ID", "Name", "Category", "Price", "Qty", "Expiration"]
            hdr_row = ctk.CTkFrame(self.results_frame, fg_color=THEME["navy"],
                                   corner_radius=8)
            hdr_row.pack(fill="x", pady=(0, 4))
            for h, w in zip(headers, widths):
                ctk.CTkLabel(hdr_row, text=h, width=w,
                             font=get_font(12, "bold"),
                             text_color=THEME["gold"]).pack(side="left", padx=4, pady=6)
            for i, m in enumerate(matches):
                row_color = THEME["card"] if i % 2 == 0 else THEME["surface"]
                row = ctk.CTkFrame(self.results_frame, fg_color=row_color,
                                   corner_radius=6, height=36)
                row.pack(fill="x", pady=1)
                row.pack_propagate(False)
                price_str = (f"₱{m.price:.2f}/10" if "Bond Paper" in m.name
                             else f"₱{m.price:.2f}")
                for val, w in zip([m.item_id, m.name, m.category,
                                   price_str, str(m.quantity), m.expiration], widths):
                    ctk.CTkLabel(row, text=val, width=w,
                                 font=get_font(12),
                                 text_color=THEME["text"],
                                 anchor="w").pack(side="left", padx=4)
        else:
            self.status.show(f"No items found matching '{query}'.", "error")

    def _render_detail_card(self, item):
        card = ctk.CTkFrame(self.results_frame, fg_color=THEME["card"],
                            corner_radius=10, border_width=1,
                            border_color=THEME["border"])
        card.pack(fill="x", pady=4)
        ctk.CTkLabel(card, text="Item Details",
                     font=get_font(13, "bold"),
                     text_color=THEME["gold"]).pack(anchor="w", padx=16, pady=(12, 4))
        details = [("ID", item.item_id), ("Name", item.name),
                   ("Category", item.category), ("Price", f"₱{item.price:.2f}"),
                   ("Quantity", str(item.quantity)), ("Expiration", item.expiration)]
        for label, value in details:
            r = ctk.CTkFrame(card, fg_color="transparent")
            r.pack(fill="x", padx=16, pady=2)
            ctk.CTkLabel(r, text=label + ":", width=90, anchor="w",
                         font=get_font(12),
                         text_color=THEME["sub"]).pack(side="left")
            ctk.CTkLabel(r, text=value,
                         font=get_font(12),
                         text_color=THEME["text"]).pack(side="left")
        ctk.CTkLabel(card, text="", height=8).pack()


# ─────────────────────────────────────────
# MAIN APPLICATION WINDOW
# ─────────────────────────────────────────

class NUmartApp(ctk.CTk):
    """Root application window. Manages landing → role screen transitions."""

    def __init__(self):
        super().__init__()
        self.title("NUmart — Study smart. Shop smart.")
        self.geometry("1100x680")
        self.minsize(860, 580)

        # Set initial dark appearance

        self.mode_var = StringVar(value="dark")
        self.store    = NUmart()
        self._current_role   = None
        self._sidebar        = None
        self._content_frames = {}

        self._show_landing()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        for after_id in self.tk.eval('after info').split():
            self.after_cancel(after_id)
        self.destroy()

    # ── Screen transitions ──────────────────

    def _clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._sidebar        = None
        self._content_frames = {}

    def _show_landing(self):
        self._clear_window()
        self._current_role = None
        self.configure(fg_color=THEME["bg"])

        landing = LandingScreen(
            self,
            on_customer=self._enter_customer,
            on_admin=self._enter_admin,
            mode_var=self.mode_var
        )
        landing.pack(fill="both", expand=True)

    def _enter_customer(self):
        self._current_role = "customer"
        self._build_app_shell("customer")
        self._navigate("browse")

    def _enter_admin(self):
        self._current_role = "admin"
        self._build_app_shell("admin")
        self._navigate("inventory")

    def _build_app_shell(self, role):
        """Build sidebar + content area for the given role."""
        self._clear_window()
        mode = self.mode_var.get()
        self.configure(fg_color=THEME["bg"])

        # Gold top accent strip
        ctk.CTkFrame(self, height=5, fg_color=THEME["gold"],
                     corner_radius=0).pack(fill="x", side="top")

        # Bottom status strip
        self._status_strip = ctk.CTkFrame(self, height=34,
                                          fg_color=THEME["navy_dark"],
                                          corner_radius=0)
        self._status_strip.pack(fill="x", side="bottom")
        self._strip_lbl = ctk.CTkLabel(
            self._status_strip,
            text=f"NUmart  ·  {'Customer Mode' if role == 'customer' else 'Admin Mode'}  ·  IT-252",
            font=get_font(11),
            text_color=THEME["white"])
        self._strip_lbl.pack(side="left", padx=14)
        self._cart_strip_lbl = ctk.CTkLabel(
            self._status_strip, text="",
            font=get_font(11, "bold"),
            text_color=THEME["gold"])
        self._cart_strip_lbl.pack(side="right", padx=14)

        # Main row: sidebar + content
        main_row = ctk.CTkFrame(self, fg_color="transparent")
        main_row.pack(fill="both", expand=True)

        self._sidebar = Sidebar(
            main_row,
            role=role,
            mode_var=self.mode_var,
            on_navigate=self._navigate,
            on_logout=self._logout
        )
        self._sidebar.pack(side="left", fill="y")

        self._content_area = ctk.CTkFrame(main_row, fg_color=THEME["bg"],
                                          corner_radius=0)
        self._content_area.pack(side="left", fill="both", expand=True)

        # Build all pages upfront
        if role == "customer":
            self._content_frames = {
                "browse" : BrowsePage(self._content_area, self.store,
                                      self.mode_var, self._refresh_cart_status),
                "cart"   : CartPage(self._content_area, self.store,
                                    self.mode_var, self._refresh_cart_status),
                "promo"  : PromoPage(self._content_area, self.store,
                                     self.mode_var, self._refresh_cart_status),
                "payment": PaymentPage(self._content_area, self.store,
                                       self.mode_var, self._refresh_cart_status),
                "history": HistoryPage(self._content_area, self.store,
                                       self.mode_var, self._refresh_cart_status),
            }
        else:
            self._content_frames = {
                "inventory" : AdminInventoryPage(self._content_area,
                                                 self.store, self.mode_var),
                "add_item"  : AdminAddItemPage(self._content_area,
                                               self.store, self.mode_var),
                "update_item": AdminUpdateItemPage(self._content_area,
                                                   self.store, self.mode_var),
                "delete_item": AdminDeleteItemPage(self._content_area,
                                                   self.store, self.mode_var),
                "search_item": AdminSearchItemPage(self._content_area,
                                                   self.store, self.mode_var),
            }

        for frame in self._content_frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._refresh_cart_status()

    def _navigate(self, page):
        """Switch the visible content frame."""
        for name, frame in self._content_frames.items():
            if name == page:
                frame.lift()
                frame.on_show()
            else:
                frame.lower()
        if self._sidebar:
            self._sidebar.set_active(page)

    def _refresh_cart_status(self):
        """Update sidebar cart total and bottom strip."""
        total = self.store.cart.compute_total()
        if self._sidebar:
            self._sidebar.update_cart_total(total)
        if hasattr(self, "_cart_strip_lbl"):
            if self._current_role == "customer":
                count = sum(1 for _ in self.store.cart.iter_items())
                if count > 0:
                    self._cart_strip_lbl.configure(
                        text=f"🛒 {count} item(s)  ·  ₱{total:.2f}")
                else:
                    self._cart_strip_lbl.configure(text="")

    def _logout(self):
        """Return to landing screen (called after logout confirmation)."""
        # Reset store for fresh customer session; keep history across roles
        self.store.cart.clear()
        self.store.discount   = 0
        self.store.promo_used = ""
        self.store.undo_stack = Stack()
        self._show_landing()

# ─────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────

if __name__ == "__main__":
    app = NUmartApp()
    app.mainloop()

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import math

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PRIMARY = "#D4AF37"
PRIMARY_HOVER = "#E4C55C"
NAVY = "#0A1633"
SURFACE = "#161B22"
CARD = "#1E2530"
TEXT = "#F8FAFC"
TEXT_SECONDARY = "#94A3B8"
BORDER = "#313A49"
SUCCESS = "#66BB6A"
DANGER = "#EF5350"

FONT_TITLE = ("Inter", 28, "bold")
FONT_HEADING = ("Inter", 18, "bold")
FONT_BODY = ("Inter", 13)
FONT_SMALL = ("Inter", 11)


def ease_out_cubic(t):
    return 1 - (1 - t) ** 3


def animate(root, start, end, duration_ms, callback, on_complete=None):
    steps = max(1, duration_ms // 16)

    for i in range(steps + 1):
        t = ease_out_cubic(i / steps)
        value = start + (end - start) * t
        delay = int((i / steps) * duration_ms)
        root.after(delay, lambda v=value: callback(v))

    if on_complete:
        root.after(duration_ms, on_complete)


class SidebarButton(ctk.CTkButton):

    def __init__(self, parent, text, command=None):
        super().__init__(
            parent,
            text=text,
            command=command,
            height=42,
            corner_radius=12,
            fg_color="transparent",
            hover_color=CARD,
            text_color=TEXT,
            anchor="w",
            font=FONT_BODY,
            border_width=1,
            border_color="transparent"
        )


class StatCard(ctk.CTkFrame):

    def __init__(self, parent, title, value):
        super().__init__(
            parent,
            fg_color=CARD,
            corner_radius=16,
            border_width=1,
            border_color=BORDER
        )

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text=title,
            text_color=TEXT_SECONDARY,
            font=FONT_SMALL
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 4))

        ctk.CTkLabel(
            self,
            text=value,
            text_color=TEXT,
            font=FONT_TITLE
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 18))


class Toast(ctk.CTkFrame):

    def __init__(self, parent, message, color=SUCCESS):
        super().__init__(
            parent,
            fg_color=CARD,
            corner_radius=14,
            border_width=1,
            border_color=color,
            height=60
        )

        self.place(relx=1.0, x=-20, y=-80, anchor="ne")

        ctk.CTkLabel(
            self,
            text=message,
            font=FONT_BODY,
            text_color=TEXT
        ).pack(padx=18, pady=18)

        animate(
            parent,
            -80,
            20,
            250,
            lambda v: self.place_configure(y=int(v))
        )

        parent.after(3000, self.destroy)


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.geometry("1400x850")
        self.title("NU Shopping Management System")
        self.configure(fg_color=NAVY)

        self.attributes("-alpha", 0.0)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.build_sidebar()
        self.build_main()

        animate(
            self,
            0.0,
            1.0,
            320,
            lambda v: self.attributes("-alpha", v)
        )

    def build_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=250,
            fg_color="#091224",
            corner_radius=0,
            border_width=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="NU SHOP",
            font=FONT_TITLE,
            text_color=PRIMARY
        ).pack(anchor="w", padx=24, pady=(30, 10))

        ctk.CTkLabel(
            self.sidebar,
            text="Inventory & POS Dashboard",
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY
        ).pack(anchor="w", padx=24, pady=(0, 30))

        nav_items = [
            "Dashboard",
            "Inventory",
            "Cart",
            "Transactions",
            "Users",
            "Reports",
            "Settings"
        ]

        for item in nav_items:
            SidebarButton(
                self.sidebar,
                text=item,
                command=lambda n=item: self.change_page(n)
            ).pack(fill="x", padx=16, pady=5)

    def build_main(self):

        self.main = ctk.CTkFrame(
            self,
            fg_color=NAVY,
            corner_radius=0
        )
        self.main.grid(row=0, column=1, sticky="nsew")

        self.main.grid_columnconfigure(0, weight=1)

        topbar = ctk.CTkFrame(
            self.main,
            fg_color="transparent",
            height=70
        )
        topbar.grid(row=0, column=0, sticky="ew", padx=24, pady=24)

        ctk.CTkLabel(
            topbar,
            text="Dashboard",
            font=FONT_TITLE,
            text_color=TEXT
        ).pack(side="left")

        ctk.CTkButton(
            topbar,
            text="+ Add Item",
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            text_color="#111111",
            corner_radius=12,
            height=40,
            width=120,
            command=self.show_success
        ).pack(side="right")

        stats = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )
        stats.grid(row=1, column=0, sticky="ew", padx=24)

        for i in range(4):
            stats.grid_columnconfigure(i, weight=1)

        cards = [
            ("Total Sales", "₱52,300"),
            ("Orders", "1,248"),
            ("Inventory", "322"),
            ("Customers", "482")
        ]

        for idx, (title, value) in enumerate(cards):
            card = StatCard(stats, title, value)
            card.grid(row=0, column=idx, sticky="nsew", padx=8)

        table_frame = ctk.CTkFrame(
            self.main,
            fg_color=CARD,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )
        table_frame.grid(row=2, column=0, sticky="nsew", padx=24, pady=24)

        ctk.CTkLabel(
            table_frame,
            text="Recent Transactions",
            font=FONT_HEADING,
            text_color=TEXT
        ).pack(anchor="w", padx=20, pady=(20, 12))

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#141A22",
            foreground="#F8FAFC",
            fieldbackground="#141A22",
            rowheight=34,
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#1E2530",
            foreground="#F8FAFC",
            relief="flat"
        )

        columns = ("id", "customer", "amount", "status")

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )

        for col in columns:
            self.table.heading(col, text=col.upper())
            self.table.column(col, anchor="center")

        self.table.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        sample_data = [
            ("1001", "Kim", "₱1,250", "Paid"),
            ("1002", "Cedrick", "₱880", "Pending"),
            ("1003", "Admin", "₱4,500", "Paid")
        ]

        for row in sample_data:
            self.table.insert("", "end", values=row)

    def change_page(self, page_name):
        Toast(self, f"Opened {page_name}")

    def show_success(self):
        Toast(self, "Item added successfully")

    def close_window(self):

        animate(
            self,
            1.0,
            0.0,
            220,
            lambda v: self.attributes("-alpha", v),
            on_complete=self.destroy
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()


class InventoryPage(ctk.CTkFrame):

  def __init__(self, parent):
    super().__init__(
      parent,
      fg_color="transparent"
    )

    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(2, weight=1)

    self.build_header()
    self.build_toolbar()
    self.build_inventory_table()

  def build_header(self):

    header = ctk.CTkFrame(
      self,
      fg_color="transparent"
    )
    header.grid(
      row=0,
      column=0,
      sticky="ew",
      padx=24,
      pady=(24, 12)
    )

    header.grid_columnconfigure(0, weight=1)

    left = ctk.CTkFrame(
      header,
      fg_color="transparent"
    )
    left.grid(
      row=0,
      column=0,
      sticky="w"
    )

    ctk.CTkLabel(
      left,
      text="Inventory Management",
      font=FONT_TITLE,
      text_color=TEXT
    ).pack(anchor="w")

    ctk.CTkLabel(
      left,
      text="Manage products, stock levels, and inventory records",
      font=FONT_BODY,
      text_color=TEXT_SECONDARY
    ).pack(anchor="w", pady=(4, 0))

    right = ctk.CTkFrame(
      header,
      fg_color="transparent"
    )
    right.grid(
      row=0,
      column=1,
      sticky="e"
    )

    self.search_var = tk.StringVar()

    self.entry_search = ctk.CTkEntry(
      right,
      width=240,
      height=40,
      corner_radius=12,
      textvariable=self.search_var,
      placeholder_text="Search inventory...",
      fg_color=CARD,
      border_color=BORDER,
      text_color=TEXT,
      font=FONT_BODY
    )
    self.entry_search.pack(side="left", padx=(0, 12))

    self.btn_add_item = ctk.CTkButton(
      right,
      text="+ Add Item",
      height=40,
      width=130,
      corner_radius=12,
      fg_color=PRIMARY,
      hover_color=PRIMARY_HOVER,
      text_color="#111111",
      font=FONT_BODY,
      command=self.add_item
    )
    self.btn_add_item.pack(side="left")

  def build_toolbar(self):

    toolbar = ctk.CTkFrame(
      self,
      fg_color=CARD,
      corner_radius=16,
      border_width=1,
      border_color=BORDER,
      height=70
    )
    toolbar.grid(
      row=1,
      column=0,
      sticky="ew",
      padx=24,
      pady=(0, 18)
    )

    toolbar.grid_propagate(False)

    left = ctk.CTkFrame(
      toolbar,
      fg_color="transparent"
    )
    left.pack(
      side="left",
      padx=18,
      pady=14
    )

    ctk.CTkButton(
      left,
      text="Refresh",
      width=110,
      height=38,
      corner_radius=10,
      fg_color=SURFACE,
      hover_color=CARD,
      border_width=1,
      border_color=BORDER,
      text_color=TEXT,
      font=FONT_BODY,
      command=self.refresh_inventory
    ).pack(side="left", padx=(0, 10))

    ctk.CTkButton(
      left,
      text="Export",
      width=110,
      height=38,
      corner_radius=10,
      fg_color=SURFACE,
      hover_color=CARD,
      border_width=1,
      border_color=BORDER,
      text_color=TEXT,
      font=FONT_BODY,
      command=self.export_inventory
    ).pack(side="left")

    right = ctk.CTkFrame(
      toolbar,
      fg_color="transparent"
    )
    right.pack(
      side="right",
      padx=18,
      pady=14
    )

    self.lbl_total_items = ctk.CTkLabel(
      right,
      text="322 Items",
      font=FONT_BODY,
      text_color=TEXT_SECONDARY
    )
    self.lbl_total_items.pack()

  def build_inventory_table(self):

    table_container = ctk.CTkFrame(
      self,
      fg_color=CARD,
      corner_radius=18,
      border_width=1,
      border_color=BORDER
    )
    table_container.grid(
      row=2,
      column=0,
      sticky="nsew",
      padx=24,
      pady=(0, 24)
    )

    table_container.grid_columnconfigure(0, weight=1)
    table_container.grid_rowconfigure(1, weight=1)

    top = ctk.CTkFrame(
      table_container,
      fg_color="transparent"
    )
    top.grid(
      row=0,
      column=0,
      sticky="ew",
      padx=20,
      pady=(20, 12)
    )

    top.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
      top,
      text="Inventory Records",
      font=FONT_HEADING,
      text_color=TEXT
    ).grid(
      row=0,
      column=0,
      sticky="w"
    )

    self.status_badge = ctk.CTkLabel(
      top,
      text="LIVE",
      width=70,
      height=28,
      corner_radius=999,
      fg_color=SUCCESS,
      text_color="#111111",
      font=FONT_SMALL
    )
    self.status_badge.grid(
      row=0,
      column=1,
      sticky="e"
    )

    table_frame = ctk.CTkFrame(
      table_container,
      fg_color="transparent"
    )
    table_frame.grid(
      row=1,
      column=0,
      sticky="nsew",
      padx=20,
      pady=(0, 20)
    )

    columns = (
      "id",
      "product",
      "category",
      "price",
      "stock",
      "status"
    )

    style = ttk.Style()
    style.theme_use("default")

    style.configure(
      "Inventory.Treeview",
      background="#161B22",
      foreground="#F8FAFC",
      fieldbackground="#161B22",
      borderwidth=0,
      rowheight=40,
      font=("Inter", 11)
    )

    style.configure(
      "Inventory.Treeview.Heading",
      background="#1E2530",
      foreground="#F8FAFC",
      relief="flat",
      font=("Inter", 11, "bold")
    )

    style.map(
      "Inventory.Treeview",
      background=[("selected", "#D4AF37")],
      foreground=[("selected", "#111111")]
    )

    self.inventory_table = ttk.Treeview(
      table_frame,
      columns=columns,
      show="headings",
      style="Inventory.Treeview"
    )

    self.inventory_table.pack(
      fill="both",
      expand=True
    )

    for col in columns:
      self.inventory_table.heading(
        col,
        text=col.upper()
      )

      self.inventory_table.column(
        col,
        anchor="center",
        width=120
      )

    sample_inventory = [
      ("1001", "Keyboard", "Accessories", "₱850", "24", "In Stock"),
      ("1002", "Mouse", "Accessories", "₱420", "8", "Low Stock"),
      ("1003", "Monitor", "Display", "₱7200", "12", "In Stock"),
      ("1004", "USB Cable", "Cables", "₱120", "0", "Out of Stock"),
      ("1005", "Headset", "Audio", "₱1500", "14", "In Stock"),
    ]

    for row in sample_inventory:
      self.inventory_table.insert(
        "",
        "end",
        values=row
      )

  def add_item(self):
    Toast(
      self.winfo_toplevel(),
      "Opening add item dialog..."
    )

  def refresh_inventory(self):
    Toast(
      self.winfo_toplevel(),
      "Inventory refreshed successfully"
    )

  def export_inventory(self):
    Toast(
      self.winfo_toplevel(),
      "Inventory exported"
    )

class CartPage(ctk.CTkFrame):

    def __init__(self, parent):
      super().__init__(
        parent,
        fg_color="transparent"
      )

      self.grid_columnconfigure(0, weight=2)
      self.grid_columnconfigure(1, weight=1)
      self.grid_rowconfigure(1, weight=1)

      self.cart_items = []

      self.build_header()
      self.build_cart_table()
      self.build_summary_panel()

    def build_header(self):

      header = ctk.CTkFrame(
        self,
        fg_color="transparent"
      )
      header.grid(
        row=0,
        column=0,
        columnspan=2,
        sticky="ew",
        padx=24,
        pady=(24, 18)
      )

      header.grid_columnconfigure(0, weight=1)

      left = ctk.CTkFrame(
        header,
        fg_color="transparent"
      )
      left.grid(
        row=0,
        column=0,
        sticky="w"
      )

      ctk.CTkLabel(
        left,
        text="Shopping Cart",
        font=FONT_TITLE,
        text_color=TEXT
      ).pack(anchor="w")

      ctk.CTkLabel(
        left,
        text="Review selected items and complete transactions",
        font=FONT_BODY,
        text_color=TEXT_SECONDARY
      ).pack(anchor="w", pady=(4, 0))

      right = ctk.CTkFrame(
        header,
        fg_color="transparent"
      )
      right.grid(
        row=0,
        column=1,
        sticky="e"
      )

      ctk.CTkButton(
        right,
        text="Clear Cart",
        width=120,
        height=40,
        corner_radius=12,
        fg_color=DANGER,
        hover_color="#D64545",
        text_color="white",
        font=FONT_BODY,
        command=self.clear_cart
      ).pack(side="left", padx=(0, 12))

      ctk.CTkButton(
        right,
        text="+ Add Product",
        width=140,
        height=40,
        corner_radius=12,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        text_color="#111111",
        font=FONT_BODY,
        command=self.add_product
      ).pack(side="left")

    def build_cart_table(self):

      table_container = ctk.CTkFrame(
        self,
        fg_color=CARD,
        corner_radius=18,
        border_width=1,
        border_color=BORDER
      )
      table_container.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=(24, 12),
        pady=(0, 24)
      )

      table_container.grid_columnconfigure(0, weight=1)
      table_container.grid_rowconfigure(1, weight=1)

      top = ctk.CTkFrame(
        table_container,
        fg_color="transparent"
      )
      top.grid(
        row=0,
        column=0,
        sticky="ew",
        padx=20,
        pady=(20, 12)
      )

      top.grid_columnconfigure(0, weight=1)

      ctk.CTkLabel(
        top,
        text="Cart Items",
        font=FONT_HEADING,
        text_color=TEXT
      ).grid(
        row=0,
        column=0,
        sticky="w"
      )

      self.lbl_cart_count = ctk.CTkLabel(
        top,
        text="3 Items",
        font=FONT_SMALL,
        text_color=TEXT_SECONDARY
      )
      self.lbl_cart_count.grid(
        row=0,
        column=1,
        sticky="e"
      )

      table_frame = ctk.CTkFrame(
        table_container,
        fg_color="transparent"
      )
      table_frame.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=20,
        pady=(0, 20)
      )

      columns = (
        "id",
        "product",
        "quantity",
        "price",
        "subtotal"
      )

      style = ttk.Style()

      style.configure(
        "Cart.Treeview",
        background="#161B22",
        foreground="#F8FAFC",
        fieldbackground="#161B22",
        borderwidth=0,
        rowheight=42,
        font=("Inter", 11)
      )

      style.configure(
        "Cart.Treeview.Heading",
        background="#1E2530",
        foreground="#F8FAFC",
        relief="flat",
        font=("Inter", 11, "bold")
      )

      self.cart_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        style="Cart.Treeview"
      )

      self.cart_table.pack(
        fill="both",
        expand=True
      )

      for col in columns:
        self.cart_table.heading(
          col,
          text=col.upper()
        )

        self.cart_table.column(
          col,
          anchor="center",
          width=120
        )

      sample_cart = [
        ("1001", "Mechanical Keyboard", "1", "₱850", "₱850"),
        ("1002", "Gaming Mouse", "2", "₱420", "₱840"),
        ("1003", "USB Cable", "3", "₱120", "₱360"),
      ]

      for row in sample_cart:
        self.cart_table.insert(
          "",
          "end",
          values=row
        )

    def build_summary_panel(self):

      summary = ctk.CTkFrame(
        self,
        fg_color=CARD,
        corner_radius=18,
        border_width=1,
        border_color=BORDER,
        width=360
      )
      summary.grid(
        row=1,
        column=1,
        sticky="nsew",
        padx=(12, 24),
        pady=(0, 24)
      )

      summary.grid_propagate(False)

      ctk.CTkLabel(
        summary,
        text="Order Summary",
        font=FONT_HEADING,
        text_color=TEXT
      ).pack(
        anchor="w",
        padx=24,
        pady=(24, 18)
      )

      self.build_summary_row(summary, "Subtotal", "₱2,050")
      self.build_summary_row(summary, "Tax", "₱246")
      self.build_summary_row(summary, "Discount", "- ₱100")

      divider = ctk.CTkFrame(
        summary,
        fg_color=BORDER,
        height=1
      )
      divider.pack(
        fill="x",
        padx=24,
        pady=18
      )

      total_row = ctk.CTkFrame(
        summary,
        fg_color="transparent"
      )
      total_row.pack(
        fill="x",
        padx=24
      )

      ctk.CTkLabel(
        total_row,
        text="TOTAL",
        font=FONT_HEADING,
        text_color=TEXT
      ).pack(side="left")

      ctk.CTkLabel(
        total_row,
        text="₱2,196",
        font=FONT_HEADING,
        text_color=PRIMARY
      ).pack(side="right")

      ctk.CTkLabel(
        summary,
        text="Payment Method",
        font=FONT_BODY,
        text_color=TEXT_SECONDARY
      ).pack(
        anchor="w",
        padx=24,
        pady=(24, 8)
      )

      self.payment_option = ctk.CTkOptionMenu(
        summary,
        values=[
          "Cash",
          "GCash",
          "Credit Card",
          "Debit Card"
        ],
        height=40,
        corner_radius=12,
        fg_color=SURFACE,
        button_color=PRIMARY,
        button_hover_color=PRIMARY_HOVER,
        dropdown_fg_color=CARD,
        dropdown_hover_color=SURFACE,
        text_color=TEXT,
        font=FONT_BODY
      )
      self.payment_option.pack(
        fill="x",
        padx=24
      )

      ctk.CTkButton(
        summary,
        text="Proceed to Checkout",
        height=48,
        corner_radius=14,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        text_color="#111111",
        font=("Inter", 14, "bold"),
        command=self.checkout
      ).pack(
        fill="x",
        padx=24,
        pady=(28, 24)
      )

    def build_summary_row(self, parent, label, value):

      row = ctk.CTkFrame(
        parent,
        fg_color="transparent"
      )
      row.pack(
        fill="x",
        padx=24,
        pady=6
      )

      ctk.CTkLabel(
        row,
        text=label,
        font=FONT_BODY,
        text_color=TEXT_SECONDARY
      ).pack(side="left")

      ctk.CTkLabel(
        row,
        text=value,
        font=FONT_BODY,
        text_color=TEXT
      ).pack(side="right")

    def add_product(self):

      Toast(
        self.winfo_toplevel(),
        "Opening product selection..."
      )

    def clear_cart(self):

      for item in self.cart_table.get_children():
        self.cart_table.delete(item)

      Toast(
        self.winfo_toplevel(),
        "Cart cleared successfully",
        color=DANGER
      )

    def checkout(self):

      Toast(
        self.winfo_toplevel(),
        "Processing checkout..."
      )


class TransactionHistoryPage(ctk.CTkFrame):

  def __init__(self, parent):
    super().__init__(
      parent,
      fg_color="transparent"
    )

    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(2, weight=1)

    self.build_header()
    self.build_filters()
    self.build_history_table()

  def build_header(self):

    header = ctk.CTkFrame(
      self,
      fg_color="transparent"
    )
    header.grid(
      row=0,
      column=0,
      sticky="ew",
      padx=24,
      pady=(24, 18)
    )

    header.grid_columnconfigure(0, weight=1)

    left = ctk.CTkFrame(
      header,
      fg_color="transparent"
    )
    left.grid(
      row=0,
      column=0,
      sticky="w"
    )

    ctk.CTkLabel(
      left,
      text="Transaction History",
      font=FONT_TITLE,
      text_color=TEXT
    ).pack(anchor="w")

    ctk.CTkLabel(
      left,
      text="Review completed purchases and payment records",
      font=FONT_BODY,
      text_color=TEXT_SECONDARY
    ).pack(anchor="w", pady=(4, 0))

    right = ctk.CTkFrame(
      header,
      fg_color="transparent"
    )
    right.grid(
      row=0,
      column=1,
      sticky="e"
    )

    ctk.CTkButton(
      right,
      text="Export Report",
      width=140,
      height=40,
      corner_radius=12,
      fg_color=PRIMARY,
      hover_color=PRIMARY_HOVER,
      text_color="#111111",
      font=FONT_BODY,
      command=self.export_report
    ).pack(side="left")

  def build_filters(self):

    filters = ctk.CTkFrame(
      self,
      fg_color=CARD,
      corner_radius=18,
      border_width=1,
      border_color=BORDER,
      height=82
    )
    filters.grid(
      row=1,
      column=0,
      sticky="ew",
      padx=24,
      pady=(0, 18)
    )

    filters.grid_propagate(False)

    search_frame = ctk.CTkFrame(
      filters,
      fg_color="transparent"
    )
    search_frame.pack(
      side="left",
      padx=18,
      pady=18
    )

    self.history_search = ctk.CTkEntry(
      search_frame,
      width=260,
      height=42,
      corner_radius=12,
      placeholder_text="Search transaction...",
      fg_color=SURFACE,
      border_color=BORDER,
      text_color=TEXT,
      font=FONT_BODY
    )
    self.history_search.pack(side="left")

    filter_frame = ctk.CTkFrame(
      filters,
      fg_color="transparent"
    )
    filter_frame.pack(
      side="right",
      padx=18,
      pady=18
    )

    self.status_filter = ctk.CTkOptionMenu(
      filter_frame,
      values=[
        "All Status",
        "Paid",
        "Pending",
        "Cancelled"
      ],
      width=160,
      height=40,
      corner_radius=12,
      fg_color=SURFACE,
      button_color=PRIMARY,
      button_hover_color=PRIMARY_HOVER,
      dropdown_fg_color=CARD,
      dropdown_hover_color=SURFACE,
      text_color=TEXT,
      font=FONT_BODY
    )
    self.status_filter.pack(side="left", padx=(0, 10))

    self.date_filter = ctk.CTkOptionMenu(
      filter_frame,
      values=[
        "Today",
        "This Week",
        "This Month",
        "This Year"
      ],
      width=160,
      height=40,
      corner_radius=12,
      fg_color=SURFACE,
      button_color=PRIMARY,
      button_hover_color=PRIMARY_HOVER,
      dropdown_fg_color=CARD,
      dropdown_hover_color=SURFACE,
      text_color=TEXT,
      font=FONT_BODY
    )
    self.date_filter.pack(side="left")

  def build_history_table(self):

    container = ctk.CTkFrame(
      self,
      fg_color=CARD,
      corner_radius=18,
      border_width=1,
      border_color=BORDER
    )
    container.grid(
      row=2,
      column=0,
      sticky="nsew",
      padx=24,
      pady=(0, 24)
    )

    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(1, weight=1)

    top = ctk.CTkFrame(
      container,
      fg_color="transparent"
    )
    top.grid(
      row=0,
      column=0,
      sticky="ew",
      padx=20,
      pady=(20, 12)
    )

    top.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
      top,
      text="Recent Transactions",
      font=FONT_HEADING,
      text_color=TEXT
    ).grid(
      row=0,
      column=0,
      sticky="w"
    )

    self.lbl_transaction_count = ctk.CTkLabel(
      top,
      text="248 Records",
      font=FONT_SMALL,
      text_color=TEXT_SECONDARY
    )
    self.lbl_transaction_count.grid(
      row=0,
      column=1,
      sticky="e"
    )

    table_frame = ctk.CTkFrame(
      container,
      fg_color="transparent"
    )
    table_frame.grid(
      row=1,
      column=0,
      sticky="nsew",
      padx=20,
      pady=(0, 20)
    )

    columns = (
      "transaction_id",
      "customer",
      "amount",
      "payment",
      "status",
      "date"
    )

    style = ttk.Style()

    style.configure(
      "History.Treeview",
      background="#161B22",
      foreground="#F8FAFC",
      fieldbackground="#161B22",
      rowheight=42,
      borderwidth=0,
      font=("Inter", 11)
    )

    style.configure(
      "History.Treeview.Heading",
      background="#1E2530",
      foreground="#F8FAFC",
      relief="flat",
      font=("Inter", 11, "bold")
    )

    self.history_table = ttk.Treeview(
      table_frame,
      columns=columns,
      show="headings",
      style="History.Treeview"
    )

    self.history_table.pack(
      fill="both",
      expand=True
    )

    for col in columns:
      self.history_table.heading(
        col,
        text=col.replace("_", " ").upper()
      )

      self.history_table.column(
        col,
        anchor="center",
        width=120
      )

    sample_history = [
      ("TXN-1001", "Kim", "₱2,196", "GCash", "Paid", "May 24"),
      ("TXN-1002", "Cedrick", "₱880", "Cash", "Pending", "May 23"),
      ("TXN-1003", "Admin", "₱5,420", "Card", "Paid", "May 22"),
      ("TXN-1004", "Angela", "₱720", "Cash", "Cancelled", "May 22"),
      ("TXN-1005", "John", "₱3,500", "GCash", "Paid", "May 21"),
    ]

    for row in sample_history:
      self.history_table.insert(
        "",
        "end",
        values=row
      )

  def export_report(self):

    Toast(
      self.winfo_toplevel(),
      "Transaction report exported successfully"
    )

class UserManagementPage(ctk.CTkFrame):

  def __init__(self, parent):
    super().__init__(
      parent,
      fg_color="transparent"
    )

    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(2, weight=1)

    self.build_header()
    self.build_toolbar()
    self.build_user_table()

  def build_header(self):

    header = ctk.CTkFrame(
      self,
      fg_color="transparent"
    )
    header.grid(
      row=0,
      column=0,
      sticky="ew",
      padx=24,
      pady=(24, 18)
    )

    header.grid_columnconfigure(0, weight=1)

    left = ctk.CTkFrame(
      header,
      fg_color="transparent"
    )
    left.grid(
      row=0,
      column=0,
      sticky="w"
    )

    ctk.CTkLabel(
      left,
      text="User Management",
      font=FONT_TITLE,
      text_color=TEXT
    ).pack(anchor="w")

    ctk.CTkLabel(
      left,
      text="Manage system users, permissions, and account roles",
      font=FONT_BODY,
      text_color=TEXT_SECONDARY
    ).pack(anchor="w", pady=(4, 0))

    right = ctk.CTkFrame(
      header,
      fg_color="transparent"
    )
    right.grid(
      row=0,
      column=1,
      sticky="e"
    )

    ctk.CTkButton(
      right,
      text="+ Create User",
      width=140,
      height=40,
      corner_radius=12,
      fg_color=PRIMARY,
      hover_color=PRIMARY_HOVER,
      text_color="#111111",
      font=FONT_BODY,
      command=self.create_user
    ).pack(side="left")

  def build_toolbar(self):

    toolbar = ctk.CTkFrame(
      self,
      fg_color=CARD,
      corner_radius=18,
      border_width=1,
      border_color=BORDER,
      height=82
    )
    toolbar.grid(
      row=1,
      column=0,
      sticky="ew",
      padx=24,
      pady=(0, 18)
    )

    toolbar.grid_propagate(False)

    left = ctk.CTkFrame(
      toolbar,
      fg_color="transparent"
    )
    left.pack(
      side="left",
      padx=18,
      pady=18
    )

    self.user_search = ctk.CTkEntry(
      left,
      width=260,
      height=42,
      corner_radius=12,
      placeholder_text="Search users...",
      fg_color=SURFACE,
      border_color=BORDER,
      text_color=TEXT,
      font=FONT_BODY
    )
    self.user_search.pack(side="left", padx=(0, 12))

    ctk.CTkButton(
      left,
      text="Refresh",
      width=110,
      height=40,
      corner_radius=12,
      fg_color=SURFACE,
      hover_color=CARD,
      border_width=1,
      border_color=BORDER,
      text_color=TEXT,
      font=FONT_BODY,
      command=self.refresh_users
    ).pack(side="left")

    right = ctk.CTkFrame(
      toolbar,
      fg_color="transparent"
    )
    right.pack(
      side="right",
      padx=18,
      pady=18
    )

    self.role_filter = ctk.CTkOptionMenu(
      right,
      values=[
        "All Roles",
        "Admin",
        "Cashier",
        "Customer"
      ],
      width=160,
      height=40,
      corner_radius=12,
      fg_color=SURFACE,
      button_color=PRIMARY,
      button_hover_color=PRIMARY_HOVER,
      dropdown_fg_color=CARD,
      dropdown_hover_color=SURFACE,
      text_color=TEXT,
      font=FONT_BODY
    )
    self.role_filter.pack(side="left")

  def build_user_table(self):

    container = ctk.CTkFrame(
      self,
      fg_color=CARD,
      corner_radius=18,
      border_width=1,
      border_color=BORDER
    )
    container.grid(
      row=2,
      column=0,
      sticky="nsew",
      padx=24,
      pady=(0, 24)
    )

    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(1, weight=1)

    top = ctk.CTkFrame(
      container,
      fg_color="transparent"
    )
    top.grid(
      row=0,
      column=0,
      sticky="ew",
      padx=20,
      pady=(20, 12)
    )

    top.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
      top,
      text="Registered Users",
      font=FONT_HEADING,
      text_color=TEXT
    ).grid(
      row=0,
      column=0,
      sticky="w"
    )

    self.lbl_user_count = ctk.CTkLabel(
      top,
      text="42 Users",
      font=FONT_SMALL,
      text_color=TEXT_SECONDARY
    )
    self.lbl_user_count.grid(
      row=0,
      column=1,
      sticky="e"
    )

    table_frame = ctk.CTkFrame(
      container,
      fg_color="transparent"
    )
    table_frame.grid(
      row=1,
      column=0,
      sticky="nsew",
      padx=20,
      pady=(0, 20)
    )

    columns = (
      "user_id",
      "name",
      "email",
      "role",
      "status",
      "last_login"
    )

    style = ttk.Style()

    style.configure(
      "Users.Treeview",
      background="#161B22",
      foreground="#F8FAFC",
      fieldbackground="#161B22",
      borderwidth=0,
      rowheight=42,
      font=("Inter", 11)
    )

    style.configure(
      "Users.Treeview.Heading",
      background="#1E2530",
      foreground="#F8FAFC",
      relief="flat",
      font=("Inter", 11, "bold")
    )

    self.user_table = ttk.Treeview(
      table_frame,
      columns=columns,
      show="headings",
      style="Users.Treeview"
    )

    self.user_table.pack(
      fill="both",
      expand=True
    )

    for col in columns:
      self.user_table.heading(
        col,
        text=col.replace("_", " ").upper()
      )

      self.user_table.column(
        col,
        anchor="center",
        width=120
      )

    sample_users = [
      ("USR-001", "Kim Cedrick", "kim@gmail.com", "Admin", "Active", "Today"),
      ("USR-002", "Angela Cruz", "angela@gmail.com", "Cashier", "Active", "1 hour ago"),
      ("USR-003", "John Doe", "john@gmail.com", "Customer", "Inactive", "Yesterday"),
      ("USR-004", "Maria Santos", "maria@gmail.com", "Cashier", "Active", "Today"),
      ("USR-005", "Cedrick Lee", "cedrick@gmail.com", "Customer", "Suspended", "2 days ago"),
    ]

    for row in sample_users:
      self.user_table.insert(
        "",
        "end",
        values=row
      )

  def create_user(self):

    Toast(
      self.winfo_toplevel(),
      "Opening create user dialog..."
    )

  def refresh_users(self):

    Toast(
      self.winfo_toplevel(),
      "User list refreshed successfully"
    )

class ReportsPage(ctk.CTkFrame):

  def __init__(self, parent):
    super().__init__(
      parent,
      fg_color="transparent"
    )

    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(2, weight=1)

    self.build_header()
    self.build_stats()
    self.build_reports_panel()

  def build_header(self):

    header = ctk.CTkFrame(
      self,
      fg_color="transparent"
    )
    header.grid(
      row=0,
      column=0,
      sticky="ew",
      padx=24,
      pady=(24, 18)
    )

    header.grid_columnconfigure(0, weight=1)

    left = ctk.CTkFrame(
      header,
      fg_color="transparent"
    )
    left.grid(
      row=0,
      column=0,
      sticky="w"
    )

    ctk.CTkLabel(
      left,
      text="Analytics & Reports",
      font=FONT_TITLE,
      text_color=TEXT
    ).pack(anchor="w")

    ctk.CTkLabel(
      left,
      text="Monitor performance, sales trends, and business insights",
      font=FONT_BODY,
      text_color=TEXT_SECONDARY
    ).pack(anchor="w", pady=(4, 0))

    right = ctk.CTkFrame(
      header,
      fg_color="transparent"
    )
    right.grid(
      row=0,
      column=1,
      sticky="e"
    )

    ctk.CTkButton(
      right,
      text="Generate Report",
      width=160,
      height=40,
      corner_radius=12,
      fg_color=PRIMARY,
      hover_color=PRIMARY_HOVER,
      text_color="#111111",
      font=FONT_BODY,
      command=self.generate_report
    ).pack(side="left")

  def build_stats(self):

    stats = ctk.CTkFrame(
      self,
      fg_color="transparent"
    )
    stats.grid(
      row=1,
      column=0,
      sticky="ew",
      padx=24,
      pady=(0, 18)
    )

    for i in range(4):
      stats.grid_columnconfigure(i, weight=1)

    cards = [
      ("Today's Sales", "₱14,250"),
      ("Monthly Revenue", "₱128,400"),
      ("Best Seller", "Keyboard"),
      ("Transactions", "482")
    ]

    for idx, (title, value) in enumerate(cards):
      card = StatCard(
        stats,
        title,
        value
      )

      card.grid(
        row=0,
        column=idx,
        sticky="nsew",
        padx=8
      )

  def build_reports_panel(self):

    panel = ctk.CTkFrame(
      self,
      fg_color=CARD,
      corner_radius=18,
      border_width=1,
      border_color=BORDER
    )
    panel.grid(
      row=2,
      column=0,
      sticky="nsew",
      padx=24,
      pady=(0, 24)
    )

    panel.grid_columnconfigure(0, weight=1)

    top = ctk.CTkFrame(
      panel,
      fg_color="transparent"
    )
    top.grid(
      row=0,
      column=0,
      sticky="ew",
      padx=20,
      pady=(20, 16)
    )

    top.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
      top,
      text="Performance Overview",
      font=FONT_HEADING,
      text_color=TEXT
    ).grid(
      row=0,
      column=0,
      sticky="w"
    )

    ctk.CTkLabel(
      top,
      text="Updated just now",
      font=FONT_SMALL,
      text_color=TEXT_SECONDARY
    ).grid(
      row=0,
      column=1,
      sticky="e"
    )

    chart_container = ctk.CTkFrame(
      panel,
      fg_color=SURFACE,
      corner_radius=16,
      border_width=1,
      border_color=BORDER,
      height=320
    )
    chart_container.grid(
      row=1,
      column=0,
      sticky="ew",
      padx=20,
      pady=(0, 20)
    )

    chart_container.grid_propagate(False)

    canvas = tk.Canvas(
      chart_container,
      bg="#141A22",
      highlightthickness=0
    )
    canvas.pack(
      fill="both",
      expand=True,
      padx=14,
      pady=14
    )

    self.after(
      100,
      lambda: self.draw_chart(canvas)
    )

    bottom = ctk.CTkFrame(
      panel,
      fg_color="transparent"
    )
    bottom.grid(
      row=2,
      column=0,
      sticky="ew",
      padx=20,
      pady=(0, 20)
    )

    bottom.grid_columnconfigure((0, 1), weight=1)

    left_summary = ctk.CTkFrame(
      bottom,
      fg_color=SURFACE,
      corner_radius=16,
      border_width=1,
      border_color=BORDER
    )
    left_summary.grid(
      row=0,
      column=0,
      sticky="nsew",
      padx=(0, 10)
    )

    ctk.CTkLabel(
      left_summary,
      text="Top Categories",
      font=FONT_HEADING,
      text_color=TEXT
    ).pack(
      anchor="w",
      padx=18,
      pady=(18, 12)
    )

    categories = [
      ("Accessories", "42%"),
      ("Displays", "28%"),
      ("Audio", "18%"),
      ("Cables", "12%")
    ]

    for name, percent in categories:
      row = ctk.CTkFrame(
        left_summary,
        fg_color="transparent"
      )
      row.pack(
        fill="x",
        padx=18,
        pady=6
      )

      ctk.CTkLabel(
        row,
        text=name,
        font=FONT_BODY,
        text_color=TEXT_SECONDARY
      ).pack(side="left")

      ctk.CTkLabel(
        row,
        text=percent,
        font=FONT_BODY,
        text_color=PRIMARY
      ).pack(side="right")

    right_summary = ctk.CTkFrame(
      bottom,
      fg_color=SURFACE,
      corner_radius=16,
      border_width=1,
      border_color=BORDER
    )
    right_summary.grid(
      row=0,
      column=1,
      sticky="nsew",
      padx=(10, 0)
    )

    ctk.CTkLabel(
      right_summary,
      text="System Insights",
      font=FONT_HEADING,
      text_color=TEXT
    ).pack(
      anchor="w",
      padx=18,
      pady=(18, 12)
    )

    insights = [
      "• Sales increased by 12% this week",
      "• Keyboard remains top-selling item",
      "• Low stock detected in Audio category",
      "• Customer retention improved by 8%"
    ]

    for insight in insights:
      ctk.CTkLabel(
        right_summary,
        text=insight,
        font=FONT_BODY,
        text_color=TEXT_SECONDARY,
        justify="left",
        anchor="w"
      ).pack(
        fill="x",
        padx=18,
        pady=6
      )

  def draw_chart(self, canvas):

    canvas.delete("all")

    width = canvas.winfo_width()
    height = canvas.winfo_height()

    if width <= 1 or height <= 1:
      self.after(
        100,
        lambda: self.draw_chart(canvas)
      )
      return

    points = [
      60,
      120,
      90,
      180,
      140,
      220,
      190,
      260
    ]

    spacing = width / (len(points) + 1)

    coords = []

    for index, value in enumerate(points):
      x = (index + 1) * spacing
      y = height - value

      coords.extend([x, y])

    canvas.create_line(
      coords,
      fill=PRIMARY,
      width=4,
      smooth=True
    )

    for i in range(0, len(coords), 2):
      canvas.create_oval(
        coords[i] - 5,
        coords[i + 1] - 5,
        coords[i] + 5,
        coords[i + 1] + 5,
        fill=PRIMARY,
        outline=""
      )

  def generate_report(self):

    Toast(
      self.winfo_toplevel(),
      "Generating analytics report..."
    )

class SettingsPage(ctk.CTkFrame):

  def __init__(self, parent):
    super().__init__(
      parent,
      fg_color="transparent"
    )

    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(1, weight=1)

    self.build_header()
    self.build_settings_content()

  def build_header(self):

    header = ctk.CTkFrame(
      self,
      fg_color="transparent"
    )
    header.grid(
      row=0,
      column=0,
      sticky="ew",
      padx=24,
      pady=(24, 18)
    )

    header.grid_columnconfigure(0, weight=1)

    left = ctk.CTkFrame(
      header,
      fg_color="transparent"
    )
    left.grid(
      row=0,
      column=0,
      sticky="w"
    )

    ctk.CTkLabel(
      left,
      text="Settings",
      font=FONT_TITLE,
      text_color=TEXT
    ).pack(anchor="w")

    ctk.CTkLabel(
      left,
      text="Customize system preferences and application behavior",
      font=FONT_BODY,
      text_color=TEXT_SECONDARY
    ).pack(anchor="w", pady=(4, 0))

  def build_settings_content(self):

    content = ctk.CTkScrollableFrame(
      self,
      fg_color="transparent"
    )
    content.grid(
      row=1,
      column=0,
      sticky="nsew",
      padx=24,
      pady=(0, 24)
    )

    self.build_appearance_section(content)
    self.build_system_section(content)
    self.build_security_section(content)

  def build_appearance_section(self, parent):

    section = ctk.CTkFrame(
      parent,
      fg_color=CARD,
      corner_radius=18,
      border_width=1,
      border_color=BORDER
    )
    section.pack(
      fill="x",
      pady=(0, 18)
    )

    ctk.CTkLabel(
      section,
      text="Appearance",
      font=FONT_HEADING,
      text_color=TEXT
    ).pack(
      anchor="w",
      padx=20,
      pady=(20, 16)
    )

    theme_row = ctk.CTkFrame(
      section,
      fg_color="transparent"
    )
    theme_row.pack(
      fill="x",
      padx=20,
      pady=(0, 14)
    )

    ctk.CTkLabel(
      theme_row,
      text="Theme Mode",
      font=FONT_BODY,
      text_color=TEXT
    ).pack(side="left")

    self.theme_option = ctk.CTkOptionMenu(
      theme_row,
      values=[
        "Dark",
        "Light",
        "System"
      ],
      width=180,
      height=40,
      corner_radius=12,
      fg_color=SURFACE,
      button_color=PRIMARY,
      button_hover_color=PRIMARY_HOVER,
      dropdown_fg_color=CARD,
      dropdown_hover_color=SURFACE,
      text_color=TEXT,
      font=FONT_BODY,
      command=self.change_theme
    )
    self.theme_option.pack(side="right")

    accent_row = ctk.CTkFrame(
      section,
      fg_color="transparent"
    )
    accent_row.pack(
      fill="x",
      padx=20,
      pady=(0, 20)
    )

    ctk.CTkLabel(
      accent_row,
      text="Accent Style",
      font=FONT_BODY,
      text_color=TEXT
    ).pack(side="left")

    accent_container = ctk.CTkFrame(
      accent_row,
      fg_color="transparent"
    )
    accent_container.pack(side="right")

    colors = [
      "#D4AF37",
      "#4A90E2",
      "#50C878",
      "#FF6B6B"
    ]

    for color in colors:
      dot = ctk.CTkButton(
        accent_container,
        text="",
        width=26,
        height=26,
        corner_radius=999,
        fg_color=color,
        hover_color=color,
        border_width=2,
        border_color=BORDER
      )
      dot.pack(side="left", padx=4)

  def build_system_section(self, parent):

    section = ctk.CTkFrame(
      parent,
      fg_color=CARD,
      corner_radius=18,
      border_width=1,
      border_color=BORDER
    )
    section.pack(
      fill="x",
      pady=(0, 18)
    )

    ctk.CTkLabel(
      section,
      text="System Preferences",
      font=FONT_HEADING,
      text_color=TEXT
    ).pack(
      anchor="w",
      padx=20,
      pady=(20, 16)
    )

    options = [
      ("Enable Notifications", True),
      ("Auto Backup Data", True),
      ("Play UI Sounds", False),
      ("Enable Animations", True),
    ]

    for label, value in options:

      row = ctk.CTkFrame(
        section,
        fg_color="transparent"
      )
      row.pack(
        fill="x",
        padx=20,
        pady=10
      )

      left = ctk.CTkFrame(
        row,
        fg_color="transparent"
      )
      left.pack(side="left")

      ctk.CTkLabel(
        left,
        text=label,
        font=FONT_BODY,
        text_color=TEXT
      ).pack(anchor="w")

      ctk.CTkLabel(
        left,
        text="System configuration option",
        font=FONT_SMALL,
        text_color=TEXT_SECONDARY
      ).pack(anchor="w")

      switch = ctk.CTkSwitch(
        row,
        text="",
        progress_color=PRIMARY,
        button_color="white",
        button_hover_color="#F5F5F5"
      )
      switch.pack(side="right")

      if value:
        switch.select()

    save_btn = ctk.CTkButton(
      section,
      text="Save Preferences",
      height=44,
      corner_radius=14,
      fg_color=PRIMARY,
      hover_color=PRIMARY_HOVER,
      text_color="#111111",
      font=("Inter", 13, "bold"),
      command=self.save_settings
    )
    save_btn.pack(
      anchor="e",
      padx=20,
      pady=(18, 20)
    )

  def build_security_section(self, parent):

    section = ctk.CTkFrame(
      parent,
      fg_color=CARD,
      corner_radius=18,
      border_width=1,
      border_color=BORDER
    )
    section.pack(
      fill="x"
    )

    ctk.CTkLabel(
      section,
      text="Security",
      font=FONT_HEADING,
      text_color=TEXT
    ).pack(
      anchor="w",
      padx=20,
      pady=(20, 16)
    )

    fields = [
      "Current Password",
      "New Password",
      "Confirm Password"
    ]

    self.security_entries = []

    for field in fields:
      wrapper = ctk.CTkFrame(
        section,
        fg_color="transparent"
      )
      wrapper.pack(
        fill="x",
        padx=20,
        pady=8
      )

      ctk.CTkLabel(
        wrapper,
        text=field,
        font=FONT_BODY,
        text_color=TEXT
      ).pack(anchor="w", pady=(0, 6))

      entry = ctk.CTkEntry(
        wrapper,
        height=42,
        corner_radius=12,
        fg_color=SURFACE,
        border_color=BORDER,
        text_color=TEXT,
        font=FONT_BODY,
        show="*"
      )
      entry.pack(fill="x")

      self.security_entries.append(entry)

    ctk.CTkButton(
      section,
      text="Update Password",
      height=44,
      corner_radius=14,
      fg_color=WARNING,
      hover_color="#F0A500",
      text_color="#111111",
      font=("Inter", 13, "bold"),
      command=self.update_password
    ).pack(
      anchor="e",
      padx=20,
      pady=(20, 20)
    )

  def change_theme(self, mode):

    if mode == "Dark":
      ctk.set_appearance_mode("dark")

    elif mode == "Light":
      ctk.set_appearance_mode("light")

    else:
      ctk.set_appearance_mode("system")

    Toast(
      self.winfo_toplevel(),
      f"Theme changed to {mode}"
    )

  def save_settings(self):

    Toast(
      self.winfo_toplevel(),
      "Preferences saved successfully"
    )

  def update_password(self):

    Toast(
      self.winfo_toplevel(),
      "Password updated successfully"
    )


# =============================================================
# MAIN APPLICATION CLASS
# =============================================================

class ModernInventoryApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ---------------------------------------------------------
        # WINDOW SETUP
        # ---------------------------------------------------------

        self.title("NU Marketplace Management System")
        self.geometry("1600x920")
        self.minsize(1280, 720)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.configure(
            fg_color=BACKGROUND
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

        self.attributes("-alpha", 0.0)

        # ---------------------------------------------------------
        # APP STATE
        # ---------------------------------------------------------

        self._is_running = True
        self._after_ids = []

        self.current_page = None
        self.nav_buttons = {}

        # ---------------------------------------------------------
        # LAYOUT
        # ---------------------------------------------------------

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------------------------------------------------
        # BUILD UI
        # ---------------------------------------------------------

        self.build_sidebar()
        self.build_main_content()

        # ---------------------------------------------------------
        # INITIAL PAGE
        # ---------------------------------------------------------

        self.show_page("dashboard")

        # ---------------------------------------------------------
        # STARTUP ANIMATION
        # ---------------------------------------------------------

        self.after(
            80,
            self.fade_in
        )

    # =========================================================
    # SIDEBAR
    # =========================================================

    def build_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=280,
            fg_color=SIDEBAR,
            corner_radius=0,
            border_width=0
        )
        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsw"
        )

        self.sidebar.grid_propagate(False)

        # -----------------------------------------------------
        # LOGO SECTION
        # -----------------------------------------------------

        logo_container = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent",
            height=110
        )
        logo_container.pack(
            fill="x",
            padx=24,
            pady=(26, 18)
        )

        logo_container.pack_propagate(False)

        logo_icon = ctk.CTkFrame(
            logo_container,
            width=54,
            height=54,
            fg_color=PRIMARY,
            corner_radius=16
        )
        logo_icon.pack(
            side="left"
        )

        logo_icon.pack_propagate(False)

        ctk.CTkLabel(
            logo_icon,
            text="NU",
            font=("Inter", 18, "bold"),
            text_color="#111111"
        ).place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        logo_text = ctk.CTkFrame(
            logo_container,
            fg_color="transparent"
        )
        logo_text.pack(
            side="left",
            padx=14
        )

        ctk.CTkLabel(
            logo_text,
            text="NU Marketplace",
            font=FONT_HEADING,
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            logo_text,
            text="Management System",
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY
        ).pack(anchor="w")

        # -----------------------------------------------------
        # NAVIGATION
        # -----------------------------------------------------

        nav_container = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        nav_container.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=(12, 0)
        )

        navigation_items = [
            ("dashboard", "Dashboard"),
            ("inventory", "Inventory"),
            ("cart", "Cart"),
            ("transactions", "Transactions"),
            ("users", "Users"),
            ("reports", "Reports"),
            ("settings", "Settings")
        ]

        for key, label in navigation_items:

            button = ctk.CTkButton(
                nav_container,
                text=label,
                anchor="w",
                height=48,
                corner_radius=14,
                fg_color="transparent",
                hover_color=CARD,
                text_color=TEXT_SECONDARY,
                font=FONT_BODY,
                border_width=0,
                command=lambda k=key: self.show_page(k)
            )

            button.pack(
                fill="x",
                pady=4
            )

            self.nav_buttons[key] = button

        # -----------------------------------------------------
        # USER PROFILE
        # -----------------------------------------------------

        profile = ctk.CTkFrame(
            self.sidebar,
            fg_color=CARD,
            corner_radius=18,
            border_width=1,
            border_color=BORDER,
            height=88
        )
        profile.pack(
            fill="x",
            padx=18,
            pady=18
        )

        profile.pack_propagate(False)

        avatar = ctk.CTkFrame(
            profile,
            width=52,
            height=52,
            fg_color=PRIMARY,
            corner_radius=999
        )
        avatar.pack(
            side="left",
            padx=16,
            pady=16
        )

        avatar.pack_propagate(False)

        ctk.CTkLabel(
            avatar,
            text="K",
            font=("Inter", 18, "bold"),
            text_color="#111111"
        ).place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        user_info = ctk.CTkFrame(
            profile,
            fg_color="transparent"
        )
        user_info.pack(
            side="left"
        )

        ctk.CTkLabel(
            user_info,
            text="Kim Cedrick",
            font=FONT_BODY,
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            user_info,
            text="Administrator",
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY
        ).pack(anchor="w")

    # =========================================================
    # MAIN CONTENT
    # =========================================================

    def build_main_content(self):

        self.main_content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.main_content.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

        # -----------------------------------------------------
        # TOPBAR
        # -----------------------------------------------------

        self.topbar = ctk.CTkFrame(
            self.main_content,
            height=78,
            fg_color=SURFACE,
            corner_radius=0,
            border_width=0
        )
        self.topbar.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        self.topbar.grid_propagate(False)

        left = ctk.CTkFrame(
            self.topbar,
            fg_color="transparent"
        )
        left.pack(
            side="left",
            padx=24,
            pady=18
        )

        self.lbl_page_title = ctk.CTkLabel(
            left,
            text="Dashboard",
            font=FONT_HEADING,
            text_color=TEXT
        )
        self.lbl_page_title.pack(anchor="w")

        self.lbl_page_subtitle = ctk.CTkLabel(
            left,
            text="Monitor and manage your marketplace system",
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY
        )
        self.lbl_page_subtitle.pack(anchor="w")

        right = ctk.CTkFrame(
            self.topbar,
            fg_color="transparent"
        )
        right.pack(
            side="right",
            padx=24,
            pady=18
        )

        self.global_search = ctk.CTkEntry(
            right,
            width=260,
            height=40,
            corner_radius=12,
            placeholder_text="Search...",
            fg_color=CARD,
            border_color=BORDER,
            text_color=TEXT,
            font=FONT_BODY
        )
        self.global_search.pack(
            side="left",
            padx=(0, 12)
        )

        self.notification_btn = ctk.CTkButton(
            right,
            text="🔔",
            width=42,
            height=42,
            corner_radius=12,
            fg_color=CARD,
            hover_color=SURFACE,
            border_width=1,
            border_color=BORDER,
            text_color=TEXT,
            font=("Inter", 16),
            command=self.show_notifications
        )
        self.notification_btn.pack(side="left")

        # -----------------------------------------------------
        # PAGE CONTAINER
        # -----------------------------------------------------

        self.page_container = ctk.CTkFrame(
            self.main_content,
            fg_color="transparent"
        )
        self.page_container.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.page_container.grid_rowconfigure(0, weight=1)
        self.page_container.grid_columnconfigure(0, weight=1)

        # -----------------------------------------------------
        # PAGE INSTANCES
        # -----------------------------------------------------

        self.pages = {
            "dashboard": DashboardPage(self.page_container),
            "inventory": InventoryPage(self.page_container),
            "cart": CartPage(self.page_container),
            "transactions": TransactionHistoryPage(self.page_container),
            "users": UserManagementPage(self.page_container),
            "reports": ReportsPage(self.page_container),
            "settings": SettingsPage(self.page_container)
        }

        for page in self.pages.values():

            page.grid(
                row=0,
                column=0,
                sticky="nsew"
            )

    # =========================================================
    # PAGE NAVIGATION
    # =========================================================

    def show_page(self, name):

        if self.current_page == name:
            return

        page_titles = {
            "dashboard": (
                "Dashboard",
                "Monitor and manage your marketplace system"
            ),
            "inventory": (
                "Inventory",
                "Track products and stock levels"
            ),
            "cart": (
                "Shopping Cart",
                "Review customer purchases and checkout"
            ),
            "transactions": (
                "Transactions",
                "View payment and sales history"
            ),
            "users": (
                "User Management",
                "Manage users and permissions"
            ),
            "reports": (
                "Reports & Analytics",
                "Track business performance and insights"
            ),
            "settings": (
                "Settings",
                "Configure preferences and system options"
            )
        }

        title, subtitle = page_titles.get(
            name,
            ("Dashboard", "")
        )

        self.lbl_page_title.configure(
            text=title
        )

        self.lbl_page_subtitle.configure(
            text=subtitle
        )

        for key, button in self.nav_buttons.items():

            if key == name:

                button.configure(
                    fg_color=PRIMARY,
                    hover_color=PRIMARY_HOVER,
                    text_color="#111111"
                )

            else:

                button.configure(
                    fg_color="transparent",
                    hover_color=CARD,
                    text_color=TEXT_SECONDARY
                )

        self.pages[name].tkraise()

        self.current_page = name

    # =========================================================
    # TOAST / NOTIFICATIONS
    # =========================================================

    def show_notifications(self):

        Toast(
            self,
            "No new notifications"
        )

    # =========================================================
    # WINDOW ANIMATIONS
    # =========================================================

    def fade_in(self):

        animate(
            self,
            0.0,
            1.0,
            320,
            lambda value: self.attributes(
                "-alpha",
                value
            )
        )

    def fade_out(self, callback=None):

        animate(
            self,
            1.0,
            0.0,
            220,
            lambda value: self.attributes(
                "-alpha",
                value
            ),
            on_complete=callback
        )

    # =========================================================
    # SHUTDOWN
    # =========================================================

    def on_close(self):

        self._is_running = False

        for after_id in self._after_ids:

            try:
                self.after_cancel(after_id)

            except:
                pass

        self.fade_out(
            self.destroy
        )


# =============================================================
# ENTRY POINT
# =============================================================

if __name__ == "__main__":

    app = ModernInventoryApp()

    app.mainloop()

# =============================================================
# OPTIONAL ADVANCED ANIMATION UTILITIES
# =============================================================

def hex_to_rgb(color):

    color = color.lstrip("#")

    return tuple(
        int(color[i:i + 2], 16)
        for i in (0, 2, 4)
    )


def rgb_to_hex(rgb):

    return "#%02x%02x%02x" % rgb


def interpolate_color(start, end, t):

    start_rgb = hex_to_rgb(start)
    end_rgb = hex_to_rgb(end)

    result = tuple(
        int(
            start_rgb[i] + (
                end_rgb[i] - start_rgb[i]
            ) * t
        )
        for i in range(3)
    )

    return rgb_to_hex(result)


# =============================================================
# ADVANCED HOVER BUTTON
# =============================================================

class AnimatedButton(ctk.CTkButton):

    def __init__(
        self,
        parent,
        default_color,
        hover_color,
        **kwargs
    ):

        super().__init__(
            parent,
            fg_color=default_color,
            hover_color=hover_color,
            **kwargs
        )

        self.default_color = default_color
        self.target_hover = hover_color

        self.bind(
            "<Enter>",
            self.on_enter
        )

        self.bind(
            "<Leave>",
            self.on_leave
        )

    def animate_to(self, target):

        start = self.cget("fg_color")

        if isinstance(start, tuple):
            start = start[1]

        if isinstance(target, tuple):
            target = target[1]

        steps = 10

        for i in range(steps + 1):

            t = i / steps

            color = interpolate_color(
                start,
                target,
                t
            )

            self.after(
                i * 15,
                lambda c=color: self.configure(
                    fg_color=c
                )
            )

    def on_enter(self, event):

        self.animate_to(
            self.target_hover
        )

    def on_leave(self, event):

        self.animate_to(
            self.default_color
        )


# =============================================================
# LOADING OVERLAY
# =============================================================

class LoadingOverlay(ctk.CTkFrame):

    def __init__(self, parent, text="Loading..."):
        super().__init__(
            parent,
            fg_color=(
                "#FFFFFF",
                "#111111"
            )
        )

        self.place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

        container = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=18,
            border_width=1,
            border_color=BORDER,
            width=260,
            height=180
        )
        container.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        container.pack_propagate(False)

        self.spinner = Spinner(
            container
        )
        self.spinner.pack(
            pady=(32, 16)
        )

        self.spinner.start()

        ctk.CTkLabel(
            container,
            text=text,
            font=FONT_BODY,
            text_color=TEXT
        ).pack()

    def destroy_overlay(self):

        self.spinner.stop()

        self.destroy()


# =============================================================
# CONFIRM DIALOG
# =============================================================

class ConfirmDialog(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        title,
        message
    ):

        super().__init__(parent)

        self.result = False

        self.title(title)

        self.geometry("420x220")

        self.resizable(False, False)

        self.configure(
            fg_color=BACKGROUND
        )

        self.transient(parent)

        self.grab_set()

        self.build_ui(
            title,
            message
        )

        self.wait_window()

    def build_ui(
        self,
        title,
        message
    ):

        container = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=20,
            border_width=1,
            border_color=BORDER
        )
        container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            container,
            text=title,
            font=FONT_HEADING,
            text_color=TEXT
        ).pack(
            pady=(26, 10)
        )

        ctk.CTkLabel(
            container,
            text=message,
            font=FONT_BODY,
            text_color=TEXT_SECONDARY,
            justify="center",
            wraplength=300
        ).pack(
            padx=20
        )

        actions = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )
        actions.pack(
            pady=24
        )

        cancel_btn = ctk.CTkButton(
            actions,
            text="Cancel",
            width=120,
            height=42,
            corner_radius=12,
            fg_color=SURFACE,
            hover_color=CARD,
            border_width=1,
            border_color=BORDER,
            text_color=TEXT,
            font=FONT_BODY,
            command=self.cancel
        )
        cancel_btn.pack(
            side="left",
            padx=8
        )

        confirm_btn = ctk.CTkButton(
            actions,
            text="Confirm",
            width=120,
            height=42,
            corner_radius=12,
            fg_color=DANGER,
            hover_color="#D64545",
            text_color="white",
            font=FONT_BODY,
            command=self.confirm
        )
        confirm_btn.pack(
            side="left",
            padx=8
        )

    def confirm(self):

        self.result = True

        self.destroy()

    def cancel(self):

        self.result = False

        self.destroy()


# =============================================================
# EMPTY STATE COMPONENT
# =============================================================

class EmptyState(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        icon="📦",
        title="No Data Found",
        subtitle="There is currently nothing to display.",
        button_text="Refresh",
        command=None
    ):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.build_ui(
            icon,
            title,
            subtitle,
            button_text,
            command
        )

    def build_ui(
        self,
        icon,
        title,
        subtitle,
        button_text,
        command
    ):

        wrapper = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        wrapper.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        ctk.CTkLabel(
            wrapper,
            text=icon,
            font=("Segoe UI Emoji", 52),
            text_color=TEXT_SECONDARY
        ).pack(
            pady=(0, 14)
        )

        ctk.CTkLabel(
            wrapper,
            text=title,
            font=FONT_HEADING,
            text_color=TEXT
        ).pack()

        ctk.CTkLabel(
            wrapper,
            text=subtitle,
            font=FONT_BODY,
            text_color=TEXT_SECONDARY
        ).pack(
            pady=(6, 18)
        )

        ctk.CTkButton(
            wrapper,
            text=button_text,
            width=150,
            height=42,
            corner_radius=12,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            text_color="#111111",
            font=FONT_BODY,
            command=command
        ).pack()


# =============================================================
# KEYBOARD SHORTCUTS
# =============================================================

def bind_global_shortcuts(app):

    app.bind(
        "<Control-n>",
        lambda e: Toast(
            app,
            "Create new item shortcut triggered"
        )
    )

    app.bind(
        "<Control-s>",
        lambda e: Toast(
            app,
            "Save shortcut triggered"
        )
    )

    app.bind(
        "<Control-f>",
        lambda e: app.global_search.focus()
    )

    app.bind(
        "<Escape>",
        lambda e: app.on_close()
    )

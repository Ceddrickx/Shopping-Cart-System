# 🎒 MP5 — NUmart Shopping Cart System
> **Data Structures and Algorithms | IT-252 | Term 3 | A.Y. 2025–2026**

---

## 📌 Project Overview
A terminal-based **Shopping Cart System** built in Python that simulates buyer login, item browsing, cart management, checkout, and payment for **NUmart** — a school supplies store. Each core module applies a specific data structure discussed in class.

---

## 📁 File Structure
```
shopping-cart-system/
│
├── main.py          ← Entry point — CLI menus and user interaction (run this)
├── system.py        ← Core logic — NUmart class, login, cart, promo, payment, receipt
├── structures.py    ← Data structures — LinkedList, CartLinkedList, Stack, Queue
└── README.md
```

---

## 👥 Group Members & Task Distribution

> **Group 4**
> Cachapero, Ecks Matthew | Feleo, Alyanna Gabrinne | Isaac, Raphael | Naelgas, Kirby Wayne | Villar, Kim Cedrick

---

### 👤 Member 1 — Feleo
**Role:** Project Lead / Inventory & Main Menu

| Task | Location |
|------|----------|
| Define `ItemNode` and `LinkedList` for inventory | `structures.py` |
| Pre-load 25 school supply items into inventory | `system.py` → `_load_inventory()` |
| Build main menu and integrate all modules | `main.py` → `main_menu()` |
| Buyer login system with 3-attempt limit | `system.py` → `buyer_login()` |

> **Data Structure:** `Linked List` — inventory catalog

---

### 👤 Member 2 — Naelgas
**Role:** Cart Operations & Undo Feature

| Task | Location |
|------|----------|
| Define `CartNode` and `CartLinkedList` | `structures.py` |
| Add item to cart with stock validation | `system.py` → `add_to_cart()` |
| Remove item from cart | `system.py` → `remove_from_cart()` |
| Display cart contents with subtotals | `system.py` → `display_cart()` |
| Undo last add/remove action | `system.py` → `undo_last_action()` |

> **Data Structure:** `Linked List` — cart | `Stack` — undo operations

---

### 👤 Member 3 — Villar
**Role:** Price Calculation & Promo Codes

| Task | Location |
|------|----------|
| Compute subtotal of all cart items | `system.py` → `get_final_total()` |
| Apply and remove promo codes with discount | `system.py` → `apply_promo()`, `remove_promo()` |
| Display full price summary | `system.py` → `display_price_summary()` |
| Review and merge all Pull Requests | GitHub |

> **Data Structure:** `Queue` — transaction history

---

### 👤 Member 4 — Cachapero
**Role:** Payment Simulation

| Task | Location |
|------|----------|
| Cash payment flow and change computation | `system.py` → `_pay_cash()` |
| Card payment flow with 16-digit validation | `system.py` → `_pay_card()` |
| E-Wallet flow — GCash, Maya, ShopeePay | `system.py` → `_pay_ewallet()` |
| Payment method selection and processing | `system.py` → `process_payment()` |

> **Data Structure:** `Stack` — undo stack used during cart/payment session

---

### 👤 Member 5 — Isaac
**Role:** Receipt & Transaction History

| Task | Location |
|------|----------|
| Generate formatted receipt on terminal | `system.py` → `_generate_receipt()` |
| Deduct purchased quantities from inventory | `system.py` → `_generate_receipt()` |
| Store and display transaction history | `structures.py` → `Queue` |
| Reset cart, discount, and undo stack after checkout | `system.py` → `_generate_receipt()` |

> **Data Structure:** `Queue` — transaction history log (FIFO)

---

## 🗂️ Data Structures Used

| Data Structure | Defined In | Purpose |
|----------------|------------|---------|
| `LinkedList` | `structures.py` | Inventory catalog (25 items) |
| `CartLinkedList` | `structures.py` | Shopping cart items |
| `Stack` | `structures.py` | Undo last cart action (LIFO) |
| `Queue` | `structures.py` | Transaction history (FIFO) |

---

## 🛠️ System Features
- ✅ Buyer login with username/password and 3-attempt limit
- ✅ Browse 25 pre-loaded school supply items
- ✅ Add and remove items from cart with stock validation
- ✅ Undo last cart action
- ✅ Apply and remove promo codes (SAVE10, STUDENT15, NUFV30, BACKTOSCHOOL45)
- ✅ Full price summary with discount breakdown
- ✅ Cash, Card, and E-Wallet (GCash, Maya, ShopeePay) payment simulation
- ✅ Formatted receipt generation on terminal
- ✅ Transaction history stored and viewable per session
- ✅ Input validation and error handling throughout

---

## 💳 Promo Codes
| Code | Discount |
|------|----------|
| `SAVE10` | 10% off |
| `STUDENT15` | 15% off |
| `NUFV30` | 30% off |
| `BACKTOSCHOOL45` | 45% off |

---

## 📅 Presentation Details
- **Dates:** June 1 – June 2
- **Language:** Python only
- **Interface:** Terminal / Command Line (PyCharm or VS Code)

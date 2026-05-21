# 🎒 MP5 — Shopping Cart System with Payment Handling
> **Data Structures | Term 3 | A.Y. 2025–2026**

---

## 📌 Project Overview

A terminal-based **Shopping Cart System** built in Python that simulates item selection, checkout, and payment for a **School Supplies Store**. Each module applies a specific data structure discussed in class.

---

## 🚀 How to Run

> Make sure you have **Python 3.10+** installed.

```bash
# 1. Clone the repository
git clone https://github.com/Ceddrickx/shopping-cart-system.git

# 2. Go into the project folder
cd shopping-cart-system

# 3. Run the program
python main.py
```

---

## 📁 File Structure

```
shopping-cart-system/
│      
├── main.py                  ← Item Model, Linked List, Main Menu (Entry point run this)
├── member2_cart.py          ← Cart Operations, Undo Stack
├── member3_price.py         ← Price Calculation, Promo Queue
├── member4_payment.py       ← Payment Simulation, Payment Stack
├── member5_receipt.py       ← Receipt, Transaction History, Error Handling
└── README.md
```

---

## 👥 Group Member Task Distribution

### 👤 Member 1 (main.py) — Feleo & Isaac
**Role:** Project Lead / Item Model & Main Menu

| Task | Module |
|------|--------|
| Define the Item class (ID, name, category, price, quantity, expiration) | `Item` class |
| Search item by name or ID | Search module |
| Update item details | Update module |
| Build the main menu and integrate all modules | `main.py` |

> **Data Structure:** `Linked List` — item catalog / inventory

---

### 👤 Member 2 — Naelgas
**Role:** Cart Operations & Undo Feature

| Task | Module |
|------|--------|
| Add item to cart | Insert module |
| Remove item by name or ID | Delete module |
| Display cart contents | Display module |
| Undo last add/remove operation using stack transactions | Undo Stack |

> **Data Structure:** `Stack` — undo transaction history

---

### 👤 Member 3 — Villar
**Role:** Price Calculation & Promo Codes

| Task | Module |
|------|--------|
| Compute total price of all items in cart | Price module |
| Apply promo code or discount | Promo module |
| Display final payable amount (subtotal, discount, total) | Display module |
| Review and merge all Pull Requests | GitHub |

> **Data Structure:** `Queue` — promo code processing

---

### 👤 Member 4 — Cachapero
**Role:** Payment Simulation

| Task | Module |
|------|--------|
| Cash payment flow and change computation | Cash module |
| Card payment flow (card number input, validation) | Card module |
| E-Wallet payment flow (account/reference input) | E-Wallet module |
| Display payment confirmation screen | Confirmation module |

> **Data Structure:** `Stack` — payment method history

---

### 👤 Member 5 — All Members
**Role:** Receipt, Transaction History & Error Handling

| Task | Module |
|------|--------|
| Generate formatted receipt summary on terminal | Receipt module |
| Store and display past transaction history | History module |
| Handle empty structure operations and boundary conditions | Error Handling |

> **Data Structure:** `Circular Linked List` — transaction log / receipt history

---

## 🗂️ Data Structures Used

| Data Structure | Used By | Purpose |
|----------------|---------|---------|
| Linked List | Member 1 | Item catalog / inventory |
| Stack | Member 2 | Undo transaction history |
| Queue | Member 3 | Promo code processing |
| Stack | Member 4 | Payment method history |
| Circular Linked List | Member 5 | Transaction log / receipt history |

---

## 🛠️ System Features

- ✅ Add, remove, and display cart items
- ✅ Undo last cart action
- ✅ Apply promo codes with discount computation
- ✅ Cash, Card, and E-Wallet payment simulation
- ✅ Formatted receipt generation on terminal
- ✅ Transaction history with Circular Linked List
- ✅ Full error handling (empty structure, invalid input, boundary conditions)

---

## 📅 Presentation Details

- **Dates:** June 1 – June 2
- **Language:** Python only
- **Interface:** Terminal / Command Line (PyCharm or VS Code)

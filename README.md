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
├── main.py                  ← Entry point (run this)
├── member1_item.py          ← Item Model, Linked List, Main Menu
├── member2_cart.py          ← Cart Operations, Undo Stack
├── member3_price.py         ← Price Calculation, Promo Queue
├── member4_payment.py       ← Payment Simulation, Payment Stack
├── member5_receipt.py       ← Receipt, Transaction History, Error Handling
└── README.md
```

---

## 👥 Group Member Task Distribution

### 👤 Member 1 — Feleo & Isaac
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

---

## 🔧 Git Setup Guide for Members

> This project uses the **Fork + Pull Request** workflow.
> This means you work on your **own copy** of the repo and submit your code to **Kim (Ceddrickx)** for review before it gets merged.
> No one can directly edit the main repository except **Kim (Ceddrickx)**.
> Steps 1–6 are done **only once** when you first set up.

---

### ✅ STEP 1 — Install Git

1. Go to [https://git-scm.com/downloads](https://git-scm.com/downloads)
2. Download and install Git for your operating system
3. After installing, open a terminal and verify it works:

```bash
git --version
```

You should see something like `git version 2.x.x` ✅

---

### ✅ STEP 2 — Create a GitHub Account

1. Go to [https://github.com](https://github.com)
2. Sign up for a free account if you don't have one yet

> You do **not** need to be added as a collaborator for this workflow. Anyone can fork.

---

### ✅ STEP 3 — Fork the Repository

Forking creates your own personal copy of Kim's repo under your GitHub account.

1. Go to: [https://github.com/Ceddrickx/shopping-cart-system](https://github.com/Ceddrickx/shopping-cart-system)
2. Click the **Fork** button at the top right of the page
3. Click **Create fork**
4. You now have your own copy at:
   `https://github.com/YOUR_USERNAME/shopping-cart-system` ✅

---

### ✅ STEP 4 — Set Up Git Identity on Your PC (first time only)

Open your terminal (VS Code terminal or Command Prompt) and run:

```bash
git config --global user.name "Your Full Name"
git config --global user.email "your_email@gmail.com"
```

> Use the **same email** you used to sign up on GitHub.

---

### ✅ STEP 5 — Clone YOUR Fork (not Kim's)

Download **your fork** to your PC:

```bash
git clone https://github.com/YOUR_USERNAME/shopping-cart-system.git
```

Then navigate into the project folder:

```bash
cd shopping-cart-system
```

You should now see all the project files on your PC ✅

---

### ✅ STEP 6 — Connect to Kim's Original Repo

This lets you pull the latest updates from Kim's repo anytime:

```bash
git remote add upstream https://github.com/Ceddrickx/shopping-cart-system.git
```

Verify the connection:

```bash
git remote -v
```

You should see both `origin` (your fork) and `upstream` (Kim's repo) ✅

---

### ✅ STEP 7 — Open the Project in Your Editor

**If using VS Code:**
```bash
code .
```

**If using PyCharm:**
- Open PyCharm → Click **Open** → Select the `shopping-cart-system` folder

---

### ✅ STEP 8 — Know Your Assigned File

Only edit the file assigned to you:

| Member | Assigned File/s |
|--------|----------------|
| Feleo & Isaac | `main.py` and `member1_item.py` |
| Naelgas | `member2_cart.py` |
| Villar  | `member3_price.py` |
| Cachapero | `member4_payment.py` |
| All Members | `member5_receipt.py` |

> ⚠️ **Do NOT edit files that belong to other members.**

---

### ✅ STEP 9 — Sync with Kim's Repo Before Coding (Every Session)

Before coding each session, always get the latest updates from Kim's original repo first:

```bash
git pull upstream main
```

Then update your own fork too:

```bash
git push origin main
```

> Always do this before you start coding to avoid conflicts. ⚠️

---

### ✅ STEP 10 — Push Your Code to YOUR Fork

Once you're done editing your assigned file, run these **3 commands in order**:

```bash
# 1. Stage your file (tell Git which file you changed)
git add your_file.py

# 2. Commit with a short message describing what you did
git commit -m "Your name: describe what you added or changed"

# 3. Push to YOUR fork (not Kim's repo)
git push origin main
```

**Real examples per member:**

```bash
# Feleo & Isaac (Member 1)
git add member1_item.py
git commit -m "Feleo: finished Item class and linked list catalog"
git push origin main

# Naelgas (Member 2)
git add member2_cart.py
git commit -m "Naelgas: finished add to cart and undo stack"
git push origin main

# Villar (Member 3)
git add member3_price.py
git commit -m "Villar: added promo queue and discount logic"
git push origin main

# Cachapero (Member 4)
git add member4_payment.py
git commit -m "Cachapero: completed cash and e-wallet payment flow"
git push origin main
```

---

### ✅ STEP 11 — Create a Pull Request to Kim's Repo

This is how your code gets submitted to the main repository for Kim to review.

1. Go to your fork on GitHub:
   `https://github.com/YOUR_USERNAME/shopping-cart-system`
2. Click **Contribute** → **Open Pull Request**
3. Make sure it says:
   - **base repository:** `Ceddrickx/shopping-cart-system` ← Kim's main repo
   - **head repository:** `YOUR_USERNAME/shopping-cart-system` ← your fork
4. Add a title like: `"Naelgas - Member 2: Cart Operations done"`
5. Click **Create Pull Request** ✅

> Kim will receive a notification and review your code before merging it into the main repo.

---

### ✅ STEP 12 — Wait for Kim to Merge

Kim (Ceddrickx) will:
- Review your submitted code
- Request changes if needed — just fix them and push again to your fork, the Pull Request updates automatically
- Merge it into the main repo once everything looks good ✅

---

## 👑 Guide  

When a teammate submits a Pull Request:

1. Go to your repo → click the **Pull Requests** tab
2. Click the Pull Request to open and review it
3. Check the **Files changed** tab — make sure they only edited their assigned file
4. If everything looks good → click **Merge pull request** → **Confirm merge** ✅
5. If there's an issue → click **Request changes** and leave a comment explaining what to fix

---

## ⚠️ Common Errors & Fixes

| Error | What It Means | Fix |
|-------|--------------|-----|
| `git push` rejected | Pushing to Kim's repo directly | Make sure you cloned YOUR fork, not Kim's |
| `fatal: not a git repository` | You're in the wrong folder | Run `cd shopping-cart-system` first |
| Merge conflict | Two people edited the same file | Message Kim immediately — do NOT force push |
| Pull Request has conflicts | Your fork is outdated | Run `git pull upstream main` then push again |
| `fatal: unable to access` | No internet or wrong URL | Check your connection and the repo URL |

---

## 💬 Daily Workflow Summary

```
Every coding session — follow this order:

1.  git pull upstream main       ← get latest from Kim's repo
2.  git push origin main         ← update your own fork
3.  Edit ONLY your assigned file
4.  git add your_file.py         ← stage your changes
5.  git commit -m "message"      ← describe what you did
6.  git push origin main         ← push to your fork
7.  Open Pull Request on GitHub  ← submit to Kim for review
```

---

## 🔗 Repository Link

> [https://github.com/Ceddrickx/shopping-cart-system](https://github.com/Ceddrickx/shopping-cart-system)

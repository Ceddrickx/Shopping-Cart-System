# ============================================================
# system.py
# NUmart - Study smart. Shop smart.
# Contains all system logic:
#   - Inventory setup (pre-loaded 25 items)
#   - Cart operations
#   - Undo operations
#   - Price calculation & promo codes
#   - Payment simulation
#   - Receipt generation
#   - Admin inventory management
# ============================================================

import datetime
from structures import LinkedList, CartLinkedList, Stack, Queue


# ─────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────

ADMIN_PIN = "2026"

PROMO_CODES = {
    "SAVE10"        : 10,
    "STUDENT15"     : 15,
    "NUFV30"        : 30,
    "BACKTOSCHOOL45": 45
}


# ─────────────────────────────────────────
# NUMART SYSTEM CLASS
# ─────────────────────────────────────────

class NUmart:
    """
    Main system class for NUmart Shopping Cart System.
    Manages inventory, cart, undo stack, and transaction history queue.
    """

    def __init__(self):
        self.inventory   = LinkedList()       # stores all shop items
        self.cart        = CartLinkedList()   # stores items added by customer
        self.undo_stack  = Stack()            # tracks cart actions for undo
        self.history     = Queue()            # stores completed transactions
        self.discount    = 0                  # current applied discount (%)
        self.promo_used  = ""                 # currently applied promo code

        # load the 25 pre-loaded items on startup
        self._load_inventory()

    # ─────────────────────────────────────
    # PRE-LOAD INVENTORY
    # ─────────────────────────────────────

    def _load_inventory(self):
        """Pre-load all 25 school supply items into the inventory linked list."""
        items = [
            # ID     Name                    Category    Price   Qty   Expiration
            ("001", "Ballpen (Black)",       "Writing",  12.00,  250,  "None"),
            ("002", "Ballpen (Red)",         "Writing",  12.00,  120,  "None"),
            ("003", "Pencil (Mongol)",       "Writing",  15.00,  200,  "None"),
            ("004", "Highlighter",           "Writing",  45.00,  80,   "None"),
            ("005", "Permanent Marker",      "Writing",  55.00,  60,   "None"),
            ("006", "Notebook (50 leaves)",  "Paper",    35.00,  150,  "None"),
            ("007", "Notebook (100 leaves)", "Paper",    60.00,  120,  "None"),
            ("008", "Pad Paper",             "Paper",    28.00,  200,  "None"),
            ("009", "Bond Paper (Short)",    "Paper",    3.00,   1000, "None"),
            ("010", "Folder (Long)",         "Paper",    15.00,  180,  "None"),
            ("011", "Scissors",              "Tools",    65.00,  40,   "None"),
            ("012", "Ruler (30cm)",          "Tools",    20.00,  100,  "None"),
            ("013", "Compass",               "Tools",    85.00,  35,   "None"),
            ("014", "Stapler",               "Tools",    95.00,  30,   "None"),
            ("015", "Tape (Clear)",          "Tools",    35.00,  80,   "None"),
            ("016", "Glue Stick",            "Adhesives",35.00,  70,   "2027-12-31"),
            ("017", "Paste (White)",         "Adhesives",45.00,  50,   "2027-06-30"),
            ("018", "Double-sided Tape",     "Adhesives",55.00,  40,   "None"),
            ("019", "Correction Tape",       "Adhesives",45.00,  100,  "None"),
            ("020", "Eraser",                "Adhesives",12.00,  180,  "None"),
            ("021", "Colored Paper",         "Art",      25.00,  150,  "None"),
            ("022", "Watercolor Paint",      "Art",      120.00, 25,   "2026-12-31"),
            ("023", "Crayons (12 colors)",   "Art",      55.00,  60,   "None"),
            ("024", "Coloring Pencils",      "Art",      95.00,  50,   "None"),
            ("025", "Sketchpad",             "Art",      85.00,  40,   "None"),
        ]
        for item in items:
            self.inventory.insert(*item)

    # ─────────────────────────────────────
    # CART OPERATIONS
    # ─────────────────────────────────────

    def add_to_cart(self, item_id, quantity):
        """
        Add an item to the cart after validating stock.
        Pushes the action to the undo stack.
        """
        item = self.inventory.search(item_id)

        if item is None:
            print(f"\n  [!] Item ID '{item_id}' not found in inventory.")
            return

        # check if requested quantity exceeds available stock
        cart_item = self.cart.search(item_id)
        already_in_cart = cart_item.quantity if cart_item else 0
        total_requested = already_in_cart + quantity

        if total_requested > item.quantity:
            available = item.quantity - already_in_cart
            if available <= 0:
                if item.quantity == 0:
                    print(f"\n  [!] '{item.name}' is out of stock.")
                else:
                    print(f"\n  [!] '{item.name}' is already maxed out in your cart.")
            else:
                print(f"\n  [!] Insufficient stock. Only {available} item(s) available for '{item.name}'.")
            return

        # add to cart
        self.cart.add_item(item.item_id, item.name, item.category, item.price, quantity)

        # push action to undo stack
        self.undo_stack.push({
            "action"  : "ADD",
            "item_id" : item.item_id,
            "name"    : item.name,
            "quantity": quantity
        })

        print(f"\n  [✓] {quantity}x '{item.name}' added to cart.")

    def remove_from_cart(self, item_id):
        """
        Remove an item from the cart by item ID.
        Pushes the action to the undo stack.
        """
        if self.cart.is_empty():
            print("\n  [!] Your cart is empty. Nothing to remove.")
            return

        cart_item = self.cart.search(item_id)
        if cart_item is None:
            print(f"\n  [!] Item ID '{item_id}' is not in your cart.")
            return

        # save details before removing for undo
        removed_qty      = cart_item.quantity
        removed_name     = cart_item.name
        removed_category = cart_item.category
        removed_price    = cart_item.price

        self.cart.remove_item(item_id)

        # push action to undo stack — capture category and price at removal
        # time so undo restores the exact original values, independent of any
        # subsequent admin edits to the inventory item
        self.undo_stack.push({
            "action"  : "REMOVE",
            "item_id" : item_id,
            "name"    : removed_name,
            "category": removed_category,
            "price"   : removed_price,
            "quantity": removed_qty
        })

        print(f"\n  [✓] '{removed_name}' removed from cart.")

    def display_cart(self):
        """Display all items in the cart with subtotals."""
        if self.cart.is_empty():
            print("\n  [!] Your cart is empty.")
            return

        self.cart.display()
        total = self.cart.compute_total()
        print(f"\n  Cart Total: ₱{total:.2f}")

        if self.discount > 0:
            discounted = total * (self.discount / 100)
            final      = total - discounted
            print(f"  Discount  : {self.discount}% (-₱{discounted:.2f})")
            print(f"  Amount Due: ₱{final:.2f}")

    # ─────────────────────────────────────
    # UNDO OPERATION
    # ─────────────────────────────────────

    def undo_last_action(self):
        """Undo the last add or remove action using the stack."""
        if self.undo_stack.is_empty():
            print("\n  [!] Nothing to undo.")
            return

        last_action = self.undo_stack.pop()
        action   = last_action["action"]
        item_id  = last_action["item_id"]
        name     = last_action["name"]
        quantity = last_action["quantity"]

        if action == "ADD":
            # undo an add → remove it from cart
            cart_item = self.cart.search(item_id)
            if cart_item is not None:
                if cart_item.quantity > quantity:
                    cart_item.quantity -= quantity
                else:
                    self.cart.remove_item(item_id)
                # success message only when item was actually found and removed
                print(f"\n  [✓] Undo successful — removed {quantity}x '{name}' from cart.")
            else:
                # item was not in the cart — undo cannot be completed
                print(f"\n  [!] Undo failed — '{name}' was not found in your cart.")

        elif action == "REMOVE":
            # undo a remove → re-add using category and price captured
            # at removal time, not the current live inventory state
            category = last_action["category"]
            price    = last_action["price"]
            self.cart.add_item(item_id, name, category, price, quantity)
            # add_item creates a new node or merges into an existing one
            print(f"\n  [✓] Undo successful — '{name}' added back to cart.")

    # ─────────────────────────────────────
    # PROMO CODE & PRICE CALCULATION
    # ─────────────────────────────────────

    def apply_promo(self, code):
        """Apply a promo code if valid. Updates the discount rate."""
        code = code.strip().upper()
        if code in PROMO_CODES:
            self.discount   = PROMO_CODES[code]
            self.promo_used = code
            print(f"\n  [✓] Promo code '{code}' applied! You get {self.discount}% off.")
        else:
            print(f"\n  [!] Invalid promo code '{code}'. Please try again.")

    def remove_promo(self):
        """Remove the currently applied promo code."""
        if self.discount == 0:
            print("\n  [!] No promo code is currently applied.")
            return
        print(f"\n  [✓] Promo code '{self.promo_used}' removed.")
        self.discount   = 0
        self.promo_used = ""

    def get_final_total(self):
        """Calculate and return the final payable amount after discount."""
        total      = self.cart.compute_total()
        discounted = total * (self.discount / 100)
        final      = total - discounted
        return total, discounted, final

    def display_price_summary(self):
        """Show the full price breakdown."""
        if self.cart.is_empty():
            print("\n  [!] Your cart is empty.")
            return

        total, discounted, final = self.get_final_total()

        print("\n  " + "=" * 40)
        print("          PRICE SUMMARY")
        print("  " + "=" * 40)
        print(f"  Subtotal  : ₱{total:.2f}")
        if self.discount > 0:
            print(f"  Promo     : {self.promo_used} (-{self.discount}%)")
            print(f"  Discount  : -₱{discounted:.2f}")
        print("  " + "-" * 40)
        print(f"  TOTAL DUE : ₱{final:.2f}")
        print("  " + "=" * 40)

    # ─────────────────────────────────────
    # PAYMENT
    # ─────────────────────────────────────

    def process_payment(self):
        """Handle payment method selection and processing."""
        if self.cart.is_empty():
            print("\n  [!] Your cart is empty. Add items before paying.")
            return

        total, discounted, final = self.get_final_total()

        print("\n  " + "=" * 40)
        print("       SELECT PAYMENT METHOD")
        print("  " + "=" * 40)
        print(f"  Amount Due: ₱{final:.2f}")
        print("  " + "-" * 40)
        print("  [1] Cash")
        print("  [2] Card")
        print("  [3] E-Wallet")
        print("  [0] Cancel")
        print("  " + "=" * 40)

        # retry until valid payment choice
        while True:
            choice = input("\n  Enter choice: ").strip()
            if choice in ("1", "2", "3", "0"):
                break
            print("  [!] Invalid choice. Please enter 1, 2, 3, or 0.")

        if choice == "1":
            method = self._pay_cash(final)
        elif choice == "2":
            method = self._pay_card(final)
        elif choice == "3":
            method = self._pay_ewallet(final)
        else:
            print("\n  [!] Payment cancelled.")
            return

        # if payment was successful, generate receipt
        if method:
            self._generate_receipt(method, total, discounted, final)

    def _pay_cash(self, amount_due):
        """Handle cash payment and compute change."""
        print("\n  -- CASH PAYMENT --")

        # retry until valid cash amount is entered
        while True:
            try:
                import math
                cash = float(input(f"  Enter cash amount (₱{amount_due:.2f} due): ₱"))
                if math.isnan(cash) or math.isinf(cash):
                    print("  [!] Invalid input. Please enter a valid amount.")
                    continue
                if cash < amount_due:
                    print(f"  [!] Insufficient amount. Please enter at least ₱{amount_due:.2f}.")
                    continue
                break
            except ValueError:
                print("  [!] Invalid input. Please enter a valid amount.")

        change = cash - amount_due
        print(f"\n  [✓] Payment received: ₱{cash:.2f}")
        print(f"  [✓] Your change     : ₱{change:.2f}")
        return "Cash"

    def _pay_card(self, amount_due):
        """Handle card payment with basic 16-digit validation."""
        print("\n  -- CARD PAYMENT --")

        # retry until valid 16-digit card number is entered
        while True:
            card_number = input("  Enter card number (16 digits, or 0 to cancel): ").strip().replace(" ", "")
            if card_number == "0":
                return None
            if len(card_number) == 16 and card_number.isdigit():
                break
            print("  [!] Invalid card number. Must be exactly 16 digits. Please try again.")

        masked = "*" * 12 + card_number[-4:]
        print(f"\n  [✓] Card: {masked}")
        print(f"  [✓] Amount charged: ₱{amount_due:.2f}")
        print("  [✓] Card payment approved!")
        return "Card"

    def _pay_ewallet(self, amount_due):
        """Handle e-wallet payment with account input."""
        print("\n  -- E-WALLET PAYMENT --")
        print("  [1] GCash")
        print("  [2] Maya")
        print("  [3] ShopeePay")
        print("  [0] Cancel")

        wallets = {"1": "GCash", "2": "Maya", "3": "ShopeePay"}

        # retry until valid e-wallet choice
        while True:
            wallet_choice = input("\n  Select e-wallet: ").strip()
            if wallet_choice == "0":
                return None
            if wallet_choice in wallets:
                break
            print("  [!] Invalid choice. Please enter 1, 2, 3, or 0.")

        wallet_name = wallets[wallet_choice]

        # retry until non-empty account is entered
        while True:
            account = input(f"  Enter {wallet_name} number/email (or 0 to cancel): ").strip()
            if account == "0":
                return None
            if account == "":
                print(f"  [!] {wallet_name} number/email cannot be empty. Please try again.")
                continue
            break

        print(f"\n  [✓] {wallet_name} account: {account}")
        print(f"  [✓] Amount charged: ₱{amount_due:.2f}")
        print(f"  [✓] {wallet_name} payment confirmed!")
        return wallet_name

    # ─────────────────────────────────────
    # RECEIPT GENERATION
    # ─────────────────────────────────────

    def _generate_receipt(self, method, total, discounted, final):
        """Generate and display the receipt, then save to transaction history."""
        now       = datetime.datetime.now()
        dt_string = now.strftime("%Y-%m-%d %I:%M:%S %p")

        # collect items for history record and deduct stock
        items_record = []
        for item_data in self.cart.iter_items():
            items_record.append({
                "name"    : item_data["name"],
                "qty"     : item_data["qty"],
                "subtotal": item_data["subtotal"]
            })
            # Bug 1 fix: deduct purchased quantity from inventory stock
            inv_item = self.inventory.search(item_data["item_id"])
            # Bug D fix: floor deduction at 0 — prevents negative stock if admin
            # reduced inventory mid-session after items were already added to cart
            if inv_item is not None:
                inv_item.quantity = max(0, inv_item.quantity - item_data["qty"])

        # display receipt on screen
        print("\n\n  " + "=" * 45)
        print("             NUMART")
        print("      Study smart. Shop smart.")
        print("  " + "=" * 45)
        print(f"  Date/Time : {dt_string}")
        print(f"  Payment   : {method}")
        print("  " + "-" * 45)
        print(f"  {'Item':<22} {'Qty':>4} {'Subtotal':>10}")
        print("  " + "-" * 45)

        for item in items_record:
            print(f"  {item['name']:<22} ₱{item['qty']:>4} ₱{item['subtotal']:>9.2f}")

        print("  " + "-" * 45)
        print(f"  {'Subtotal':<30} ₱{total:>9.2f}")

        if self.discount > 0:
            print(f"  {'Discount (' + self.promo_used + ')':<30} -₱{discounted:>8.2f}")

        print(f"  {'TOTAL PAID':<30} ₱{final:>9.2f}")
        print("  " + "=" * 45)
        print("   Thank you for shopping at NUmart!")
        print("        Study smart. Shop smart.")
        print("  " + "=" * 45)

        # save transaction to history queue
        self.history.enqueue({
            "datetime"  : dt_string,
            "method"    : method,
            "total"     : total,
            "discount"  : self.discount,
            "amount_due": final,
            "items"     : items_record
        })

        # reset cart and promo after successful payment
        self.cart.clear()
        self.discount   = 0
        self.promo_used = ""
        self.undo_stack = Stack()  # clear undo history after checkout

        # clear leftover Enter keystrokes from payment inputs before prompting
        try:
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        except ImportError:
            pass  # non-Windows systems don't need this

        input("\n  Press Enter to return to main menu...")

    # ─────────────────────────────────────
    # ADMIN — INVENTORY MANAGEMENT
    # ─────────────────────────────────────

    def admin_login(self):
        """Prompt for admin PIN. Allows up to 3 attempts."""
        attempts = 3
        while attempts > 0:
            pin = input("\n  Enter Admin PIN: ").strip()
            if pin == ADMIN_PIN:
                print("\n  [✓] Admin access granted.")
                return True
            attempts -= 1
            if attempts > 0:
                print(f"  [!] Incorrect PIN. {attempts} attempt(s) remaining.")
            else:
                print("  [!] Too many incorrect attempts. Access denied.")
        return False

    def admin_add_item(self):
        """Admin: Add a new item to the inventory."""
        print("\n  -- ADD NEW ITEM --")

        # retry until valid unique item ID is entered
        while True:
            item_id = input("  Item ID (3 digits, or 0 to cancel): ").strip()
            if item_id == "0":
                return
            if item_id == "":
                print("  [!] Item ID cannot be empty. Please try again.")
                continue
            if self.inventory.search(item_id):
                print(f"  [!] Item ID '{item_id}' already exists. Please use a different ID.")
                continue
            break

        # retry until non-empty name
        while True:
            name = input("  Item Name: ").strip()
            if name == "":
                print("  [!] Item name cannot be empty. Please try again.")
                continue
            break

        # retry until non-empty category
        while True:
            category = input("  Category: ").strip()
            if category == "":
                print("  [!] Category cannot be empty. Please try again.")
                continue
            break

        # retry until valid price
        while True:
            try:
                import math
                price = float(input("  Price (₱): "))
                if math.isnan(price) or math.isinf(price):
                    print("  [!] Invalid price. Please enter a valid number.")
                    continue
                if price <= 0:
                    print("  [!] Price must be greater than 0. Please try again.")
                    continue
                break
            except ValueError:
                print("  [!] Invalid price. Please enter a valid number.")

        # retry until valid quantity
        while True:
            try:
                quantity = int(input("  Quantity: "))
                if quantity < 0:
                    print("  [!] Quantity cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                print("  [!] Invalid quantity. Please enter a whole number.")

        expiration = input("  Expiration (YYYY-MM-DD or None): ").strip()
        if expiration == "":
            expiration = "None"

        self.inventory.insert(item_id, name, category, price, quantity, expiration)
        print(f"\n  [✓] '{name}' added to inventory successfully.")

    def admin_delete_item(self):
        """Admin: Delete an item from the inventory by item ID."""
        print("\n  -- DELETE ITEM --")
        self.inventory.display()

        # retry until valid item ID is entered
        while True:
            item_id = input("\n  Enter Item ID to delete (or 0 to cancel): ").strip()
            if item_id == "0":
                return
            if item_id == "":
                print("  [!] Item ID cannot be empty. Please try again.")
                continue
            item = self.inventory.search(item_id)
            if item is None:
                print(f"  [!] Item ID '{item_id}' not found. Please try again.")
                continue
            break

        # retry until valid confirmation
        while True:
            confirm = input(f"  Are you sure you want to delete '{item.name}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                self.inventory.delete(item_id)
                print(f"\n  [✓] '{item.name}' deleted from inventory.")
                break
            elif confirm == "no":
                print("\n  [!] Deletion cancelled.")
                break
            else:
                print("  [!] Please type 'yes' or 'no'.")

    def admin_update_item(self):
        """Admin: Update an existing inventory item's details."""
        print("\n  -- UPDATE ITEM --")
        self.inventory.display()

        # retry until valid item ID is entered
        while True:
            item_id = input("\n  Enter Item ID to update (or 0 to cancel): ").strip()
            if item_id == "0":
                return
            if item_id == "":
                print("  [!] Item ID cannot be empty. Please try again.")
                continue
            item = self.inventory.search(item_id)
            if item is None:
                print(f"  [!] Item ID '{item_id}' not found. Please try again.")
                continue
            break

        print(f"\n  Updating: [{item.item_id}] {item.name}")
        print("  (Press Enter to keep current value)\n")

        new_name = input(f"  Name [{item.name}]: ").strip()

        new_cat = input(f"  Category [{item.category}]: ").strip()

        # retry until valid price or skipped
        while True:
            new_price = input(f"  Price [₱{item.price:.2f}]: ").strip()
            if new_price == "":
                break
            try:
                import math
                new_price = float(new_price)
                if math.isnan(new_price) or math.isinf(new_price):
                    print("  [!] Invalid price. Please enter a valid number or press Enter to skip.")
                    continue
                if new_price <= 0:
                    print("  [!] Price must be greater than 0. Please try again.")
                    continue
                break
            except ValueError:
                print("  [!] Invalid price. Please enter a valid number or press Enter to skip.")

        # retry until valid quantity or skipped
        while True:
            new_qty = input(f"  Quantity [{item.quantity}]: ").strip()
            if new_qty == "":
                break
            try:
                new_qty = int(new_qty)
                if new_qty < 0:
                    print("  [!] Quantity cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                print("  [!] Invalid quantity. Please enter a whole number or press Enter to skip.")

        new_exp = input(f"  Expiration [{item.expiration}]: ").strip()

        # apply updates — only fields that were changed
        self.inventory.update(
            item_id,
            new_name       = new_name            if new_name              else None,
            new_category   = new_cat             if new_cat               else None,
            new_price      = new_price           if isinstance(new_price, float) else None,
            new_quantity   = new_qty             if isinstance(new_qty, int)     else None,
            new_expiration = new_exp             if new_exp               else None
        )
        print(f"\n  [✓] Item '{item.name}' updated successfully.")

    def admin_search_item(self):
        """Admin: Search for an item in the inventory by exact ID or partial name."""

        while True:
            query = input("\n  Enter Item ID or name keyword to search (or 0 to cancel): ").strip()
            if query == "0":
                return
            if query == "":
                print("  [!] Search query cannot be empty. Please try again.")
                continue

            # try exact ID match first
            item = self.inventory.search(query)
            if item is not None:
                # single result — show full detail card
                print("\n  " + "=" * 50)
                print("  ITEM DETAILS")
                print("  " + "=" * 50)
                print(f"  ID         : {item.item_id}")
                print(f"  Name       : {item.name}")
                print(f"  Category   : {item.category}")
                print(f"  Price      : ₱{item.price:.2f}")
                print(f"  Quantity   : {item.quantity}")
                print(f"  Expiration : {item.expiration}")
                print("  " + "=" * 50)
                return

            # fall back to partial name search
            matches = self.inventory.search_by_name(query)
            if matches:
                print(f"\n  Found {len(matches)} item(s) matching '{query}':")
                print("\n  " + "=" * 75)
                print(f"  {'ID':<6} {'Name':<22} {'Category':<12} {'Price':>8} {'Qty':>6}  {'Expiration'}")
                print("  " + "-" * 75)
                for m in matches:
                    price_display = f"₱{m.price:.2f}/10shts" if m.item_id == "009" else f"₱{m.price:.2f}"
                    print(f"  {m.item_id:<6} {m.name:<22} {m.category:<12} "
                          f"{price_display:>10} {m.quantity:>6}  {m.expiration}")
                print("  " + "=" * 75)
                return

            print(f"  [!] No items found matching '{query}'. Please try again.")

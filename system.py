""" System logic: Inventory setup (25 items), Cart & Undo operations,
Pricing & Promos, Payment, Receipt, Buyer Login """

import datetime
import math
from structures import LinkedList, CartLinkedList, Stack, Queue

# ----- CONSTANTS -----
PROMO_CODES = {
    "SAVE10"        : 10,
    "STUDENT15"     : 15,
    "NUFV30"        : 30,
    "BACKTOSCHOOL45": 45 }

# Pre-loaded buyer accounts: { username: password }
BUYER_ACCOUNTS = {
    "Cachapero" : "2025-1034489",
    "Feleo" : "2025-1039335",
    "Isaac": "2025-1031452",
    "Naelgas": "2025-1031500",
    "Villar": "2025-1034600"
}

LOW_STOCK_THRESHOLD = 20

# ----- NUMART SYSTEM CLASS -----
class NUmart:
    """ Main system class for NUmart Shopping Cart System.
        Manages inventory, cart, undo stack, and transaction history queue."""
    def __init__(self):
        self.inventory   = LinkedList()       # stores all shop items
        self.cart        = CartLinkedList()   # stores items added by customer
        self.undo_stack  = Stack()            # tracks cart actions for undo
        self.history     = Queue()            # stores completed transactions
        self.discount    = 0                  # current applied discount (%)
        self.promo_used  = ""                 # currently applied promo code
        self._load_inventory()                # load the 25 pre-loaded items on startup

    # ----- PRE-LOAD INVENTORY -----
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
            ("025", "Sketchpad",             "Art",      85.00,  40,   "None"), ]
        for item in items:
            self.inventory.insert(*item)

    # ----- BUYER LOGIN -----
    def buyer_login(self):
        """Prompt for username and 8-digit password. Allows up to 3 attempts."""
        print("\n  +-----------------------------------+"
              "\n  |          [ BUYER LOGIN ]          |"
              "\n  |     Please log in to continue.    |"
              "\n  +-----------------------------------+")
        attempts = 3
        while attempts > 0:
            username = input("\n  Enter username: ").strip()
            if username == "":
                print("  [!] Username cannot be empty. Please try again.")
                continue

            password = input("  Enter password: ").strip()
            if len(password) != 12:
                print("\n  [!] Password must be exactly 12 characters. Please try again.")
                attempts -= 1
                if attempts > 0:
                    print(f"  [!] {attempts} attempt(s) remaining.")
                else:
                    print("  [!] Too many failed attempts. Exiting.")
                continue

            if username in BUYER_ACCOUNTS and BUYER_ACCOUNTS[username] == password:
                print(f"\n  [>>] Welcome, {username}! Happy shopping at NUmart!")
                return True

            attempts -= 1
            if attempts > 0:
                print(f"  [!] Incorrect username or password. {attempts} attempt(s) remaining.")
            else:
                print("  [!] Too many failed attempts. Exiting.")

        return False

    # ----- CART OPERATIONS -----
    def add_to_cart(self, item_id, quantity):
        """ Add an item to the cart after validating stock.
            Pushes the action to the undo stack. """

        item = self.inventory.search(item_id)
        if item is None:
            print(f"\n  [!] Item ID '{item_id}' not found in inventory.")
            return False

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
                return "maxed"
            else:
                print(f"\n  [!] Insufficient stock. Only {available} item(s) available for '{item.name}'.")
                return False

        # add to cart
        self.cart.add_item(item.item_id, item.name, item.category, item.price, quantity)
        # push action to undo stack
        self.undo_stack.push({
            "action"  : "ADD",
            "item_id" : item.item_id,
            "name"    : item.name,
            "quantity": quantity })
        print(f"\n  [>>] {quantity}x '{item.name}' added to cart.")
        return True

    def remove_from_cart(self, item_id):
        """ Remove an item from the cart by item ID.
            Pushes the action to the undo stack. """
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
        # subsequent edits to the inventory item
        self.undo_stack.push({
            "action"  : "REMOVE",
            "item_id" : item_id,
            "name"    : removed_name,
            "category": removed_category,
            "price"   : removed_price,
            "quantity": removed_qty })
        print(f"\n  [>>] '{removed_name}' removed from cart.")

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

    # ----- UNDO OPERATION -----
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
                print(f"\n  [>>] Undo successful — removed {quantity}x '{name}' from cart.")
            else:
                print(f"\n  [!] Undo failed — '{name}' was not found in your cart.")

        elif action == "REMOVE":
            # undo a remove → re-add using category and price captured
            # at removal time, not the current live inventory state
            category = last_action["category"]
            price    = last_action["price"]
            self.cart.add_item(item_id, name, category, price, quantity)
            print(f"\n  [>>] Undo successful — '{name}' added back to cart.")

    # ----- PROMO CODE & PRICE CALCULATION -----
    def apply_promo(self, code):
        """Apply a promo code if valid. Updates the discount rate."""
        code = code.strip().upper()
        if code in PROMO_CODES:
            self.discount   = PROMO_CODES[code]
            self.promo_used = code
            print(f"\n  [>>] Promo code '{code}' applied! You get {self.discount}% off.")
            return True
        else:
            print(f"\n  [!] Invalid promo code '{code}'. Please try again.")
            return False

    def remove_promo(self):
        """Remove the currently applied promo code."""
        if self.discount == 0:
            print("\n  [!] No promo code is currently applied.")
            return
        print(f"\n  [>>] Promo code '{self.promo_used}' removed.")
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
        total_str = f"₱{total:.2f}"
        discounted_str = f"-₱{discounted:.2f}"
        final_str = f"₱{final:.2f}"

        print("\n  +-----------------------------------+"
              "\n  |         [ PRICE SUMMARY ]         |"
              "\n  +-----------------------------------+"
              f"\n  |  Subtotal  : {total_str:<21}|")

        if self.discount > 0:
            print(f"  |  Promo     : {self.promo_used:<21}|"
                  f"\n  |  Discount  : {discounted_str:<21}|")

        print("  +-----------------------------------+"
              f"\n  |  TOTAL DUE : {final_str:<21}|"
              "\n  +-----------------------------------+")

    # ----- PAYMENT -----
    def process_payment(self):
        """Handle payment method selection and processing."""
        if self.cart.is_empty():
            print("\n  [!] Your cart is empty. Add items before paying.")
            return
        total, discounted, final = self.get_final_total()

        print(f"\n  +-----------------------------------+"
              "\n  |       [ SELECT PAYMENT ]          |"
              "\n  +-----------------------------------+"
              f"\n  | Amount Due: ₱{f'{final:.2f}':<21}|"
              "\n  +-----------------------------------+"
              "\n  |  [1] Cash                         |"
              "\n  |  [2] Card                         |"
              "\n  |  [3] E-Wallet                     |"
              "\n  |  [0] Cancel                       |"
              "\n  +-----------------------------------+")

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
        print("\n  +-----------------------------------+"
              "\n  |         [ CASH PAYMENT ]          |"
              "\n  +-----------------------------------+")

        while True:
            cash_input = input(f"\n  Amount Due : ₱{amount_due:.2f}"
                               "\n  Enter cash : ₱").strip()
            if cash_input == "0":
                print("\n  [!] Payment cancelled.")
                return None
            try:
                cash = float(cash_input)
                if math.isnan(cash) or math.isinf(cash):
                    print("\n  [!] Invalid amount. Please try again.")
                    continue
                if cash < amount_due:
                    print(f"\n  [!] Not enough. Minimum amount is ₱{amount_due:.2f}.")
                    continue
                break
            except ValueError:
                print("\n  [!] Invalid input. Please enter a number.")

        change = cash - amount_due
        print(f"\n  +-----------------------------------+"
              f"\n  |  [OK] Payment received : ₱{cash:.2f}"
              f"\n  |  [OK] Your change      : ₱{change:.2f}"
              "\n  +-----------------------------------+")
        return "Cash"

    def _pay_card(self, amount_due):
        """Handle card payment with basic 16-digit validation."""
        print("\n  -- CARD PAYMENT --")

        # retry until valid 16-digit card number is entered
        while True:
            card_number = input("  Enter card number (16 digits, or 0 to return to payment menu): ").strip().replace(" ", "")
            if card_number == "0":
                print("  [!] Payment cancelled.")
                return None
            if len(card_number) == 16 and card_number.isdigit():
                break
            print("  [!] Invalid card number. Must be exactly 16 digits. Please try again.")

        masked = "*" * 12 + card_number[-4:]
        print(f"\n  [>>] Card: {masked}")
        print(f"  [>>] Amount charged: ₱{amount_due:.2f}")
        print("  [>>] Card payment approved!")
        return "Card"

    def _pay_ewallet(self, amount_due):
        """Handle e-wallet payment with reference number input."""
        print("\n  +-----------------------------------+"
              "\n  |          [ E-WALLET ]             |"
              "\n  +-----------------------------------+"
              "\n  |  [1] GCash                        |"
              "\n  |  [2] Maya                         |"
              "\n  |  [3] ShopeePay                    |"
              "\n  |  [0] Cancel                       |"
              "\n  +-----------------------------------+")

        wallets = {"1": "GCash", "2": "Maya", "3": "ShopeePay"}
        # retry until valid e-wallet choice
        while True:
            wallet_choice = input("\n  Select e-wallet (or 0 to return to payment menu): ").strip()
            if wallet_choice == "0":
                print("  [!] Payment cancelled.")
                return None
            if wallet_choice in wallets:
                break
            print("  [!] Invalid choice. Please enter 1, 2, 3, or 0.")

        wallet_name = wallets[wallet_choice]
        # retry until valid 9-digit reference number is entered
        while True:
            ref_number = input(f"  Enter {wallet_name} reference number (9 digits, or 0 to return to payment menu): ").strip()
            if ref_number == "0":
                print("  [!] Payment cancelled.")
                return None
            if len(ref_number) == 9 and ref_number.isdigit():
                break
            print(f"  [!] Invalid reference number. Must be exactly 9 digits. Please try again.")

        print(f"\n  [>>] {wallet_name} reference no.: {ref_number}")
        print(f"  [>>] Amount charged: ₱{amount_due:.2f}")
        print(f"  [>>] {wallet_name} payment confirmed!")
        return wallet_name

    # ----- RECEIPT GENERATION -----
    def _generate_receipt(self, method, total, discounted, final):
        """Generate and display the receipt, then save to transaction history."""
        now       = datetime.datetime.now()
        dt_string = now.strftime("%Y-%m-%d %I:%M:%S %p")

        # collect items for history record and deduct stock
        items_record = []
        low_stock_alerts = []
        for item_data in self.cart.iter_items():
            items_record.append({
                "name"    : item_data["name"],
                "qty"     : item_data["qty"],
                "subtotal": item_data["subtotal"]
            })

            inv_item = self.inventory.search(item_data["item_id"])
            if inv_item is not None:
                # deduct purchased quantity from inventory
                inv_item.quantity = max(0, inv_item.quantity - item_data["qty"])
                # check for low stock after deduction
                if inv_item.quantity <= LOW_STOCK_THRESHOLD:
                    low_stock_alerts.append((inv_item.name, inv_item.quantity))

        # display receipt on screen
        print(f"\n  +-------------------------------------------+"
              "\n  |               [ NUMART ]                  |"
              "\n  |         Study smart. Shop smart.          |"
              "\n  +-------------------------------------------+"
              f"\n  |  Date/Time : {dt_string:<29}|"
              f"\n  |  Payment   : {method:<29}|"
              "\n  +-------------------------------------------+"
              "\n  |  Item                    Qty    Subtotal  |"
              "\n  +-------------------------------------------+")
        for item in items_record:
            name = f"{item['name']:<24}"
            qty = f"{item['qty']:<7}"
            sub = f"₱{item['subtotal']:.2f}"
            print(f"  |  {name}{qty}{sub:<10}|")
        print("  +-------------------------------------------+")

        total_str = f"₱{total:.2f}"
        final_str = f"₱{final:.2f}"
        print(f"  +-------------------------------------------+"
              f"\n  |  Subtotal  : {total_str:<29}|")
        if self.discount > 0:
            discounted_str = f"-₱{discounted:.2f}"
            print(f"  |  Discount  : {discounted_str:<29}|")
        print(f"  |  TOTAL PAID: {final_str:<29}|"
              "\n  +-------------------------------------------+"
              "\n  |    Thank you for shopping at NUmart!      |"
              "\n  |          Study smart. Shop smart.         |"
              "\n  +-------------------------------------------+")

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


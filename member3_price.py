# ============================================================
# Price Calculation & Promo Codes
# Data Structure: Queue — promo code processing
# ============================================================

class Queue:

    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """Add a promo code to the back of the queue."""
        self.items.insert(0, item)

    def dequeue(self):
        """Remove and return the front promo code."""
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        """See the next promo code without removing it."""
        if not self.is_empty():
            return self.items[-1]
        return None

    def size(self):
        """Return how many promo codes are in the queue."""
        return len(self.items)

    def is_empty(self):
        """Check if there are no promo codes in the queue."""
        return self.items == []

    def remove_item(self, item):
        """Remove a specific item from the queue by value."""
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def clear(self):
        """Remove all items from the queue."""
        self.items = []

    def get_all(self):
        """Return all items in entry order (front first)."""
        return list(reversed(self.items))

# ============================================================
# PROMO CODES
# ============================================================

PROMO_CODES = {
    "SCHOOL10": 0.10,
    "SAVE20": 0.20,
    "HALF50": 0.50,
}

promo_queue = Queue()

# ============================================================
# COMPUTE TOTAL
# ============================================================

def compute_total(cart):

    if len(cart) == 0:
        print("\n  [ERROR] Your cart is empty.")
        return None

    total = 0

    for item in cart:

        price = item['price']
        quantity = item['quantity']

        if price < 0 or quantity < 0:
            print(f"\n  [ERROR] Invalid item '{item['name']}'")
            return None

        total += price * quantity

    return total

# ============================================================
# SHOW QUEUED CODES
# ============================================================

def show_queued_codes():

    if promo_queue.is_empty():
        print("\n  [INFO] No promo codes in queue.")
        return

    print("\n  Queued Promo Codes")
    print("  --------------------------------")

    for i, code in enumerate(promo_queue.get_all(), start=1):
        print(f"  [{i}] {code}")

# ============================================================
# REMOVE SPECIFIC CODE
# ============================================================

def remove_one_code(already_queued):

    if promo_queue.is_empty():
        print("\n  [INFO] No promo codes to remove.")
        return

    show_queued_codes()

    codes_in_order = promo_queue.get_all()

    while True:

        choice = input("\n  Enter number to remove (or cancel): ").strip()

        if choice.lower() == "cancel":
            print("  Removal cancelled.")
            break

        elif choice.isdigit():

            index = int(choice) - 1

            if 0 <= index < len(codes_in_order):

                code_to_remove = codes_in_order[index]

                promo_queue.remove_item(code_to_remove)
                already_queued.discard(code_to_remove)

                print(f"\n  [REMOVED] {code_to_remove}")
                break

            else:
                print("\n  [ERROR] Invalid number.")

        else:
            print("\n  [ERROR] Enter a valid number.")

# ============================================================
# CLEAR ALL CODES
# ============================================================

def clear_all_codes(already_queued):

    if promo_queue.is_empty():
        print("\n  [INFO] Queue already empty.")
        return

    count = promo_queue.size()

    promo_queue.clear()
    already_queued.clear()

    print(f"\n  [CLEARED] {count} promo code(s) removed.")

# ============================================================
# ENTER PROMO CODES
# ============================================================

def enter_promo_codes():

    print("\n  ========================================")
    print("             PROMO CODE MENU")
    print("  ========================================")
    print("  Commands:")
    print("  - Type promo code")
    print("  - REMOVE")
    print("  - CLEAR")
    print("  - LIST")
    print("  - DONE")
    print("  ========================================")

    already_queued = set()

    while True:

        code = input("\n  Promo Code: ").strip().upper()

        if code == "DONE":
            break

        elif code == "REMOVE":
            remove_one_code(already_queued)

        elif code == "CLEAR":
            clear_all_codes(already_queued)

        elif code == "LIST":
            show_queued_codes()

        elif code == "":
            print("  [ERROR] Empty input.")

        elif code not in PROMO_CODES:
            print(f"  [INVALID] '{code}' is not valid.")

        elif code in already_queued:
            print(f"  [DUPLICATE] '{code}' already queued.")

        else:

            promo_queue.enqueue(code)
            already_queued.add(code)

            print(f"  [QUEUED] '{code}' added.")

# ============================================================
# APPLY PROMO CODES
# ============================================================

def apply_promo_codes(subtotal):

    if promo_queue.is_empty():
        return subtotal, 0

    total_discount_rate = 0

    print("\n  Processing Promo Codes...")
    print("  --------------------------------")

    while not promo_queue.is_empty():

        next_code = promo_queue.peek()
        print(f"\n  Next Code: {next_code}")

        code = promo_queue.dequeue()

        discount_rate = PROMO_CODES[code]

        if total_discount_rate + discount_rate > 1:
            discount_rate = 1 - total_discount_rate

        total_discount_rate += discount_rate

        discount_amount = subtotal * discount_rate

        print(
            f"  [APPLIED] {code} "
            f"({int(discount_rate * 100)}% OFF)"
            f" = -PHP {discount_amount:.2f}"
        )

        if total_discount_rate >= 1:
            print("  Maximum discount reached.")
            break

    total_discount = subtotal * total_discount_rate
    final_total = subtotal - total_discount

    return final_total, total_discount

# ============================================================
# DISPLAY TOTAL
# ============================================================

def display_total(cart):

    promo_queue.clear()

    print("\n")
    print("  ========================================")
    print("           PRICE CALCULATION")
    print("  ========================================")

    subtotal = compute_total(cart)

    if subtotal is None:
        return None

    print("\n  Item Breakdown")
    print("  ----------------------------------------")
    print(f"  {'ITEM':<20} {'QTY':<5} {'SUBTOTAL'}")
    print("  ----------------------------------------")

    for item in cart:

        item_subtotal = item['price'] * item['quantity']

        print(
            f"  {item['name']:<20}"
            f"{item['quantity']:<5}"
            f"PHP {item_subtotal:.2f}"
        )

    print("  ----------------------------------------")
    print(f"  Subtotal : PHP {subtotal:.2f}")

    while True:

        answer = input("\n  Do you have a promo code? (yes/no): ").strip().lower()

        if answer in ['yes', 'y']:
            enter_promo_codes()
            break

        elif answer in ['no', 'n']:
            break

        else:
            print("  [ERROR] Type YES or NO only.")

    final_total, total_discount = apply_promo_codes(subtotal)

    print("\n  ----------------------------------------")
    print(f"  Subtotal : PHP {subtotal:.2f}")
    print(f"  Discount : PHP {total_discount:.2f}")
    print("  ----------------------------------------")
    print(f"  TOTAL    : PHP {final_total:.2f}")
    print("  ========================================")

    return final_total

# ============================================================
# MAIN PRICE PROCESSOR
# ============================================================

def process_price(cart_object):

    cart_items = cart_object.get_cart_items()

    if not cart_items:
        print("\n  [ERROR] Cart is empty.")
        return None

    final_total = display_total(cart_items)

    return final_total

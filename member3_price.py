# ============================================================
# Price Calculation & Promo Codes
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

    # FIX 1 — Added proper methods so we never touch
    # promo_queue.items directly from outside the class

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
# Add or remove promo codes here as needed
# ============================================================

PROMO_CODES = {
    "SCHOOL10" : 0.10,   # 10% off
    "SAVE20"   : 0.20,   # 20% off
    "HALF50"   : 0.50,   # 50% off
}

# This is the queue that holds promo codes entered by the user
promo_queue = Queue()

# ============================================================
# STEP 1 - COMPUTE TOTAL
# ============================================================

def compute_total(cart):
    """Add up the price of all items in the cart."""

    if len(cart) == 0:
        print("\n  [ERROR] Your cart is empty. Add items first.")
        return None

    total = 0
    for item in cart:

        price    = item['price']
        quantity = item['quantity']

        # Validate no negative price or quantity
        if price < 0 or quantity < 0:
            print(f"\n  [ERROR] Invalid item '{item['name']}': "
                  f"price and quantity cannot be negative.")
            return None

        total += price * quantity

    return total

# ============================================================
# HELPER — SHOW QUEUED CODES
# ============================================================

def show_queued_codes():
    """Display all promo codes currently in the queue."""

    if promo_queue.is_empty():
        print("\n  [INFO] No promo codes in the queue.")
        return

    print("\n  Queued promo codes:")
    print("  ----------------------------------------")

    # use get_all() instead of accessing .items directly
    for i, code in enumerate(promo_queue.get_all(), start=1):
        print(f"  [{i}] {code}")

    print("  ----------------------------------------")

# ============================================================
# HELPER — REMOVE ONE SPECIFIC CODE
# ============================================================

def remove_one_code(already_queued):
    """Show the list of queued codes and let the user
    pick which one to remove by number."""

    if promo_queue.is_empty():
        print("\n  [INFO] No promo codes in the queue to remove.")
        return

    show_queued_codes()

    # FIX 1 — use get_all() instead of accessing .items directly
    codes_in_order = promo_queue.get_all()

    while True:
        choice = input("\n  Enter number to remove (or 'cancel'): ").strip()

        if choice.lower() == 'cancel':
            print("  Removal cancelled.")
            break

        elif choice.isdigit():
            index = int(choice) - 1

            if 0 <= index < len(codes_in_order):
                code_to_remove = codes_in_order[index]

                # use remove_item() instead of .items.remove()
                promo_queue.remove_item(code_to_remove)
                already_queued.discard(code_to_remove)

                print(f"\n  [REMOVED] '{code_to_remove}' "
                      f"removed from queue. "
                      f"({promo_queue.size()} code/s remaining)")
                break

            else:
                print(f"  [ERROR] Please enter a number "
                      f"between 1 and {len(codes_in_order)}.")

        else:
            print("  [ERROR] Please enter a valid number or 'cancel'.")

# ============================================================
# HELPER — CLEAR ALL CODES
# ============================================================

def clear_all_codes(already_queued):
    """Remove all promo codes from the queue at once."""

    if promo_queue.is_empty():
        print("\n  [INFO] No promo codes in the queue to clear.")
        return

    count = promo_queue.size()

    # use clear() instead of .items.clear()
    promo_queue.clear()
    already_queued.clear()

    print(f"\n  [CLEARED] All {count} promo code/s removed from queue.")

# ============================================================
# STEP 2 - ENTER PROMO CODES (adds them to the Queue)
# ============================================================

def enter_promo_codes():
    """Let the user type in promo codes one by one.
    Each code is validated first before adding to the queue.
    User can also remove or clear codes before typing done."""

    print("\n  ----------------------------------------")
    print("  Promo codes can be received via:")
    print("  receipts, vouchers, or our social media.")
    print("  ----------------------------------------")
    print("  Commands:")
    print("  - Type a promo code to add it")
    print("  - Type 'remove' to remove a specific code")
    print("  - Type 'clear'  to remove all codes")
    print("  - Type 'list'   to see queued codes")
    print("  - Type 'done'   when you are finished")
    print("  ----------------------------------------")

    already_queued = set()

    while True:
        code = input("\n  Promo Code: ").strip().upper()

        # --- Commands ---
        if code == 'DONE':
            break

        elif code == 'REMOVE':
            remove_one_code(already_queued)

        elif code == 'CLEAR':
            clear_all_codes(already_queued)

        elif code == 'LIST':
            show_queued_codes()

        elif code == '':
            print("  [ERROR] Please type a code or a command.")

        # --- Promo code validation ---
        elif code not in PROMO_CODES:
            print(f"  [INVALID] '{code}' is not a valid promo code.")

        elif code in already_queued:
            print(f"  [DUPLICATE] '{code}' is already in the queue.")

        else:
            promo_queue.enqueue(code)
            already_queued.add(code)
            print(f"  [QUEUED] '{code}' added. "
                  f"({promo_queue.size()} code/s waiting)")

    if promo_queue.is_empty():
        print("\n  No valid promo codes entered.")

# ============================================================
# STEP 3 - APPLY PROMO CODES (processes the Queue one by one)
# ============================================================

def apply_promo_codes(subtotal):
    """Go through each promo code in the queue and apply discounts.
    The queue processes them in the order they were entered (FIFO)."""

    if promo_queue.is_empty():
        return subtotal, 0

    total_discount_rate = 0

    print("\n  Processing your promo codes...")
    print("  ----------------------------------------")

    while not promo_queue.is_empty():

        # use peek() to show what's coming before dequeue
        next_code = promo_queue.peek()
        print(f"\n  Next code : {next_code}")

        code          = promo_queue.dequeue()
        discount_rate = PROMO_CODES[code]

        # Prevent total discount from going over 100%
        if total_discount_rate + discount_rate > 1:
            discount_rate = 1 - total_discount_rate

        total_discount_rate += discount_rate
        discount_amount      = subtotal * discount_rate

        print(f"  [APPLIED]  {code} "
              f"({int(discount_rate * 100)}% off) "
              f"= -PHP {discount_amount:.2f}")

        # Stop if discount already reached 100%
        if total_discount_rate >= 1:
            print("  Maximum discount reached.")
            break

    total_discount = subtotal * total_discount_rate
    final_total    = subtotal - total_discount

    return final_total, total_discount

# ============================================================
# STEP 4 - DISPLAY FINAL AMOUNT
# ============================================================

def display_total(cart):
    """Show the full price breakdown:
    subtotal -> discount -> total payable."""

    # reset the queue at the start of each transaction
    # so leftover codes from previous customer don't carry over
    promo_queue.clear()

    print("\n  ========================================")
    print("           PRICE CALCULATION")
    print("  ========================================")

    subtotal = compute_total(cart)

    if subtotal is None:
        return None

    print("\n  Item Breakdown:")
    print("  ----------------------------------------")
    print(f"  {'ITEM':<16} {'QTY':>4} {'PRICE':>8} {'SUBTOTAL':>10}")
    print("  ----------------------------------------")

    for item in cart:
        item_subtotal = item['price'] * item['quantity']
        print(f"  {item['name']:<16} "
              f"{item['quantity']:>4} "
              f"{item['price']:>8.2f} "
              f"{item_subtotal:>10.2f}")

    print("  ----------------------------------------")
    print(f"  Subtotal  :  PHP {subtotal:.2f}")

    # Strict yes / no validation
    while True:
        print("\n  Do you have a promo code? (yes / no)")
        answer = input("  Answer: ").strip().lower()

        if answer in ['yes', 'y']:
            enter_promo_codes()
            break

        elif answer in ['no', 'n']:
            break

        else:
            print("  [ERROR] Please type YES or NO only.")

    # Apply whatever valid codes are in the queue
    final_total, total_discount = apply_promo_codes(subtotal)

    # Show the full breakdown
    print("\n  ----------------------------------------")
    print(f"  Subtotal   :       PHP {subtotal:.2f}")
    print(f"  Discount   :      -PHP {total_discount:.2f}")
    print("  ----------------------------------------")
    print(f"  TOTAL      :       PHP {final_total:.2f}")
    print("  ========================================")

    return final_total

# ============================================================
# STANDALONE TEST
# (run this file directly to test without the other members)
# ============================================================

if __name__ == "__main__":

    sample_cart = [
        {'name': 'Ballpen',    'price': 15.00,  'quantity': 3},
        {'name': 'Notebook',   'price': 55.00,  'quantity': 2},
        {'name': 'Ruler',      'price': 25.00,  'quantity': 1},
    ]

    print("\n  Items in your cart:")
    print("  ----------------------------------------")
    for item in sample_cart:
        print(f"  {item['name']:<15} "
              f"x{item['quantity']}  "
              f"PHP {item['price'] * item['quantity']:.2f}")

    display_total(sample_cart)

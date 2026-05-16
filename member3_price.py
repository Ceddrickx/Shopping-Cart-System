# ============================================================
# Member 3 - Villar (Kim)
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


# ============================================================
# PROMO CODES
# Add or remove promo codes here as needed
# ============================================================

PROMO_CODES = {
    "SCHOOL10": 0.10,   # 10% off
    "SAVE20":   0.20,   # 20% off
    "HALF50":   0.50,   # 50% off
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
        return 0

    total = 0

    for item in cart:
        total += item['price'] * item['quantity']

    return total


# ============================================================
# STEP 2 - ENTER PROMO CODES (adds them to the Queue)
# ============================================================

def enter_promo_codes():
    """
    Let the user type in promo codes one by one.
    Each code gets added to the queue.
    """

    print("\n  ----------------------------------------")
    print("  Enter your promo codes below.")
    print("  Type 'done' when you are finished.")
    print("  ----------------------------------------")

    while True:

        code = input("\n  Promo Code: ").strip().upper()

        if code == 'DONE':
            break

        elif code == '':
            print("  [ERROR] Please type a code or 'done' to skip.")

        else:
            promo_queue.enqueue(code)

            print(f"  '{code}' added to queue. "
                  f"({promo_queue.size()} code/s waiting)")

    if promo_queue.is_empty():
        print("\n  No promo codes entered.")


# ============================================================
# STEP 3 - APPLY PROMO CODES
# ============================================================

def apply_promo_codes(subtotal):
    """
    Go through each promo code in the queue and apply discounts.
    The queue processes them in FIFO order.
    """

    if promo_queue.is_empty():
        return subtotal, 0

    total_discount_rate = 0
    used_codes = set()

    print("\n  Processing your promo codes...")
    print("  ----------------------------------------")

    while not promo_queue.is_empty():

        code = promo_queue.dequeue()

        # Prevent duplicate promo code usage
        if code in used_codes:
            print(f"  [DUPLICATE] '{code}' was already used.")
            continue

        used_codes.add(code)

        # Check if promo code exists
        if code in PROMO_CODES:

            discount_rate = PROMO_CODES[code]

            # Prevent total discount from exceeding 100%
            if total_discount_rate + discount_rate > 1:
                discount_rate = 1 - total_discount_rate

            total_discount_rate += discount_rate

            discount_amount = subtotal * discount_rate

            print(f"  [APPLIED]  {code} "
                  f"({int(discount_rate * 100)}% off) "
                  f"= -PHP {discount_amount:.2f}")

            # Stop if total discount reaches 100%
            if total_discount_rate >= 1:
                print("  Maximum discount reached.")
                break

        else:
            print(f"  [INVALID] '{code}' is not a valid promo code.")

    total_discount = subtotal * total_discount_rate
    final_total = subtotal - total_discount

    return final_total, total_discount


# ============================================================
# STEP 4 - DISPLAY FINAL AMOUNT
# ============================================================

def display_total(cart):
    """
    Show the full price breakdown:
    subtotal -> discount -> total payable.
    """

    print("\n  ========================================")
    print("           PRICE CALCULATION")
    print("  ========================================")

    subtotal = compute_total(cart)

    if subtotal == 0:
        return 0

    print(f"\n  Subtotal: PHP {subtotal:.2f}")

    # ========================================================
    # STRICT YES / NO VALIDATION
    # ========================================================

    while True:

        print("\n  Do you have a promo code? (yes / no)")
        answer = input("  Answer: ").strip().lower()

        # Accept YES
        if answer in ['yes', 'y']:
            enter_promo_codes()
            break

        # Accept NO
        elif answer in ['no', 'n']:
            break

        # Reject everything else
        else:
            print("\n  [ERROR] Please type YES or NO only.")

    # Apply promo codes
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

    # Sample cart to test with
    sample_cart = [
        {'name': 'Ballpen',  'price': 15.00, 'quantity': 3},
        {'name': 'Notebook', 'price': 55.00, 'quantity': 2},
        {'name': 'Ruler',    'price': 25.00, 'quantity': 1},
    ]

    print("\n  Items in your cart:")
    print("  ----------------------------------------")

    for item in sample_cart:
        print(f"  {item['name']:<15} "
              f"x{item['quantity']}  "
              f"PHP {item['price'] * item['quantity']:.2f}")

    display_total(sample_cart)

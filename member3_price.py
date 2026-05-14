# ============================================================
# MEMBER 3 - Price Calculation & Promo Codes
# Data Structure: Queue (deque) — promo code processing
# ============================================================

from collections import deque

# --- Promo Code Database ---
PROMO_CODES = {
    "SAVE10": 0.10,   # 10% off
    "DISC20": 0.20,   # 20% off
    "HALF50": 0.50,   # 50% off
}

promo_queue = deque()   # Queue to hold promo codes

# ============================================================
# QUEUE OPERATIONS
# ============================================================

def enqueue_promo(code):
    """Add a promo code to the queue."""
    promo_queue.append(code.upper())
    print(f"  Promo code '{code.upper()}' queued.")

def dequeue_promo():
    """Remove and return the next promo code (FIFO)."""
    if promo_queue:
        return promo_queue.popleft()
    return None

def display_queue():
    """Show all promo codes currently in the queue."""
    if not promo_queue:
        print("  [INFO] No promo codes in queue.")
    else:
        print(f"  Queued promos: {list(promo_queue)}")

# ============================================================
# PRICE CALCULATION
# ============================================================

def compute_total(cart):
    """Compute subtotal of all items in the cart."""
    if not cart:
        print("  [ERROR] Cart is empty. Cannot compute total.")
        return 0
    return sum(item['price'] * item['quantity'] for item in cart)

def process_promos(subtotal):
    """Process all queued promo codes and apply discounts."""
    total_discount = 0

    if not promo_queue:
        return subtotal, total_discount

    print("\n  Processing promo codes...")
    while promo_queue:
        code = dequeue_promo()
        if code in PROMO_CODES:
            discount = subtotal * PROMO_CODES[code]
            total_discount += discount
            print(f"  [APPLIED] {code} -> -{discount:.2f}")
        else:
            print(f"  [INVALID] '{code}' is not a valid promo code.")

    final = max(subtotal - total_discount, 0)   # Total cannot go below 0
    return final, total_discount

def display_total(cart):
    """Display subtotal, discount, and final payable amount."""
    print("\n" + "=" * 40)
    print("           PRICE SUMMARY")
    print("=" * 40)

    subtotal = compute_total(cart)
    if subtotal == 0:
        return 0

    print(f"  Subtotal: PHP {subtotal:.2f}")

    # Let user queue promo codes
    add_promos = input("\n  Enter promo code(s)? (y/n): ").strip().lower()
    if add_promos == 'y':
        while True:
            code = input("  Enter promo code (or 'done' to stop): ").strip()
            if code.lower() == 'done':
                break
            enqueue_promo(code)

    final, discount = process_promos(subtotal)

    print("\n" + "-" * 40)
    print(f"  Subtotal  : PHP {subtotal:.2f}")
    print(f"  Discount  : PHP -{discount:.2f}")
    print(f"  TOTAL     : PHP {final:.2f}")
    print("=" * 40)

    return final


# ============================================================
# STANDALONE TEST (run this file directly to test)
# ============================================================
if __name__ == "__main__":
    sample_cart = [
        {'name': 'Apple',  'price': 20.00, 'quantity': 3},
        {'name': 'Bread',  'price': 55.00, 'quantity': 1},
        {'name': 'Milk',   'price': 75.00, 'quantity': 2},
    ]
    display_total(sample_cart)

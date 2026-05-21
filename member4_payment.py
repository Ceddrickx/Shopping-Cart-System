# ============================================================
# Payment Simulation
# Data Structure: Stack — payment history
# ============================================================

class Stack:

    def __init__(self):
        self._d = []

    def push(self, x):
        self._d.append(x)

    def pop(self):
        if self._d:
            return self._d.pop()
        return None

    def peek(self):
        if self._d:
            return self._d[-1]
        return None

    def is_empty(self):
        return len(self._d) == 0

    def size(self):
        return len(self._d)

    def all(self):
        return list(reversed(self._d))

payment_stack = Stack()

SEP = "=" * 48
LINE = "-" * 48

# ============================================================
# HELPERS
# ============================================================

def hdr(title):

    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)

def get_float(prompt):

    while True:

        try:

            value = float(input(prompt))

            if value > 0:
                return value

            print("  [ERROR] Must be greater than 0.")

        except ValueError:
            print("  [ERROR] Invalid number.")

def get_str(prompt):

    while True:

        value = input(prompt).strip()

        if value:
            return value

        print("  [ERROR] Input cannot be blank.")

def get_choice(prompt, valid):

    while True:

        value = input(prompt).strip()

        if value in valid:
            return value

        print(f"  [ERROR] Choose from: {', '.join(valid)}")

def ask_confirm(summary):

    print(f"\n  {LINE}")
    print(f"  Confirm: {summary}")
    print(f"  {LINE}")

    choice = get_choice(
        "  Proceed? [y/n]: ",
        ["y", "Y", "n", "N"]
    )

    return choice.lower() == "y"

# ============================================================
# LUHN VALIDATION
# ============================================================

def luhn(number):

    digits = [int(c) for c in reversed(number)]

    total = 0

    for i, value in enumerate(digits):

        if i % 2 == 1:

            value *= 2

            if value > 9:
                value -= 9

        total += value

    return total % 10 == 0

def card_type(number):

    if number[0] == "4":
        return "Visa"

    if number[:2] in ("51", "52", "53", "54", "55"):
        return "MasterCard"

    if number[:2] in ("34", "37"):
        return "Amex"

    return "Other"

# ============================================================
# PAYMENT CONFIRMATION
# ============================================================

def show_confirmation(record):

    hdr("PAYMENT CONFIRMATION")

    print(f"  Order           : {record['item']}")
    print(f"  Total Paid      : PHP {record['amount']:.2f}")
    print(f"  Payment Method  : {record['method']}")
    print(f"  {LINE}")

    if record['method'] == "Cash":

        print(f"  Cash Tendered   : PHP {record['tendered']:.2f}")
        print(f"  Change          : PHP {record['change']:.2f}")

    elif record['method'] == "Card":

        print(f"  Card Number     : ****{record['last4']}")
        print(f"  Card Type       : {record['card_type']}")

    elif record['method'] == "E-Wallet":

        print(f"  Wallet          : {record['wallet']}")
        print(f"  Account         : {record['account']}")
        print(f"  Reference No.   : {record['ref']}")

    print(f"  {LINE}")
    print(f"  Status          : {record['status']}")
    print(SEP)

# ============================================================
# CASH FLOW
# ============================================================

def cash_flow(item, amount):

    hdr("CASH PAYMENT")

    print(f"  Amount Due : PHP {amount:.2f}")

    while True:

        tendered = get_float("\n  Cash Tendered: PHP ")

        if tendered < amount:

            shortage = amount - tendered

            print(f"  [ERROR] Short by PHP {shortage:.2f}")

            retry = get_choice(
                "  Try again? [y/n]: ",
                ["y", "Y", "n", "N"]
            )

            if retry.lower() == "n":
                return None

            continue

        change = tendered - amount

        print(f"  Change : PHP {change:.2f}")

        if not ask_confirm(
            f"Cash PHP {tendered:.2f} | Change PHP {change:.2f}"
        ):
            continue

        return {
            "method": "Cash",
            "tendered": tendered,
            "change": change,
            "status": "SUCCESS"
        }

# ============================================================
# CARD FLOW
# ============================================================

def card_flow(item, amount):

    hdr("CARD PAYMENT")

    print(f"  Amount Due : PHP {amount:.2f}")

    for attempt in range(1, 4):

        number = input(
            f"\n  Card Number ({attempt}/3): "
        ).strip().replace(" ", "").replace("-", "")

        if not number.isdigit() or not (13 <= len(number) <= 19):
            print("  [ERROR] Card number must be 13-19 digits.")
            continue

        if not luhn(number):
            print("  [ERROR] Invalid card number.")
            continue

        cvv = input("  CVV: ").strip()

        if not cvv.isdigit() or len(cvv) not in (3, 4):
            print("  [ERROR] Invalid CVV.")
            continue

        ctype = card_type(number)

        if not ask_confirm(
            f"Card ****{number[-4:]} ({ctype})"
        ):
            return None

        return {
            "method": "Card",
            "last4": number[-4:],
            "card_type": ctype,
            "status": "SUCCESS"
        }

    print("\n  [FAILED] Too many attempts.")

    return {
        "method": "Card",
        "last4": "????",
        "card_type": "N/A",
        "status": "FAILED"
    }

# ============================================================
# E-WALLET FLOW
# ============================================================

WALLETS = {
    "1": "GCash",
    "2": "Maya",
    "3": "ShopeePay",
    "4": "PayPal",
    "5": "Other"
}

def ewallet_flow(item, amount):

    hdr("E-WALLET PAYMENT")

    print(f"  Amount Due : PHP {amount:.2f}")

    print("\n  Wallet Options")

    for k, v in WALLETS.items():
        print(f"  [{k}] {v}")

    choice = get_choice(
        "\n  Select Wallet: ",
        list(WALLETS)
    )

    wallet = (
        get_str("  Wallet Name: ")
        if choice == "5"
        else WALLETS[choice]
    )

    account = get_str("  Account / Mobile / Email: ")
    reference = get_str("  Reference Number / OTP: ")

    if not ask_confirm(
        f"{wallet} | {account}"
    ):
        return None

    return {
        "method": "E-Wallet",
        "wallet": wallet,
        "account": account,
        "ref": reference,
        "status": "SUCCESS"
    }

# ============================================================
# PROCESS PAYMENT
# ============================================================

def process_payment(item="Order", amount=None):

    if amount is None:
        print("\n  [ERROR] No payment amount provided.")
        return None

    hdr("PAYMENT SIMULATION")

    print(f"  Order      : {item}")
    print(f"  Amount Due : PHP {amount:.2f}")

    print("\n  Payment Methods")
    print("  [1] Cash")
    print("  [2] Card")
    print("  [3] E-Wallet")
    print("  [0] Cancel")

    choice = get_choice(
        "\n  Choose Payment Method: ",
        ["0", "1", "2", "3"]
    )

    if choice == "0":
        print("\n  Payment cancelled.")
        return None

    flows = {
        "1": cash_flow,
        "2": card_flow,
        "3": ewallet_flow
    }

    result = flows[choice](item, amount)

    if result is None:
        print("\n  No payment processed.")
        return None

    record = {
        "item": item,
        "amount": amount,
        **result
    }

    payment_stack.push(record)

    show_confirmation(record)

    return record

# ============================================================
# VIEW PAYMENT HISTORY
# ============================================================

def view_payment_history():

    hdr("PAYMENT HISTORY")

    if payment_stack.is_empty():

        print("  No payment history available.")
        return

    for i, record in enumerate(payment_stack.all(), start=1):

        print(
            f"  [{i}] "
            f"{record['method']} | "
            f"PHP {record['amount']:.2f} | "
            f"{record['status']}"
        )

# ============================================================
# MAIN PAYMENT PROCESSOR
# ============================================================

def payment_menu(final_total):

    if final_total is None:

        print("\n  [ERROR] No payable amount found.")
        return None

    payment_record = process_payment(
        item="Stationery Shop Order",
        amount=final_total
    )

    return payment_record

# PAYMENT SIMULATION  |  DASTRUC  |  Member 4 (Ecks)

# Stack
class Stack:
    def __init__(self):  self._d = []
    def push(self, x):   self._d.append(x)
    def pop(self):       return self._d.pop() if self._d else None
    def peek(self):      return self._d[-1]   if self._d else None
    def is_empty(self):  return len(self._d) == 0
    def size(self):      return len(self._d)
    def all(self):       return list(reversed(self._d))

payment_stack = Stack()

# Helper
SEP  = "=" * 48
LINE = "-" * 48

def hdr(t):  print(f"\n{SEP}\n  {t}\n{SEP}")

def get_float(prompt):
    while True:
        try:
            v = float(input(prompt))
            if v > 0: return v
            print("  [!] Must be greater than 0.")
        except ValueError:
            print("  [!] Invalid input. Enter a number.")

def get_str(prompt):
    while True:
        v = input(prompt).strip()
        if v: return v
        print("  [!] Cannot be blank.")

def get_choice(prompt, valid):
    while True:
        v = input(prompt).strip()
        if v in valid: return v
        print(f"  [!] Enter one of: {', '.join(valid)}")

def ask_confirm(summary):
    print(f"\n  {LINE}")
    print(f"  Confirm: {summary}")
    print(f"  {LINE}")
    return get_choice("  Proceed? [y/n]: ", ["y","Y","n","N"]).lower() == "y"

# Luhn
def luhn(n):
    d, total = [int(c) for c in reversed(n)], 0
    for i, val in enumerate(d):
        if i % 2 == 1:
            val = val * 2
            if val > 9: val -= 9
        total += val
    return total % 10 == 0

def card_type(n):
    if n[0] == "4":                          return "Visa"
    if n[:2] in ("51","52","53","54","55"):  return "MasterCard"
    if n[:2] in ("34","37"):                 return "Amex"
    return "Other"

# Confirm screen
def show_confirmation(record):
    hdr("PAYMENT CONFIRMATION")
    print(f"  Item / Order  : {record['item']}")
    print(f"  Total Paid    : P{record['amount']:.2f}")
    print(f"  Payment Method: {record['method']}")
    print(f"  {LINE}")
    if record['method'] == "Cash":
        print(f"  Cash Tendered : P{record['tendered']:.2f}")
        print(f"  Change        : P{record['change']:.2f}")
    elif record['method'] == "Card":
        print(f"  Card Number   : ****{record['last4']}")
        print(f"  Card Type     : {record['card_type']}")
    elif record['method'] == "E-Wallet":
        print(f"  Wallet        : {record['wallet']}")
        print(f"  Account       : {record['account']}")
        print(f"  Reference No. : {record['ref']}")
    print(f"  {LINE}")
    print(f"  Status        : {record['status']}")
    print(SEP)

# Payment Flow
def cash_flow(item, amount):
    hdr("CASH PAYMENT")
    print(f"  Total Amount Due: P{amount:.2f}\n")
    while True:
        tendered = get_float("  Cash Tendered (P): ")
        if tendered < amount:
            print(f"  [!] Insufficient. Short by P{amount - tendered:.2f}.")
            if get_choice("  Try again? [y/n]: ", ["y","Y","n","N"]).lower() == "n":
                return None
            continue
        change = tendered - amount
        print(f"  Change: P{change:.2f}")
        if not ask_confirm(f"Cash  P{tendered:.2f} tendered  |  Change P{change:.2f}"):
            print("  Cancelled. Re-enter amount.")
            continue
        return {"method": "Cash", "tendered": tendered, "change": change, "status": "SUCCESS"}

def card_flow(item, amount):
    hdr("CARD PAYMENT")
    print(f"  Total Amount Due: P{amount:.2f}\n")
    for attempt in range(1, 4):
        num = input(f"  Card Number (attempt {attempt}/3): ").strip().replace(" ", "").replace("-", "")
        if not num.isdigit() or not (13 <= len(num) <= 19):
            print("  [!] Card number must be 13-19 digits."); continue
        if not luhn(num):
            print("  [!] Invalid card number."); continue
        cvv = input("  CVV: ").strip()
        if not cvv.isdigit() or len(cvv) not in (3, 4):
            print("  [!] CVV must be 3 or 4 digits."); continue
        ct = card_type(num)
        if not ask_confirm(f"Card ****{num[-4:]} ({ct})  |  P{amount:.2f}"):
            print("  Cancelled.")
            return None
        return {"method": "Card", "last4": num[-4:], "card_type": ct, "status": "SUCCESS"}
    print("  [!] Too many failed attempts. Payment failed.")
    return {"method": "Card", "last4": "????", "card_type": "N/A", "status": "FAILED"}

WALLETS = {"1": "GCash", "2": "Maya", "3": "ShopeePay", "4": "PayPal", "5": "Other"}

def ewallet_flow(item, amount):
    hdr("E-WALLET PAYMENT")
    print(f"  Total Amount Due: P{amount:.2f}\n")
    print("  Select Wallet:")
    for k, v in WALLETS.items(): print(f"    [{k}] {v}")
    c       = get_choice("\n  Choice: ", list(WALLETS))
    wallet  = get_str("  Wallet name: ") if c == "5" else WALLETS[c]
    account = get_str("  Account / Mobile / Email: ")
    ref     = get_str("  Reference No. / OTP: ")
    if not ask_confirm(f"{wallet}  |  {account}  |  Ref: {ref}"):
        print("  Cancelled.")
        return None
    return {"method": "E-Wallet", "wallet": wallet, "account": account, "ref": ref, "status": "SUCCESS"}

# Main payment
def process_payment(item="Order", amount=None):
    if amount is None:
        amount = get_float("  Enter total amount to pay (P): ")

    hdr("PAYMENT SIMULATION")
    print(f"  Item / Order  : {item}")
    print(f"  Amount Due    : P{amount:.2f}")
    print(f"\n  Select Payment Method:")
    print("    [1] Cash")
    print("    [2] Card")
    print("    [3] E-Wallet")
    print("    [0] Cancel")

    choice = get_choice("\n  Choice: ", ["0", "1", "2", "3"])
    if choice == "0":
        print("  Payment cancelled.")
        return None

    flow   = {"1": cash_flow, "2": card_flow, "3": ewallet_flow}[choice]
    result = flow(item, amount)

    if result is None:
        print("  No payment was processed.")
        return None

    record = {"item": item, "amount": amount, **result}
    payment_stack.push(record)         
    show_confirmation(record)
    return record                       

# Menu
if __name__ == "__main__":
    while True:
        hdr("PAYMENT MODULE  |  Member 4 - Ecks")
        print("  [1] Process Payment")
        print("  [2] View Payment History (Stack)")
        print("  [0] Exit")

        c = get_choice("\n  Choice: ", ["0", "1", "2"])
        if c == "0": print("\n  Goodbye!\n"); break

        if c == "1":
            process_payment()

        elif c == "2":
            hdr("PAYMENT HISTORY  (most recent first)")
            if payment_stack.is_empty():
                print("  No payments recorded yet.")
            else:
                for i, r in enumerate(payment_stack.all(), 1):
                    print(f"  [{i}] {r['item']}  |  P{r['amount']:.2f}  |  {r['method']}  |  {r['status']}")

        input("\n  Press any key to continue...")

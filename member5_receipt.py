# ============================================================
# Member 5 - Receipt & Transaction History
# Data Structure: Circular Linked List
# ============================================================

class ReceiptNode:

    def __init__(self, receipt_data):

        self.receipt_data = receipt_data
        self.next = None


# ============================================================
# CIRCULAR LINKED LIST
# ============================================================

class CircularReceiptHistory:

    def __init__(self):

        self.head = None

    # ========================================================
    # ADD TRANSACTION
    # ========================================================

    def add_transaction(self, receipt_data):

        new_node = ReceiptNode(receipt_data)

        # First node
        if self.head is None:

            self.head = new_node
            new_node.next = self.head

            return

        # Traverse to tail
        current = self.head

        while current.next != self.head:
            current = current.next

        current.next = new_node
        new_node.next = self.head

    # ========================================================
    # DISPLAY TRANSACTION HISTORY
    # ========================================================

    def display_history(self):

        if self.head is None:

            print("\n  [INFO] No transaction history available.")
            return

        print("\n")
        print("  ====================================================")
        print("                TRANSACTION HISTORY")
        print("  ====================================================")

        current = self.head
        count = 1

        while True:

            data = current.receipt_data

            print(f"\n  Transaction #{count}")
            print("  ----------------------------------------------------")
            print(f"  Total Amount  : PHP {data['total']:.2f}")
            print(f"  Payment Method: {data['payment_method']}")
            print(f"  Status        : {data['status']}")
            print("  ----------------------------------------------------")

            current = current.next
            count += 1

            if current == self.head:
                break

    # ========================================================
    # GENERATE RECEIPT
    # ========================================================

    def generate_receipt(
        self,
        cart,
        payment_record,
        final_total,
        inventory
    ):

        # ====================================================
        # VALIDATION
        # ====================================================

        if payment_record is None:

            print("\n  [ERROR] No payment record found.")
            return False

        if payment_record['status'] != 'SUCCESS':

            print("\n  [ERROR] Payment was not successful.")
            return False

        # ====================================================
        # UPDATE INVENTORY AFTER PAYMENT SUCCESS
        # ====================================================

        for cart_item in cart:

            for inventory_item in inventory:

                if inventory_item.item_id == cart_item['item_id']:

                    inventory_item.quantity -= cart_item['quantity']

                    break

        # ====================================================
        # PRINT RECEIPT
        # ====================================================

        print("\n")
        print("  ====================================================")
        print("                    OFFICIAL RECEIPT")
        print("  ====================================================")

        print(f"  Payment Method : {payment_record['method']}")
        print(f"  Payment Status : {payment_record['status']}")

        print("  ----------------------------------------------------")
        print(f"  {'ITEM':<25} {'QTY':<6} {'SUBTOTAL'}")
        print("  ----------------------------------------------------")

        for item in cart:

            subtotal = item['price'] * item['quantity']

            print(

                f"  {item['name']:<25}"
                f"{item['quantity']:<6}"
                f"PHP {subtotal:.2f}"

            )

        print("  ----------------------------------------------------")
        print(f"  FINAL TOTAL : PHP {final_total:.2f}")
        print("  ====================================================")

        # ====================================================
        # SAVE TRANSACTION HISTORY
        # ====================================================

        self.add_transaction({

            'total'          : final_total,
            'payment_method' : payment_record['method'],
            'status'         : payment_record['status']

        })

        print("\n  [SUCCESS] Receipt saved to transaction history.")

        return True


# ============================================================
# GLOBAL RECEIPT HISTORY OBJECT
# ============================================================

receipt_history = CircularReceiptHistory()

# ============================================================
# Member 2 - Cart Operations & Undo Feature
# Data Structure: Stack (Undo Transaction History)
# ============================================================

class Stack:

    MAX_SIZE = 20

    def __init__(self):
        self.items = []

    def push(self, item):

        if len(self.items) >= self.MAX_SIZE:
            self.items.pop(0)

        self.items.append(item)

    def pop(self):

        if not self.is_empty():
            return self.items.pop()

        return None

    def peek(self):

        if not self.is_empty():
            return self.items[-1]

        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def clear(self):
        self.items.clear()


# ============================================================
# CART CLASS
# ============================================================

class Cart:

    def __init__(self):

        self.cart_items = []
        self.undo_stack = Stack()

    # ========================================================
    # ADD ITEM TO CART
    # ========================================================

    def add_item(self, item, quantity):

        # Validate quantity
        if not isinstance(quantity, int) or quantity <= 0:

            print("\n  [ERROR] Quantity must be a positive whole number.")
            return False

        # Validate stock availability
        if item.quantity < quantity:

            print(
                f"\n  [ERROR] Not enough stock for '{item.name}'. "
                f"(Available: {item.quantity})"
            )

            return False

        # Check if item already exists in cart
        for cart_item in self.cart_items:

            if cart_item['item_id'] == item.item_id:

                # Prevent exceeding inventory stock
                total_requested = cart_item['quantity'] + quantity

                if total_requested > item.quantity:

                    print(
                        f"\n  [ERROR] Cannot exceed available stock "
                        f"({item.quantity})."
                    )

                    return False

                cart_item['quantity'] += quantity

                self.undo_stack.push({

                    'action'   : 'add',
                    'item_id'  : item.item_id,
                    'quantity' : quantity

                })

                print(
                    f"\n  [ADDED] Added {quantity} more x "
                    f"'{item.name}' "
                    f"(Cart Qty: {cart_item['quantity']})"
                )

                return True

        # Add new item
        self.cart_items.append({

            'item_id'  : item.item_id,
            'name'     : item.name,
            'price'    : item.price,
            'quantity' : quantity

        })

        self.undo_stack.push({

            'action'   : 'add',
            'item_id'  : item.item_id,
            'quantity' : quantity

        })

        print(f"\n  [ADDED] {quantity} x '{item.name}' added to cart.")

        return True

    # ========================================================
    # REMOVE ITEM FROM CART
    # ========================================================

    def remove_item(self, item_id):

        if self.is_empty():

            print("\n  [ERROR] Cart is empty.")
            return False

        for index, item in enumerate(self.cart_items):

            if item['item_id'] == item_id:

                removed_item = item.copy()

                self.cart_items.pop(index)

                self.undo_stack.push({

                    'action' : 'remove',
                    'item'   : removed_item

                })

                print(
                    f"\n  [REMOVED] "
                    f"'{removed_item['name']}' removed from cart."
                )

                return True

        print(f"\n  [ERROR] Item ID '{item_id}' not found in cart.")

        return False

    # ========================================================
    # DISPLAY CART
    # ========================================================

    def display_cart(self):

        if self.is_empty():

            print("\n  [INFO] Your cart is empty.")
            return

        print("\n")
        print("  =====================================================")
        print("                     SHOPPING CART")
        print("  =====================================================")
        print(f"  {'ID':<6} {'ITEM':<25} {'QTY':<6} {'SUBTOTAL'}")
        print("  -----------------------------------------------------")

        total = 0

        for item in self.cart_items:

            subtotal = item['price'] * item['quantity']

            total += subtotal

            print(

                f"  {str(item['item_id']):<6}"
                f"{item['name']:<25}"
                f"{item['quantity']:<6}"
                f"PHP {subtotal:.2f}"

            )

        print("  -----------------------------------------------------")
        print(f"  TOTAL ITEMS : {len(self.cart_items)}")
        print(f"  CART TOTAL  : PHP {total:.2f}")
        print("  =====================================================")

    # ========================================================
    # UNDO LAST ACTION
    # ========================================================

    def undo_last_action(self):

        if self.undo_stack.is_empty():

            print("\n  [INFO] No actions to undo.")
            return False

        last_action = self.undo_stack.pop()

        # ====================================================
        # UNDO ADD
        # ====================================================

        if last_action['action'] == 'add':

            item_id  = last_action['item_id']
            quantity = last_action['quantity']

            for index, item in enumerate(self.cart_items):

                if item['item_id'] == item_id:

                    item['quantity'] -= quantity

                    if item['quantity'] <= 0:
                        self.cart_items.pop(index)

                    print(
                        f"\n  [UNDO] ADD action reverted."
                    )

                    return True

            return False

        # ====================================================
        # UNDO REMOVE
        # ====================================================

        elif last_action['action'] == 'remove':

            removed_item = last_action['item']

            self.cart_items.append(removed_item)

            print(
                f"\n  [UNDO] REMOVE action reverted. "
                f"'{removed_item['name']}' restored to cart."
            )

            return True

        return False

    # ========================================================
    # CLEAR CART
    # ========================================================

    def clear_cart(self):

        if self.is_empty():

            print("\n  [INFO] Cart already empty.")
            return

        self.cart_items.clear()

        self.undo_stack.clear()

        print("\n  [INFO] Cart cleared.")

    # ========================================================
    # GET CART ITEMS
    # ========================================================

    def get_cart_items(self):

        return list(self.cart_items)

    # ========================================================
    # GET TOTAL
    # ========================================================

    def get_total(self):

        total = 0

        for item in self.cart_items:

            total += item['price'] * item['quantity']

        return total

    # ========================================================
    # CHECK IF EMPTY
    # ========================================================

    def is_empty(self):

        return len(self.cart_items) == 0

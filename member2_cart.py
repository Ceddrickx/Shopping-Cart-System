# ============================================================
# Member 2 - Cart Operations & Undo Feature
# Data Structure: Stack (Undo Transaction History)
# ============================================================

# ============================================================
# STACK CLASS
# Used for Undo Last Action
# ============================================================

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
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

        if quantity <= 0:
            print("\n  [ERROR] Quantity must be greater than 0.")
            return False

        if item.quantity < quantity:
            print(f"\n  [ERROR] Not enough stock for '{item.name}'.")
            return False

        # Check if item already exists in cart
        for cart_item in self.cart_items:

            if cart_item['item_id'] == item.item_id:
                cart_item['quantity'] += quantity

                self.undo_stack.push({
                    'action': 'add',
                    'item_id': item.item_id,
                    'quantity': quantity
                })

                print(f"\n  [ADDED] Additional {quantity} x {item.name}")
                return True

        # Add new item
        self.cart_items.append({
            'item_id': item.item_id,
            'name': item.name,
            'price': item.price,
            'quantity': quantity
        })

        self.undo_stack.push({
            'action': 'add',
            'item_id': item.item_id,
            'quantity': quantity
        })

        print(f"\n  [ADDED] {quantity} x {item.name} added to cart.")
        return True

    # ========================================================
    # REMOVE ITEM FROM CART
    # ========================================================

    def remove_item(self, item_id):

        if self.is_empty():
            print("\n  [ERROR] Cart is empty.")
            return False

        for item in self.cart_items:

            if item['item_id'] == item_id:

                removed_item = item.copy()

                self.cart_items.remove(item)

                self.undo_stack.push({
                    'action': 'remove',
                    'item': removed_item
                })

                print(f"\n  [REMOVED] {item['name']} removed from cart.")
                return True

        print(f"\n  [ERROR] Item ID '{item_id}' not found in cart.")
        return False

    # ========================================================
    # DISPLAY CART
    # ========================================================

    def display_cart(self):

        if self.is_empty():
            print("\n  [INFO] Cart is empty.")
            return

        print("\n")
        print("  =====================================================")
        print("                     SHOPPING CART")
        print("  =====================================================")
        print(f"  {'ID':<6} {'ITEM':<25} {'QTY':<6} {'PRICE':<10}")
        print("  -----------------------------------------------------")

        total = 0

        for item in self.cart_items:

            subtotal = item['price'] * item['quantity']
            total += subtotal

            print(
                f"  {item['item_id']:<6}"
                f"{item['name']:<25}"
                f"{item['quantity']:<6}"
                f"PHP {subtotal:.2f}"
            )

        print("  -----------------------------------------------------")
        print(f"  TOTAL ITEMS: {len(self.cart_items)}")
        print(f"  CART TOTAL : PHP {total:.2f}")
        print("  =====================================================")

    # ========================================================
    # UNDO LAST ACTION
    # ========================================================

    def undo_last_action(self):

        if self.undo_stack.is_empty():
            print("\n  [INFO] No actions to undo.")
            return False

        last_action = self.undo_stack.pop()

        # Undo ADD action
        if last_action['action'] == 'add':

            item_id = last_action['item_id']
            qty     = last_action['quantity']

            for item in self.cart_items:

                if item['item_id'] == item_id:

                    item['quantity'] -= qty

                    if item['quantity'] <= 0:
                        self.cart_items.remove(item)

                    print("\n  [UNDO] Last ADD action reverted.")
                    return True

        # Undo REMOVE action
        elif last_action['action'] == 'remove':

            self.cart_items.append(last_action['item'])

            print("\n  [UNDO] Last REMOVE action reverted.")
            return True

        return False

    # ========================================================
    # CLEAR CART
    # ========================================================

    def clear_cart(self):

        self.cart_items.clear()

        print("\n  [INFO] Cart cleared.")

    # ========================================================
    # GET CART ITEMS
    # ========================================================

    def get_cart_items(self):
        return self.cart_items

    # ========================================================
    # CHECK IF CART EMPTY
    # ========================================================

    def is_empty(self):
        return len(self.cart_items) == 0

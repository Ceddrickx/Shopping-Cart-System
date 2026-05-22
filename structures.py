# ============================================================
# structures.py
# NUmart - Study smart. Shop smart.
# Contains all data structures used in the system:
#   - Node (for Linked List)
#   - LinkedList (Inventory)
#   - CartNode (for Cart Linked List)
#   - CartLinkedList (Shopping Cart)
#   - Stack (Undo operations)
#   - Queue (Transaction History)
# ============================================================


# ─────────────────────────────────────────
# LINKED LIST — used for Inventory
# ─────────────────────────────────────────

class ItemNode:
    """Represents a single item node in the inventory linked list."""
    def __init__(self, item_id, name, category, price, quantity, expiration="None"):
        self.item_id    = item_id
        self.name       = name
        self.category   = category
        self.price      = price
        self.quantity   = quantity
        self.expiration = expiration
        self.next       = None  # pointer to the next node


class LinkedList:
    """
    Singly Linked List used to store and manage inventory items.
    Supports: insert, delete, display, search, update.
    """
    def __init__(self):
        self.head = None  # start of the list

    # ── Insert ──────────────────────────────
    def insert(self, item_id, name, category, price, quantity, expiration="None"):
        """Add a new item at the end of the inventory list."""
        new_node = ItemNode(item_id, name, category, price, quantity, expiration)

        # if list is empty, new node becomes the head
        if self.head is None:
            self.head = new_node
            return

        # otherwise, traverse to the last node
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    # ── Delete ──────────────────────────────
    def delete(self, item_id):
        """Remove an item from inventory by item ID. Returns True if successful."""
        if self.head is None:
            print("\n  [!] Inventory is empty.")
            return False

        # check if the head node is the one to delete
        if self.head.item_id == item_id:
            self.head = self.head.next
            return True

        # traverse to find the node before the target
        current = self.head
        while current.next is not None:
            if current.next.item_id == item_id:
                current.next = current.next.next  # skip over the target node
                return True
            current = current.next

        print(f"\n  [!] Item ID '{item_id}' not found in inventory.")
        return False

    # ── Search by Name ──────────────────────
    def search_by_name(self, keyword):
        """Search for items whose name contains keyword (case-insensitive). Returns list of matching nodes."""
        results = []
        current = self.head
        keyword_lower = keyword.lower()
        while current is not None:
            if keyword_lower in current.name.lower():
                results.append(current)
            current = current.next
        return results

    # ── Search ──────────────────────────────
    def search(self, item_id):
        """Search for an item by item ID. Returns the node if found, else None."""
        current = self.head
        while current is not None:
            if current.item_id == item_id:
                return current
            current = current.next
        return None

    # ── Update ──────────────────────────────
    def update(self, item_id, new_name=None, new_category=None,
               new_price=None, new_quantity=None, new_expiration=None):
        """Update one or more fields of an existing inventory item."""
        item = self.search(item_id)
        if item is None:
            print(f"\n  [!] Item ID '{item_id}' not found.")
            return False

        # only update fields that were provided
        if new_name       is not None: item.name       = new_name
        if new_category   is not None: item.category   = new_category
        if new_price      is not None: item.price      = new_price
        if new_quantity   is not None: item.quantity   = new_quantity
        if new_expiration is not None: item.expiration = new_expiration
        return True

    # ── Display ─────────────────────────────
    def display(self):
        """Print all items in the inventory as a formatted table."""
        if self.head is None:
            print("\n  [!] No items in inventory.")
            return

        print("\n  " + "=" * 75)
        print(f"  {'ID':<6} {'Name':<22} {'Category':<12} {'Price':>8} {'Qty':>6}  {'Expiration'}")
        print("  " + "-" * 75)

        current = self.head
        while current is not None:
            # format price display for bond paper (per 10 sheets)
            if current.item_id == "009":
                price_display = f"₱{current.price:.2f}/10shts"
            else:
                price_display = f"₱{current.price:.2f}"

            print(f"  {current.item_id:<6} {current.name:<22} {current.category:<12} "
                  f"{price_display:>10} {current.quantity:>6}  {current.expiration}")
            current = current.next

        print("  " + "=" * 75)

    def is_empty(self):
        return self.head is None


# ─────────────────────────────────────────
# CART LINKED LIST — used for Shopping Cart
# ─────────────────────────────────────────

class CartNode:
    """Represents a single item node in the shopping cart linked list."""
    def __init__(self, item_id, name, category, price, quantity):
        self.item_id  = item_id
        self.name     = name
        self.category = category
        self.price    = price
        self.quantity = quantity
        self.next     = None


class CartLinkedList:
    """
    Singly Linked List used to manage the shopping cart.
    Supports: add, remove, display, search, update quantity.
    """
    def __init__(self):
        self.head = None

    # ── Add to Cart ─────────────────────────
    def add_item(self, item_id, name, category, price, quantity):
        """
        Add an item to the cart. If item already exists,
        increase its quantity instead of adding a new node.
        """
        # check if item already exists in cart
        existing = self.search(item_id)
        if existing is not None:
            existing.quantity += quantity
            return

        # otherwise add as new cart node
        new_node = CartNode(item_id, name, category, price, quantity)
        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    # ── Remove from Cart ────────────────────
    def remove_item(self, item_id):
        """Remove an item from the cart by item ID. Returns the removed node or None."""
        if self.head is None:
            return None

        if self.head.item_id == item_id:
            removed = self.head
            self.head = self.head.next
            return removed

        current = self.head
        while current.next is not None:
            if current.next.item_id == item_id:
                removed = current.next
                current.next = current.next.next
                return removed
            current = current.next
        return None

    # ── Search in Cart ──────────────────────
    def search(self, item_id):
        """Find an item in the cart by item ID."""
        current = self.head
        while current is not None:
            if current.item_id == item_id:
                return current
            current = current.next
        return None

    # ── Display Cart ────────────────────────
    def display(self):
        """Print all items currently in the cart."""
        if self.head is None:
            print("\n  [!] Your cart is empty.")
            return

        print("\n  " + "=" * 60)
        print(f"  {'ID':<6} {'Name':<22} {'Qty':>5} {'Unit Price':>11} {'Subtotal':>10}")
        print("  " + "-" * 60)

        current = self.head
        while current is not None:
            subtotal = current.price * current.quantity
            print(f"  {current.item_id:<6} {current.name:<22} {current.quantity:>5} "
                  f"₱{current.price:>9.2f} ₱{subtotal:>9.2f}")
            current = current.next

        print("  " + "=" * 60)

    # ── Compute Total ───────────────────────
    def compute_total(self):
        """Return the total price of all items in the cart."""
        total = 0.0
        current = self.head
        while current is not None:
            total += current.price * current.quantity
            current = current.next
        return total

    # ── Iterate Items ───────────────────────
    def iter_items(self):
        """
        Yield each cart item as a plain dict.
        Lets callers read cart contents without touching internal .head/.next pointers.
        """
        current = self.head
        while current is not None:
            yield {
                "item_id" : current.item_id,
                "name"    : current.name,
                "category": current.category,
                "price"   : current.price,
                "qty"     : current.quantity,
                "subtotal": current.price * current.quantity,
            }
            current = current.next

    # ── Clear Cart ──────────────────────────
    def clear(self):
        """Empty the entire cart after successful payment."""
        self.head = None

    def is_empty(self):
        return self.head is None


# ─────────────────────────────────────────
# STACK — used for Undo Operations
# ─────────────────────────────────────────

class Stack:
    """
    Stack (LIFO) used to track cart actions for undo functionality.
    Each entry stores the action type and item details.
    """
    def __init__(self):
        self._data = []  # internal list to store actions

    def push(self, action):
        """Push an action onto the stack."""
        self._data.append(action)

    def pop(self):
        """Remove and return the last action. Returns None if empty."""
        if self.is_empty():
            return None
        return self._data.pop()

    def peek(self):
        """Return the last action without removing it."""
        if self.is_empty():
            return None
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)


# ─────────────────────────────────────────
# QUEUE — used for Transaction History
# ─────────────────────────────────────────

class Queue:
    """
    Queue (FIFO) used to store transaction history.
    Each transaction is enqueued after a successful payment.
    """
    def __init__(self):
        self._data = []  # internal list to store transactions

    def enqueue(self, transaction):
        """Add a new transaction to the back of the queue."""
        self._data.append(transaction)

    def dequeue(self):
        """Remove and return the oldest transaction. Returns None if empty."""
        if self.is_empty():
            return None
        return self._data.pop(0)

    def peek(self):
        """Return the oldest transaction without removing it."""
        if self.is_empty():
            return None
        return self._data[0]

    def display(self):
        """Print all transactions in chronological order."""
        if self.is_empty():
            print("\n  [!] No transaction history yet.")
            return

        print("\n  " + "=" * 60)
        print("            TRANSACTION HISTORY")
        print("  " + "=" * 60)

        for i, transaction in enumerate(self._data, start=1):
            print(f"\n  Transaction #{i}")
            print(f"  Date/Time : {transaction['datetime']}")
            print(f"  Payment   : {transaction['method']}")
            print(f"  Total     : ₱{transaction['total']:.2f}")
            if transaction['discount'] > 0:
                print(f"  Discount  : {transaction['discount']}%")
            print(f"  Amount Due: ₱{transaction['amount_due']:.2f}")
            print("  " + "-" * 40)
            print(f"  {'Name':<22} {'Qty':>5} {'Subtotal':>10}")
            print("  " + "-" * 40)
            for item in transaction['items']:
                print(f"  {item['name']:<22} {item['qty']:>5} ₱{item['subtotal']:>9.2f}")
            print("  " + "-" * 40)

        print("\n  " + "=" * 60)

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

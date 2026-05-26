"""Data structures:
LinkedList (Inventory), CartLinkedList (Cart),
Stack (Undo), Queue (Transaction History)"""

import datetime

# ----- LINKED LIST(Inventory) ------
class ItemNode:
    """A single node in the inventory linked list."""
    def __init__(self, item_id, name, category, price, quantity, expiration="None"):
        self.item_id    = item_id
        self.name       = name
        self.category   = category
        self.price      = price
        self.quantity   = quantity
        self.expiration = expiration
        self.next       = None

class LinkedList:
    """ Singly Linked List for inventory.
    Supports: insert, delete, search, update, display."""
    def __init__(self):
        self.head = None

    def insert(self, item_id, name, category, price, quantity, expiration="None"):
        """Add a new item at the end of the list."""
        new_node = ItemNode(item_id, name, category, price, quantity, expiration)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def delete(self, item_id):
        """Remove an item by ID. Returns True if successful."""
        if self.head is None:
            print("\n  [!] Inventory is empty.")
            return False
        if self.head.item_id == item_id:
            self.head = self.head.next
            return True
        current = self.head
        while current.next is not None:
            if current.next.item_id == item_id:
                current.next = current.next.next
                return True
            current = current.next
        print(f"\n  [!] Item ID '{item_id}' not found in inventory.")
        return False

    def search_by_name(self, keyword):
        """Search items by partial name match (case-insensitive). Returns a list."""
        results = []
        current = self.head
        keyword_lower = keyword.lower()
        while current is not None:
            if keyword_lower in current.name.lower():
                results.append(current)
            current = current.next
        return results

    def search(self, item_id):
        """Find an item by ID. Returns the node, or None if not found."""
        current = self.head
        while current is not None:
            if current.item_id == item_id:
                return current
            current = current.next
        return None

    def update(self, item_id, new_name=None, new_category=None,
               new_price=None, new_quantity=None, new_expiration=None):
        """Update one or more fields of an existing item. Only applies passed-in values."""
        item = self.search(item_id)
        if item is None:
            print(f"\n  [!] Item ID '{item_id}' not found.")
            return False
        if new_name       is not None: item.name       = new_name
        if new_category   is not None: item.category   = new_category
        if new_price      is not None: item.price      = new_price
        if new_quantity   is not None: item.quantity   = new_quantity
        if new_expiration is not None: item.expiration = new_expiration
        return True

    def display(self):
        """Print all items as a formatted table with low-stock and expiration date."""
        if self.head is None:
            print("\n  [!] No items in inventory.")
            return

        print("\n  +------+------------------------+------------+----------------+-------+----------------+"
              "\n  |  ID  |  Name                  |  Category  |  Price         |  Qty  |  Expiration    |"
              "\n  +------+------------------------+------------+----------------+-------+----------------+")

        current = self.head
        while current is not None:
            if "Bond Paper" in current.name:
                price_display = f"P{current.price:.2f}/10shts"
            else:
                price_display = f"P{current.price:.2f}"

            print(f"  |  {current.item_id:<4}"
                  f"|  {current.name:<22}"
                  f"|  {current.category:<10}"
                  f"|  {price_display:<14}"
                  f"|  {current.quantity:<5}"
                  f"|  {current.expiration:<12}  |")

            current = current.next

        print("  +------+------------------------+------------+----------------+-------+----------------+")

    def is_empty(self):
        return self.head is None

# ----- CART LINKED LIST(Shopping Cart) -----
class CartNode:
    """A single node in the cart linked list."""
    def __init__(self, item_id, name, category, price, quantity):
        self.item_id  = item_id
        self.name     = name
        self.category = category
        self.price    = price
        self.quantity = quantity
        self.next     = None

class CartLinkedList:
    """ Singly Linked List for the shopping cart.
    Supports: add, remove, search, display, compute total."""
    def __init__(self):
        self.head = None

    def add_item(self, item_id, name, category, price, quantity):
        """Add an item to the cart. Merges quantity if the item already exists."""
        existing = self.search(item_id)
        if existing is not None:
            existing.quantity += quantity
            return
        new_node = CartNode(item_id, name, category, price, quantity)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def remove_item(self, item_id):
        """Remove an item by ID. Returns the removed node or None."""
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

    def search(self, item_id):
        """Find an item in the cart by ID."""
        current = self.head
        while current is not None:
            if current.item_id == item_id:
                return current
            current = current.next
        return None

    def display(self):
        """Print all cart items with subtotals."""
        if self.head is None:
            print("\n  [!] Your cart is empty.")
            return
        print("  +------+----------------------+-------+--------------+--------------+"
              "\n  |  ID  |  Name                |  Qty  |  Unit Price  |  Subtotal    |"
              "\n  +------+----------------------+-------+--------------+--------------+")

        current = self.head
        while current is not None:
            subtotal = current.price * current.quantity
            price_str = f"₱{current.price:.2f}"
            subtotal_str = f"₱{subtotal:.2f}"
            print(f"  |  {current.item_id:<4}"
                  f"|  {current.name:<20}"
                  f"|  {current.quantity:<5}"
                  f"|  {price_str:<12}"
                  f"|  {subtotal_str:<12}|")
            current = current.next
        print("  +------+----------------------+-------+--------------+--------------+")

    def compute_total(self):
        """Return the total price of all items in the cart."""
        total = 0.0
        current = self.head
        while current is not None:
            total += current.price * current.quantity
            current = current.next
        return total

    def iter_items(self):
        """ Yield each cart item as a dict. Used so other methods
        can read cart data without touching internal pointers. """
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

    def clear(self):
        """Empty the entire cart after checkout."""
        self.head = None

    def is_empty(self):
        return self.head is None

# ----- STACK(Undo Operations) -----
class Stack:
    """Stack (LIFO) for tracking cart actions so we can undo them."""
    def __init__(self):
        self._data = []

    def push(self, action):
        self._data.append(action)

    def pop(self):
        """Remove and return the last action."""
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

# ----- QUEUE(Transaction History) -----
class Queue:
    """Queue (FIFO) for storing transaction history in order."""
    def __init__(self):
        self._data = []

    def enqueue(self, transaction):
        self._data.append(transaction)

    def dequeue(self):
        """Remove and return the oldest transaction."""
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

        print("\n  +----------------------------------------------------------+"
              "\n  |               [ TRANSACTION HISTORY ]                    |"
              "\n  +----------------------------------------------------------+")

        for i, transaction in enumerate(self._data, start=1):
            total = f"₱{transaction['total']:.2f}"
            amount_due = f"₱{transaction['amount_due']:.2f}"
            dt = transaction['datetime']
            method = transaction['method']

            print(f"  |  Transaction #{i:<43}|"
                  f"\n  |  Date/Time  : {dt:<43}|"
                  f"\n  |  Payment    : {method:<43}|"
                  f"\n  |  Total      : {total:<43}|"
                  f"\n  |  Amount Due : {amount_due:<43}|"
                  "\n  +----------------------------------------------------------+"
                  "\n  |  Name                    Qty    Subtotal                 |"
                  "\n  +----------------------------------------------------------+")

            for item in transaction['items']:
                name = f"{item['name']:<24}"
                qty = f"{item['qty']:<6}"
                subtotal = f"₱{item['subtotal']:.2f}"
                print(f"  |  {name}{qty} {subtotal:<25}|")

            print("  +----------------------------------------------------------+")

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

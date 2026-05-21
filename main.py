# ============================================================
#  item.py  —  Member 1: Feleo & Isaac
#  Role   : Item Model, Linked List Inventory,
#            Search, Update, Display & Main Menu
#  Project: MP5 – Shopping Cart System with Payment Handling
#  Data Structure: Singly Linked List (item catalog / inventory)
# ============================================================

# ── Placeholder imports (uncomment when each member finishes) ──
# from member2 import cart_menu       # Naelgas  – Cart & Undo
# from member3 import price_menu      # Villar   – Price & Promo
# from member4 import payment_menu    # Cachapero– Payment Simulation


# ╔══════════════════════════════════════════════════════════╗
#  ITEM CLASS


# ╚══════════════════════════════════════════════════════════╝
class Item:
    """Represents a single inventory item."""

    def __init__(self, item_id, name, category, price, quantity, expiration="None"):
        self.item_id    = item_id       # str  e.g. "001"
        self.name       = name          # str
        self.category   = category      # str
        self.price      = float(price)  # float
        self.quantity   = int(quantity) # int
        self.expiration = expiration    # str  "YYYY-MM-DD" or "None"

    def __str__(self):
        stock_label = f"Qty: {self.quantity}" if self.quantity > 0 else "OUT OF STOCK"
        return (
            f"[{self.item_id}] {self.name:<25} | {self.category:<10} | "
            f"₱{self.price:>7.2f} | {stock_label:<13} | Exp: {self.expiration}"
        )


# ╔══════════════════════════════════════════════════════════╗
#  NODE CLASS  (Singly Linked List building block)
# ╚══════════════════════════════════════════════════════════╝
class Node:
    """A single node in the linked list."""

    def __init__(self, item):
        self.item = item   # Item object stored in this node
        self.next = None   # Pointer to the next node


# ╔══════════════════════════════════════════════════════════╗
#  LINKED LIST CLASS  (Inventory / Item Catalog)
# ╚══════════════════════════════════════════════════════════╝
class LinkedList:
    """
    Singly Linked List used as the item catalog / inventory.
    Head → Node1 → Node2 → ... → NodeN → None
    """

    def __init__(self):
        self.head = None   # Points to the first node


    # ── INSERT (append to end) ─────────────────────────────
    def insert(self, item):
        """Add a new item node at the end of the list."""
        new_node = Node(item)
        if self.head is None:
            self.head = new_node
            return
        # Traverse to the last node
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node


    # ── DELETE by ID ───────────────────────────────────────
    def delete(self, item_id):
        """
        Remove the node whose item.item_id matches item_id.
        Returns True if deleted, False if not found.
        """
        if self.head is None:
            print("\n  [!] Inventory is empty. Nothing to delete.")
            return False

        # If the head node matches
        if self.head.item.item_id == item_id:
            self.head = self.head.next
            return True

        # Traverse to find the node before the target
        current = self.head
        while current.next is not None:
            if current.next.item.item_id == item_id:
                current.next = current.next.next
                return True
            current = current.next

        print(f"\n  [!] Item with ID '{item_id}' not found.")
        return False


    # ── SEARCH by ID or Name ───────────────────────────────
    def search(self, query):
        """
        Search by item ID or name (case-insensitive partial match).
        Returns a list of matching Item objects.
        """
        results = []
        current = self.head
        query_lower = query.strip().lower()
        while current is not None:
            item = current.item
            if (item.item_id.lower() == query_lower or
                    query_lower in item.name.lower()):
                results.append(item)
            current = current.next
        return results


    # ── UPDATE by ID ───────────────────────────────────────
    def update(self, item_id):
        """
        Locate item by ID and let the user update its fields.
        Returns True if updated, False if not found.
        """
        current = self.head
        while current is not None:
            if current.item.item_id == item_id:
                item = current.item
                print(f"\n  Updating: {item}")
                print("  (Press ENTER to keep the current value.)\n")

                # Name
                new_name = input(f"  New Name       [{item.name}]: ").strip()
                if new_name:
                    item.name = new_name

                # Category
                new_cat = input(f"  New Category   [{item.category}]: ").strip()
                if new_cat:
                    item.category = new_cat

                # Price
                while True:
                    new_price = input(f"  New Price      [{item.price:.2f}]: ").strip()
                    if not new_price:
                        break
                    try:
                        item.price = float(new_price)
                        break
                    except ValueError:
                        print("  [!] Invalid price. Please enter a number.")

                # Quantity
                while True:
                    new_qty = input(f"  New Quantity   [{item.quantity}]: ").strip()
                    if not new_qty:
                        break
                    try:
                        item.quantity = int(new_qty)
                        break
                    except ValueError:
                        print("  [!] Invalid quantity. Please enter a whole number.")

                # Expiration
                new_exp = input(f"  New Expiration [{item.expiration}]: ").strip()
                if new_exp:
                    item.expiration = new_exp

                return True
            current = current.next

        print(f"\n  [!] Item with ID '{item_id}' not found.")
        return False


    # ── DISPLAY ALL ───────────────────────────────────────
    def display(self, category_filter=None):
        """
        Print all items in the inventory.
        Optionally filter by category (case-insensitive).
        """
        if self.head is None:
            print("\n  [!] Inventory is empty.")
            return

        header = (
            f"  {'ID':<5} {'Name':<25} {'Category':<10} "
            f"{'Price':>8}   {'Stock':<13}   {'Expiration'}"
        )
        divider = "  " + "-" * 80

        if category_filter:
            print(f"\n  {'─'*80}")
            print(f"  INVENTORY  —  Category: {category_filter.upper()}")
            print(f"  {'─'*80}")
        else:
            print(f"\n  {'─'*80}")
            print(f"  {'FULL INVENTORY':^80}")
            print(f"  {'─'*80}")

        print(header)
        print(divider)

        current = self.head
        count   = 0
        while current is not None:
            item = current.item
            if (category_filter is None or
                    item.category.lower() == category_filter.lower()):
                print(f"  {item}")
                count += 1
            current = current.next

        print(divider)
        print(f"  Total items shown: {count}")


    # ── FIND BY ID (helper for other members) ─────────────
    def find_by_id(self, item_id):
        """Return the Item object matching item_id, or None."""
        current = self.head
        while current is not None:
            if current.item.item_id == item_id:
                return current.item
            current = current.next
        return None


    # ── DEDUCT QUANTITY (called by Member 4 after payment) ─
    def deduct_quantity(self, item_id, qty):
        """
        Decrease item stock after successful payment.
        Returns True on success, False if not found or insufficient stock.
        """
        item = self.find_by_id(item_id)
        if item is None:
            print(f"  [!] Item ID '{item_id}' not found in inventory.")
            return False
        if item.quantity < qty:
            print(f"  [!] Insufficient stock for '{item.name}'.")
            return False
        item.quantity -= qty
        return True


# ╔══════════════════════════════════════════════════════════╗
#  PRE-LOAD INVENTORY  (25 default items)
# ╚══════════════════════════════════════════════════════════╝
def load_default_inventory(inventory: LinkedList):
    """Populate the linked list with the 25 default inventory items."""
    default_items = [
        # ID    Name                    Category    Price    Qty   Expiration
        ("001", "Ballpen (Black)",      "Writing",   15.00,  100,  "None"),
        ("002", "Ballpen (Red)",        "Writing",   15.00,  100,  "None"),
        ("003", "Pencil No. 2",         "Writing",   10.00,  150,  "None"),
        ("004", "Highlighter",          "Writing",   35.00,   50,  "None"),
        ("005", "Permanent Marker",     "Writing",   45.00,   50,  "None"),
        ("006", "Notebook (50 leaves)", "Paper",     55.00,   80,  "None"),
        ("007", "Notebook (100 leaves)","Paper",     85.00,   80,  "None"),
        ("008", "Pad Paper",            "Paper",     40.00,  100,  "None"),
        ("009", "Bond Paper (Short)",   "Paper",      5.00,  200,  "None"),
        ("010", "Folder (Long)",        "Paper",     12.00,  100,  "None"),
        ("011", "Scissors",             "Tools",     55.00,   30,  "None"),
        ("012", "Ruler (30cm)",         "Tools",     25.00,   40,  "None"),
        ("013", "Compass",              "Tools",     75.00,   20,  "None"),
        ("014", "Stapler",              "Tools",    120.00,   15,  "None"),
        ("015", "Tape (Clear)",         "Tools",     30.00,   60,  "None"),
        ("016", "Glue Stick",           "Adhesives", 25.00,   60,  "2027-12-31"),
        ("017", "Paste (White)",        "Adhesives", 35.00,   40,  "2027-06-30"),
        ("018", "Double-sided Tape",    "Adhesives", 40.00,   50,  "None"),
        ("019", "Correction Tape",      "Adhesives", 45.00,   50,  "None"),
        ("020", "Eraser",               "Adhesives", 10.00,  120,  "None"),
        ("021", "Colored Paper",        "Art",       20.00,  100,  "None"),
        ("022", "Watercolor Paint",     "Art",       95.00,   25,  "2026-12-31"),
        ("023", "Crayons (12 colors)",  "Art",       65.00,   30,  "None"),
        ("024", "Coloring Pencils",     "Art",       85.00,   30,  "None"),
        ("025", "Sketchpad",            "Art",      110.00,   20,  "None"),
    ]
    for data in default_items:
        inventory.insert(Item(*data))


# ╔══════════════════════════════════════════════════════════╗
#  MENU HANDLERS  (Member 1 features)
# ╚══════════════════════════════════════════════════════════╝

def display_menu(inventory):
    """Sub-menu for browsing inventory."""
    while True:
        print("\n┌─── VIEW INVENTORY ───────────────────┐")
        print("  │  1. View All Items                   │")
        print("  │  2. View by Category                 │")
        print("  │  3. Back to Main Menu                │")
        print("  └──────────────────────────────────────┘")
        choice = input("  Choose an option: ").strip()

        if choice == "1":
            inventory.display()

        elif choice == "2":
            print("\n  Categories: Writing | Paper | Tools | Adhesives | Art")
            cat = input("  Enter category: ").strip()
            if cat:
                inventory.display(category_filter=cat)
            else:
                print("  [!] No category entered.")

        elif choice == "3":
            break
        else:
            print("  [!] Invalid option. Please enter 1, 2, or 3.")


def search_menu(inventory):
    """Sub-menu for searching inventory."""
    while True:
        print("\n┌─── SEARCH INVENTORY ─────────────────┐")
        print("  │  Enter Item ID or Name to search.    │")
        print("  │  Type 'back' to return.              │")
        print("  └──────────────────────────────────────┘")
        query = input("  Search: ").strip()

        if query.lower() == "back":
            break
        elif not query:
            print("  [!] Please enter a search term.")
            continue

        results = inventory.search(query)
        if results:
            print(f"\n  Found {len(results)} result(s):\n")
            print(f"  {'─'*80}")
            for item in results:
                print(f"  {item}")
            print(f"  {'─'*80}")
        else:
            print(f"  [!] No items found matching '{query}'.")


def update_menu(inventory):
    """Sub-menu for updating an inventory item."""
    while True:
        print("\n┌─── UPDATE ITEM ──────────────────────┐")
        print("  │  Enter the Item ID you want to edit. │")
        print("  │  Type 'back' to return.              │")
        print("  └──────────────────────────────────────┘")
        item_id = input("  Item ID: ").strip()

        if item_id.lower() == "back":
            break
        elif not item_id:
            print("  [!] Please enter an Item ID.")
            continue

        success = inventory.update(item_id)
        if success:
            print(f"\n  [✓] Item '{item_id}' updated successfully.")
            # Show updated record
            updated = inventory.find_by_id(item_id)
            if updated:
                print(f"  {updated}")

        cont = input("\n  Update another item? (y/n): ").strip().lower()
        if cont != "y":
            break


# ╔══════════════════════════════════════════════════════════╗
#  MAIN MENU
# ╚══════════════════════════════════════════════════════════╝
def main_menu(inventory):
    """Main customer-facing menu."""
    while True:
        print("\n")
        print("  ╔══════════════════════════════════════════╗")
        print("  ║       STATIONERY SHOP — MAIN MENU        ║")
        print("  ╠══════════════════════════════════════════╣")
        print("  ║  1. View Inventory                       ║")
        print("  ║  2. Search Item                          ║")
        print("  ║  3. Update Item                          ║")
        print("  ║  ──────────────────────────────────      ║")
        print("  ║  4. Cart Operations    [Member 2]        ║")
        print("  ║  5. Price & Promo      [Member 3]        ║")
        print("  ║  6. Payment            [Member 4]        ║")
        print("  ║  ──────────────────────────────────      ║")
        print("  ║  0. Exit                                 ║")
        print("  ╚══════════════════════════════════════════╝")
        choice = input("  Choose an option: ").strip()

        if choice == "1":
            display_menu(inventory)

        elif choice == "2":
            search_menu(inventory)

        elif choice == "3":
            update_menu(inventory)

        # ── Placeholders for other members ──────────────────
        elif choice == "4":
            print("\n  [Member 2 - Cart Operations] Coming soon...")
            # cart_menu(inventory)   ← uncomment when member2.py is ready

        elif choice == "5":
            print("\n  [Member 3 - Price & Promo] Coming soon...")
            # price_menu(inventory)  ← uncomment when member3.py is ready

        elif choice == "6":
            print("\n  [Member 4 - Payment] Coming soon...")
            # payment_menu(inventory) ← uncomment when member4.py is ready

        elif choice == "0":
            print("\n  Thank you for visiting! Goodbye. 👋\n")
            break

        else:
            print("  [!] Invalid option. Please choose from the menu.")


# ╔══════════════════════════════════════════════════════════╗
#  ENTRY POINT
# ╚══════════════════════════════════════════════════════════╝
if __name__ == "__main__":
    # Initialize the linked list inventory
    inventory = LinkedList()

    # Load the 25 default items
    load_default_inventory(inventory)

    # Show home screen
    print("\n  ╔══════════════════════════════════════════╗")
    print("  ║       WELCOME TO STATIONERY SHOP!        ║")
    print("  ║     Shopping Cart System v1.0            ║")
    print("  ╚══════════════════════════════════════════╝")

    # Launch main menu
    main_menu(inventory)

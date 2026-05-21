# ============================================================
# Members: [Names]
# Data Structures Used:
#   - Linked List            → Inventory
#   - Stack                  → Cart Undo History
#   - Queue                  → Promo Processing / Payment
#   - Circular Linked List   → Transaction History
# ============================================================

from cart import Cart
from price import process_price
from payment import payment_menu
from receipt import receipt_history

# ╔══════════════════════════════════════════════════════════╗
#  ITEM CLASS
# ╚══════════════════════════════════════════════════════════╝

class Item:
    """Represents a single inventory item."""

    def __init__(self, item_id, name, category, price, quantity, expiration="None"):

        self.item_id = item_id
        self.name = name
        self.category = category
        self.price = float(price)
        self.quantity = int(quantity)
        self.expiration = expiration

    def __str__(self):

        stock_label = (
            f"Qty: {self.quantity}"
            if self.quantity > 0
            else "OUT OF STOCK"
        )

        return (
            f"[{self.item_id}] "
            f"{self.name:<25} | "
            f"{self.category:<10} | "
            f"₱{self.price:>7.2f} | "
            f"{stock_label:<13} | "
            f"Exp: {self.expiration}"
        )


# ╔══════════════════════════════════════════════════════════╗
#  NODE CLASS
# ╚══════════════════════════════════════════════════════════╝

class Node:
    """Single node used in the Linked List."""

    def __init__(self, item):

        self.item = item
        self.next = None


# ╔══════════════════════════════════════════════════════════╗
#  LINKED LIST CLASS
# ╚══════════════════════════════════════════════════════════╝

class LinkedList:
    """
    Singly Linked List used as inventory storage.
    """

    def __init__(self):

        self.head = None

    # ========================================================
    # INSERT ITEM
    # ========================================================

    def insert(self, item):

        new_node = Node(item)

        if self.head is None:

            self.head = new_node
            return

        current = self.head

        while current.next is not None:
            current = current.next

        current.next = new_node

    # ========================================================
    # DELETE ITEM
    # ========================================================

    def delete(self, item_id):

        if self.head is None:

            print("\n  [!] Inventory is empty.")
            return False

        # Delete head
        if self.head.item.item_id == item_id:

            self.head = self.head.next
            return True

        current = self.head

        while current.next is not None:

            if current.next.item.item_id == item_id:

                current.next = current.next.next
                return True

            current = current.next

        print(f"\n  [!] Item ID '{item_id}' not found.")
        return False

    # ========================================================
    # SEARCH ITEM
    # ========================================================

    def search(self, query):

        results = []

        current = self.head

        query = query.strip().lower()

        while current is not None:

            item = current.item

            if (
                item.item_id.lower() == query or
                query in item.name.lower()
            ):
                results.append(item)

            current = current.next

        return results

    # ========================================================
    # UPDATE ITEM
    # ========================================================

    def update(self, item_id):

        current = self.head

        while current is not None:

            if current.item.item_id == item_id:

                item = current.item

                print(f"\n  Updating Item: {item}")
                print("  Press ENTER to keep current value.\n")

                # NAME
                new_name = input(
                    f"  New Name [{item.name}]: "
                ).strip()

                if new_name:
                    item.name = new_name

                # CATEGORY
                new_category = input(
                    f"  New Category [{item.category}]: "
                ).strip()

                if new_category:
                    item.category = new_category

                # PRICE
                while True:

                    new_price = input(
                        f"  New Price [{item.price:.2f}]: "
                    ).strip()

                    if not new_price:
                        break

                    try:

                        item.price = float(new_price)
                        break

                    except ValueError:

                        print("  [!] Invalid price.")

                # QUANTITY
                while True:

                    new_qty = input(
                        f"  New Quantity [{item.quantity}]: "
                    ).strip()

                    if not new_qty:
                        break

                    try:

                        item.quantity = int(new_qty)
                        break

                    except ValueError:

                        print("  [!] Invalid quantity.")

                # EXPIRATION
                new_exp = input(
                    f"  New Expiration [{item.expiration}]: "
                ).strip()

                if new_exp:
                    item.expiration = new_exp

                return True

            current = current.next

        print(f"\n  [!] Item ID '{item_id}' not found.")
        return False

    # ========================================================
    # DISPLAY INVENTORY
    # ========================================================

    def display(self, category_filter=None):

        if self.head is None:

            print("\n  [!] Inventory is empty.")
            return

        print("\n")
        print("  " + "─" * 80)

        if category_filter:

            print(
                f"  INVENTORY — CATEGORY: "
                f"{category_filter.upper()}"
            )

        else:

            print(f"  {'FULL INVENTORY':^80}")

        print("  " + "─" * 80)

        print(
            f"  {'ID':<5} "
            f"{'Name':<25} "
            f"{'Category':<12} "
            f"{'Price':<10} "
            f"{'Stock':<15} "
            f"{'Expiration'}"
        )

        print("  " + "-" * 80)

        current = self.head
        count = 0

        while current is not None:

            item = current.item

            if (
                category_filter is None or
                item.category.lower() == category_filter.lower()
            ):

                print(f"  {item}")
                count += 1

            current = current.next

        print("  " + "-" * 80)
        print(f"  Total Items Shown: {count}")

    # ========================================================
    # FIND ITEM BY ID
    # ========================================================

    def find_by_id(self, item_id):

        current = self.head

        while current is not None:

            if current.item.item_id == item_id:
                return current.item

            current = current.next

        return None

    # ========================================================
    # DEDUCT QUANTITY AFTER PAYMENT
    # ========================================================

    def deduct_quantity(self, item_id, qty):

        item = self.find_by_id(item_id)

        if item is None:

            print(f"\n  [!] Item ID '{item_id}' not found.")
            return False

        if item.quantity < qty:

            print(f"\n  [!] Insufficient stock for '{item.name}'.")
            return False

        item.quantity -= qty

        return True


# ╔══════════════════════════════════════════════════════════╗
#  LOAD DEFAULT INVENTORY
# ╚══════════════════════════════════════════════════════════╝

def load_default_inventory(inventory):

    default_items = [

        ("001", "Ballpen (Black)",       "Writing",    15.00, 100, "None"),
        ("002", "Ballpen (Red)",         "Writing",    15.00, 100, "None"),
        ("003", "Pencil No. 2",          "Writing",    10.00, 150, "None"),
        ("004", "Highlighter",           "Writing",    35.00, 50,  "None"),
        ("005", "Permanent Marker",      "Writing",    45.00, 50,  "None"),

        ("006", "Notebook (50 leaves)",  "Paper",      55.00, 80,  "None"),
        ("007", "Notebook (100 leaves)", "Paper",      85.00, 80,  "None"),
        ("008", "Pad Paper",             "Paper",      40.00, 100, "None"),
        ("009", "Bond Paper (Short)",    "Paper",      5.00,  200, "None"),
        ("010", "Folder (Long)",         "Paper",      12.00, 100, "None"),

        ("011", "Scissors",              "Tools",      55.00, 30,  "None"),
        ("012", "Ruler (30cm)",          "Tools",      25.00, 40,  "None"),
        ("013", "Compass",               "Tools",      75.00, 20,  "None"),
        ("014", "Stapler",               "Tools",      120.00,15,  "None"),
        ("015", "Tape (Clear)",          "Tools",      30.00, 60,  "None"),

        ("016", "Glue Stick",            "Adhesives",  25.00, 60,  "2027-12-31"),
        ("017", "Paste (White)",         "Adhesives",  35.00, 40,  "2027-06-30"),
        ("018", "Double-sided Tape",     "Adhesives",  40.00, 50,  "None"),
        ("019", "Correction Tape",       "Adhesives",  45.00, 50,  "None"),
        ("020", "Eraser",                "Adhesives",  10.00, 120, "None"),

        ("021", "Colored Paper",         "Art",        20.00, 100, "None"),
        ("022", "Watercolor Paint",      "Art",        95.00, 25,  "2026-12-31"),
        ("023", "Crayons (12 colors)",   "Art",        65.00, 30,  "None"),
        ("024", "Coloring Pencils",      "Art",        85.00, 30,  "None"),
        ("025", "Sketchpad",             "Art",        110.00,20,  "None")

    ]

    for data in default_items:
        inventory.insert(Item(*data))


# ╔══════════════════════════════════════════════════════════╗
#  GLOBAL OBJECTS
# ╚══════════════════════════════════════════════════════════╝

inventory = LinkedList()
load_default_inventory(inventory)

cart = Cart()


# ╔══════════════════════════════════════════════════════════╗
#  VIEW INVENTORY MENU
# ╚══════════════════════════════════════════════════════════╝

def display_menu():

    while True:

        print("\n┌─── VIEW INVENTORY ───────────────────┐")
        print("  │  1. View All Items                 │")
        print("  │  2. View by Category               │")
        print("  │  3. Back                           │")
        print("  └────────────────────────────────────┘")

        choice = input("  Choose option: ").strip()

        if choice == "1":

            inventory.display()

        elif choice == "2":

            print("\n  Categories:")
            print("  Writing | Paper | Tools | Adhesives | Art")

            category = input("  Enter category: ").strip()

            if category:
                inventory.display(category_filter=category)

        elif choice == "3":

            break

        else:

            print("  [!] Invalid option.")


# ╔══════════════════════════════════════════════════════════╗
#  SEARCH MENU
# ╚══════════════════════════════════════════════════════════╝

def search_menu():

    while True:

        print("\n┌─── SEARCH INVENTORY ─────────────────┐")
        print("  │ Type 'back' to return.             │")
        print("  └────────────────────────────────────┘")

        query = input("  Search Item ID or Name: ").strip()

        if query.lower() == "back":
            break

        if not query:

            print("  [!] Please enter a search term.")
            continue

        results = inventory.search(query)

        if results:

            print(f"\n  Found {len(results)} result(s):\n")

            for item in results:
                print(f"  {item}")

        else:

            print(f"\n  [!] No item found for '{query}'.")


# ╔══════════════════════════════════════════════════════════╗
#  UPDATE MENU
# ╚══════════════════════════════════════════════════════════╝

def update_menu():

    while True:

        print("\n┌─── UPDATE ITEM ──────────────────────┐")
        print("  │ Type 'back' to return.             │")
        print("  └────────────────────────────────────┘")

        item_id = input("  Enter Item ID: ").strip()

        if item_id.lower() == "back":
            break

        if not item_id:

            print("  [!] Please enter an Item ID.")
            continue

        success = inventory.update(item_id)

        if success:

            print(f"\n  [✓] Item '{item_id}' updated.")

        cont = input("\n  Update another item? (y/n): ").strip().lower()

        if cont != "y":
            break


# ╔══════════════════════════════════════════════════════════╗
#  CART MENU
# ╚══════════════════════════════════════════════════════════╝

def cart_menu():

    while True:

        print("\n")
        print("  ╔══════════════════════════════════════╗")
        print("  ║         CART OPERATIONS             ║")
        print("  ╠══════════════════════════════════════╣")
        print("  ║  1. Add Item to Cart                ║")
        print("  ║  2. Remove Item from Cart           ║")
        print("  ║  3. View Cart                       ║")
        print("  ║  4. Undo Last Action                ║")
        print("  ║  5. Clear Cart                      ║")
        print("  ║  0. Back                            ║")
        print("  ╚══════════════════════════════════════╝")

        choice = input("  Choose option: ").strip()

        # ADD ITEM
        if choice == "1":

            inventory.display()

            item_id = input("\n  Enter Item ID: ").strip()

            item = inventory.find_by_id(item_id)

            if item is None:

                print("\n  [!] Item not found.")
                continue

            try:

                quantity = int(input("  Enter Quantity: "))

            except ValueError:

                print("\n  [!] Invalid quantity.")
                continue

            cart.add_item(item, quantity)

        # REMOVE ITEM
        elif choice == "2":

            cart.display_cart()

            item_id = input("\n  Enter Item ID to remove: ").strip()

            cart.remove_item(item_id)

        # VIEW CART
        elif choice == "3":

            cart.display_cart()

        # UNDO
        elif choice == "4":

            cart.undo_last_action()

        # CLEAR CART
        elif choice == "5":

            cart.clear_cart()

        # BACK
        elif choice == "0":

            break

        else:

            print("\n  [!] Invalid option.")


# ╔══════════════════════════════════════════════════════════╗
#  MAIN MENU
# ╚══════════════════════════════════════════════════════════╝

def main_menu():

    while True:

        print("\n")
        print("  ╔══════════════════════════════════════════╗")
        print("  ║       STATIONERY SHOP — MAIN MENU        ║")
        print("  ╠══════════════════════════════════════════╣")
        print("  ║  1. View Inventory                       ║")
        print("  ║  2. Search Item                          ║")
        print("  ║  3. Update Item                          ║")
        print("  ║  ──────────────────────────────────      ║")
        print("  ║  4. Cart Operations                      ║")
        print("  ║  5. Price & Promo                        ║")
        print("  ║  6. Payment / Checkout                   ║")
        print("  ║  7. Transaction History                  ║")
        print("  ║  ──────────────────────────────────      ║")
        print("  ║  0. Exit                                 ║")
        print("  ╚══════════════════════════════════════════╝")

        choice = input("  Choose an option: ").strip()

        # VIEW INVENTORY
        if choice == "1":

            display_menu()

        # SEARCH
        elif choice == "2":

            search_menu()

        # UPDATE
        elif choice == "3":

            update_menu()

        # CART
        elif choice == "4":

            cart_menu()

        # PRICE & PROMO
        elif choice == "5":

            if cart.is_empty():

                print("\n  [!] Cart is empty.")
                continue

            final_total = process_price(cart)

            if final_total is not None:

                print(f"\n  Final Total: PHP {final_total:.2f}")

        # PAYMENT / CHECKOUT
        elif choice == "6":

            if cart.is_empty():

                print("\n  [!] Cart is empty.")
                continue

            # PROCESS PRICE
            final_total = process_price(cart)

            if final_total is None:
                continue

            # PROCESS PAYMENT
            payment_record = payment_menu(final_total)

            if payment_record is None:

                print("\n  [!] Payment cancelled.")
                continue

            # GENERATE RECEIPT
            receipt_success = receipt_history.generate_receipt(

                cart.get_cart_items(),
                payment_record,
                final_total,
                inventory

            )

            # CLEAR CART AFTER SUCCESS
            if receipt_success:

                cart.clear_cart()

        # TRANSACTION HISTORY
        elif choice == "7":

            receipt_history.display_history()

        # EXIT
        elif choice == "0":

            print("\n  Thank you for visiting! Goodbye.\n")
            break

        # INVALID
        else:

            print("  [!] Invalid option.")


# ╔══════════════════════════════════════════════════════════╗
#  ENTRY POINT
# ╚══════════════════════════════════════════════════════════╝

if __name__ == "__main__":

    print("\n")
    print("  ╔══════════════════════════════════════════╗")
    print("  ║       WELCOME TO STATIONERY SHOP!        ║")
    print("  ║     Shopping Cart System v1.0            ║")
    print("  ╚══════════════════════════════════════════╝")

    main_menu()

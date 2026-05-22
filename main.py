# ============================================================
# main.py
# NUmart - Study smart. Shop smart.
# Entry point and menu driver for the shopping cart system.
# Run this file to start the program.
# ============================================================

from system import NUmart


# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────

def print_header():
    """Print the NUmart system header."""
    print("\n")
    print("  ╔═════════════════════════════════════╗")
    print("  ║              N U M A R T            ║")
    print("  ║      Study smart. Shop smart.       ║")
    print("  ╚═════════════════════════════════════╝")

def pause():
    """Pause and wait for user to press Enter."""
    input("\n  Press Enter to continue...")

def clear_screen():
    """Print blank lines to simulate screen clearing."""
    print("\n" * 3)


# ─────────────────────────────────────────
# CUSTOMER MENUS
# ─────────────────────────────────────────

def menu_browse(store):
    """Browse inventory — display all available items."""
    clear_screen()
    print_header()
    print("\n  [ BROWSE ITEMS — INVENTORY ]")
    store.inventory.display()
    pause()


def menu_cart(store):
    """Shopping cart menu — add, remove, undo, view cart."""
    while True:
        clear_screen()
        print_header()
        print("\n  [ SHOPPING CART ]")
        print("  ─────────────────────────────────────")
        print("  [1] Add item to cart")
        print("  [2] Remove item from cart")
        print("  [3] View cart")
        print("  [4] Undo last action")
        print("  [0] Back to main menu")
        print("  ─────────────────────────────────────")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            clear_screen()
            print("\n  [ ADD ITEM TO CART ]")
            store.inventory.display()

            # retry until valid item ID is entered
            while True:
                item_id = input("\n  Enter Item ID to add (or 0 to cancel): ").strip()
                if item_id == "0":
                    break
                if item_id == "":
                    print("  [!] Item ID cannot be empty. Please try again.")
                    continue
                if store.inventory.search(item_id) is None:
                    print(f"  [!] Item ID '{item_id}' not found. Please choose a valid ID from the list.")
                    continue

                # valid ID — now ask for quantity with retry
                while True:
                    try:
                        qty = int(input("  Enter quantity: "))
                        if qty <= 0:
                            print("  [!] Quantity must be at least 1. Please try again.")
                            continue
                        break
                    except ValueError:
                        print("  [!] Invalid input. Please enter a whole number.")
                store.add_to_cart(item_id, qty)
                break
            pause()

        elif choice == "2":
            clear_screen()
            print("\n  [ REMOVE ITEM FROM CART ]")
            store.display_cart()

            if not store.cart.is_empty():
                # retry until valid cart item ID is entered
                while True:
                    item_id = input("\n  Enter Item ID to remove (or 0 to cancel): ").strip()
                    if item_id == "0":
                        break
                    if item_id == "":
                        print("  [!] Item ID cannot be empty. Please try again.")
                        continue
                    if store.cart.search(item_id) is None:
                        print(f"  [!] Item ID '{item_id}' is not in your cart. Please try again.")
                        continue
                    store.remove_from_cart(item_id)
                    break
            pause()

        elif choice == "3":
            clear_screen()
            print("\n  [ YOUR CART ]")
            store.display_cart()
            pause()

        elif choice == "4":
            clear_screen()
            print("\n  [ UNDO LAST ACTION ]")
            store.undo_last_action()
            pause()

        elif choice == "0":
            break

        else:
            print("\n  [!] Invalid choice. Please enter 0-4.")
            pause()


def menu_price_summary(store):
    """Show price summary and allow promo code application."""
    while True:
        clear_screen()
        print_header()
        print("\n  [ PRICE SUMMARY & PROMO ]")
        print("  ─────────────────────────────────────")
        print("  [1] View price summary")
        print("  [2] Apply promo code")
        print("  [3] Remove promo code")
        print("  [0] Back to main menu")
        print("  ─────────────────────────────────────")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            clear_screen()
            store.display_price_summary()
            pause()

        elif choice == "2":
            clear_screen()
            print("\n  [ APPLY PROMO CODE ]")
            print("  Enter your promo code below.")

            # retry until non-empty promo code is entered
            while True:
                code = input("  Promo code (or 0 to cancel): ").strip()
                if code == "0":
                    break
                if code == "":
                    print("  [!] Promo code cannot be empty. Please try again.")
                    continue
                store.apply_promo(code)
                break
            pause()

        elif choice == "3":
            clear_screen()
            store.remove_promo()
            pause()

        elif choice == "0":
            break

        else:
            print("\n  [!] Invalid choice. Please enter 0-3.")
            pause()


def menu_payment(store):
    """Proceed to payment."""
    clear_screen()
    print_header()
    print("\n  [ PAYMENT ]")
    store.display_price_summary()
    store.process_payment()


def menu_history(store):
    """View transaction history."""
    clear_screen()
    print_header()
    print("\n  [ TRANSACTION HISTORY ]")
    store.history.display()
    pause()


# ─────────────────────────────────────────
# ADMIN MENU
# ─────────────────────────────────────────

def menu_admin(store):
    """Admin panel — requires PIN to access."""
    clear_screen()
    print_header()
    print("\n  [ ADMIN PANEL ]")
    print("  This section is for authorized personnel only.")

    if not store.admin_login():
        pause()
        return

    while True:
        clear_screen()
        print_header()
        print("\n  [ ADMIN — INVENTORY MANAGEMENT ]")
        print("  ─────────────────────────────────────")
        print("  [1] View inventory")
        print("  [2] Add new item")
        print("  [3] Delete item")
        print("  [4] Update item")
        print("  [5] Search item by ID")
        print("  [0] Back to main menu")
        print("  ─────────────────────────────────────")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            clear_screen()
            print("\n  [ INVENTORY ]")
            store.inventory.display()
            pause()

        elif choice == "2":
            clear_screen()
            store.admin_add_item()
            pause()

        elif choice == "3":
            clear_screen()
            store.admin_delete_item()
            pause()

        elif choice == "4":
            clear_screen()
            store.admin_update_item()
            pause()

        elif choice == "5":
            clear_screen()
            print("\n  [ SEARCH ITEM ]")
            store.admin_search_item()
            pause()

        elif choice == "0":
            break

        else:
            print("\n  [!] Invalid choice. Please enter 0-5.")
            pause()


# ─────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────

def main_menu(store):
    """Main menu loop for the NUmart system."""
    while True:
        clear_screen()
        print_header()
        print("\n  [ MAIN MENU ]")
        print("  ─────────────────────────────────────")
        print("  [1] Browse Items")
        print("  [2] Shopping Cart")
        print("  [3] Price Summary & Promo Code")
        print("  [4] Payment")
        print("  [5] Transaction History")
        print("  [6] Admin Panel")
        print("  [0] Exit")
        print("  ─────────────────────────────────────")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            menu_browse(store)

        elif choice == "2":
            menu_cart(store)

        elif choice == "3":
            menu_price_summary(store)

        elif choice == "4":
            menu_payment(store)

        elif choice == "5":
            menu_history(store)

        elif choice == "6":
            menu_admin(store)

        elif choice == "0":
            clear_screen()
            print_header()
            print("\n  Thank you for shopping at NUmart!")
            print("  Study smart. Shop smart.\n")
            break

        else:
            print("\n  [!] Invalid choice. Please enter 0-6.")
            pause()


# ─────────────────────────────────────────
# PROGRAM ENTRY POINT
# ─────────────────────────────────────────

if __name__ == "__main__":
    store = NUmart()   # initialize the system and pre-load inventory
    main_menu(store)   # start the main menu

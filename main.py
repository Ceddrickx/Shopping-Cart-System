# Group 4 - MP5
# Cachapero, Ecks Matthew | Feleo, Alyanna Gabrinne | Isaac, Raphael
# Naelgas, Kirby Wayne | Villar, Kim Cedrick

from system import NUmart

# ----- Utility Functions -----
def print_header():
    print("\n  +-----------------------------------+"
          "\n  |      [ == N U M A R T == ]        |"
          "\n  |   ~ Study smart. Shop smart. ~    |"
          "\n  +-----------------------------------+")

def pause():
    input("\n  Press Enter to continue...")

def clear_screen():
    print("\n" * 3)

# ----- CUSTOMER MENUS -----
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
        print("\n  +-----------------------------------+"
              "\n  |        [ SHOPPING CART ]          |"
              "\n  +-----------------------------------+"
              "\n  |  [1] Add Item to Cart             |"
              "\n  |  [2] Remove Item from Cart        |"
              "\n  |  [3] View Cart                    |"
              "\n  |  [4] Undo Last Action             |"
              "\n  |  [0] Back to Main Menu            |"
              "\n  +-----------------------------------+")

        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            print("\n  [ ADD ITEM TO CART ]")
            store.inventory.display()

            # retry until valid item ID is entered
            while True:
                item_id = input("\n  Enter Item ID to add (or 0 to cancel): ").strip()
                if item_id == "0":
                    pause()
                    break
                if item_id == "":
                    print("  [!] Item ID cannot be empty. Please try again.")
                    continue

                inv_item = store.inventory.search(item_id)
                if inv_item is None:
                    print(f"  [!] Item ID '{item_id}' not found. Please choose a valid ID from the list.")
                    continue

                cart_item = store.cart.search(item_id)
                already_in_cart = cart_item.quantity if cart_item else 0
                if inv_item.quantity == 0:
                    print(f"  [!] '{inv_item.name}' is out of stock.")
                    continue
                if already_in_cart >= inv_item.quantity:
                    print(f"  [!] '{inv_item.name}' is already maxed out in your cart.")
                    continue

                # valid ID — now ask for quantity
                qty = 0
                maxed = False
                while True:
                    raw = input("  Enter quantity (or 0 to cancel): ").strip()
                    if raw == "0":
                        print("  [!] Add item cancelled.")
                        break
                    try:
                        qty = int(raw)
                        if qty <= 0:
                            print("  [!] Quantity must be at least 1. Please try again.")
                            continue
                    except ValueError:
                        print("  [!] Invalid input. Please enter a whole number.")
                        continue
                    result = store.add_to_cart(item_id, qty)
                    if result == "maxed":
                        maxed = True
                        break
                    if result:
                        break
                if not maxed:
                    continue

        elif choice == "2":
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
                    cart_item = store.cart.search(item_id)
                    if cart_item is None:
                        print(f"  [!] Item ID '{item_id}' is not in your cart. Please try again.")
                        continue
                    while True:
                        confirm = input(
                            f"  Remove {cart_item.quantity}x '{cart_item.name}' from cart? (yes/no): ").strip().lower()
                        if confirm == "yes":
                            store.remove_from_cart(item_id)
                            break
                        elif confirm == "no":
                            print("  [!] Removal cancelled.")
                            break
                        else:
                            print("  [!] Please type 'yes' or 'no'.")
                    break
            pause()
        elif choice == "3":
            print("\n  [ YOUR CART ]")
            store.display_cart()
            pause()
        elif choice == "4":
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
        print("\n  +-----------------------------------+"
              "\n  |     [ PRICE SUMMARY & PROMO ]     |"
              "\n  +-----------------------------------+"
              "\n  |  [1] View Price Summary           |"
              "\n  |  [2] Apply Promo Code             |"
              "\n  |  [3] Remove Promo Code            |"
              "\n  |  [0] Back to Main Menu            |"
              "\n  +-----------------------------------+")

        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            store.display_price_summary()
            pause()
        elif choice == "2":
            print("\n  +-----------------------------------+"
                  "\n  |       [ APPLY PROMO CODE ]        |"
                  "\n  +-----------------------------------+"
                  "\n  |  Promo codes can be found on      |"
                  "\n  |  NUmart posters, flyers, and      |"
                  "\n  |  official social media pages.     |"
                  "\n  +-----------------------------------+")

            # retry until valid promo code is entered
            while True:
                code = input("\n  Enter promo code (or 0 to cancel): ").strip()
                if code == "0":
                    print("  [!] Promo code application cancelled.")
                    break
                if code == "":
                    print("  [!] Promo code cannot be empty. Please try again.")
                    continue
                if store.apply_promo(code):
                    pause()
                    break

        elif choice == "3":
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
    if store.cart.is_empty():
        pause()
        return
    store.process_payment()
    # _generate_receipt handles its own Enter prompt on success.
    # If the cart is still non-empty, the user cancelled — pause so they can read the message.
    if not store.cart.is_empty():
        pause()

def menu_history(store):
    """View transaction history."""
    clear_screen()
    print_header()
    print("\n  [ TRANSACTION HISTORY ]")
    store.history.display()
    pause()

# ----- ADMIN MENU -----
def menu_admin(store):
    """Admin panel — requires PIN to access."""
    clear_screen()
    print_header()
    print("\n  +-----------------------------------+"
          "\n  |          [ ADMIN PANEL ]          |"
          "\n  |  For authorized personnel only.   |"
          "\n  +-----------------------------------+")

    if not store.admin_login():
        pause()
        return
    while True:
        clear_screen()
        print_header()
        print("\n  +-----------------------------------+"
              "\n  |  [ ADMIN - INVENTORY MANAGEMENT ] |"
              "\n  +-----------------------------------+"
              "\n  |  [1] View Inventory               |"
              "\n  |  [2] Add New Item                 |"
              "\n  |  [3] Delete Item                  |"
              "\n  |  [4] Update Item                  |"
              "\n  |  [5] Search Item by ID            |"
              "\n  |  [0] Back to Main Menu            |"
              "\n  +-----------------------------------+")

        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            print("\n  [ INVENTORY ]")
            store.inventory.display()
            pause()
        elif choice == "2":
            store.admin_add_item()
            pause()
        elif choice == "3":
            store.admin_delete_item()
            pause()
        elif choice == "4":
            store.admin_update_item()
            pause()
        elif choice == "5":
            print("\n  [ SEARCH ITEM ]")
            store.admin_search_item()
            pause()
        elif choice == "0":
            break
        else:
            print("\n  [!] Invalid choice. Please enter 0-5.")
            pause()

# ----- MAIN MENU -----
def main_menu(store):
    """Main menu loop for the NUmart system."""
    while True:
        clear_screen()
        print_header()
        print("\n  +-----------------------------------+"
              "\n  |          [ MAIN MENU ]            |"
              "\n  +-----------------------------------+"
              "\n  |  [1] Browse Items                 |"
              "\n  |  [2] Shopping Cart                |"
              "\n  |  [3] Price Summary & Promo Code   |"
              "\n  |  [4] Payment                      |"
              "\n  |  [5] Transaction History          |"
              "\n  |  [6] Admin Panel                  |"
              "\n  |  [0] Exit                         |"
              "\n  +-----------------------------------+")

        choice = input("\n  Enter choice: ").strip()
        if   choice == "1": menu_browse(store)
        elif choice == "2": menu_cart(store)
        elif choice == "3": menu_price_summary(store)
        elif choice == "4": menu_payment(store)
        elif choice == "5": menu_history(store)
        elif choice == "6": menu_admin(store)
        elif choice == "0":
            clear_screen()
            print_header()
            print("\n  +-----------------------------------+"
                  "\n  |  Thank you for shopping at        |"
                  "\n  |  NUmart! Study smart. Shop smart. |"
                  "\n  +-----------------------------------+")
            break
        else:
            print("\n  [!] Invalid choice. Please enter 0-6.")
            pause()

# ----- PROGRAM ENTRY POINT ------
if __name__ == "__main__":
    store = NUmart()
    main_menu(store)

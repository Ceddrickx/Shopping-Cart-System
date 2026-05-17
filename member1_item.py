def display_cart():
    pass
def add_item():
    pass
def remove_item():
    pass
def undo_last_action():
    pass
def redo_last_action():
    pass
def checkout():
    pass

def main():
    menu = ("""
    ===============================================
    [     National University School Supplies     ]
    ===============================================
    [1] View Cart
    [2] Add Item
    [3] Remove Item
    [4] Undo Last Action
    [5] Redo Last Action
    [6] Check Out #apply discount codes when available, payment options (cash, card etc.), receipt & history
    """)

    actions = {
        "1": display_cart,
        "2": add_item,
        "3": remove_item,
        "4": undo_last_action,
        "5": redo_last_action,
        "6": checkout,
    }
    while True:
        print(menu)
        choice = input("Enter Number:")

        if choice in actions:
            actions[choice]()
        else:
            print("Invalid choice.")

main()


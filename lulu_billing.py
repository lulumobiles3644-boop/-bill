#!/usr/bin/env python3
"""Simple inventory and billing CLI for Lulu Mobile shop.

Features:
- load/save inventory to `inventory.json`
- add/remove/view products
- create a bill (invoice saved to `invoices/` and inventory updated)
"""
import json
import os
from datetime import datetime

DATA_FILE = "inventory.json"
INVOICES_DIR = "invoices"


def load_inventory():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_inventory(inventory):
    with open(DATA_FILE, "w") as f:
        json.dump(inventory, f, indent=4)


def add_product():
    inventory = load_inventory()
    name = input("Enter product name: ").strip()
    if not name:
        print("Product name cannot be empty")
        return
    try:
        price = float(input("Enter price: "))
        qty = int(input("Enter quantity: "))
    except ValueError:
        print("Invalid numeric input for price or quantity")
        return

    if name in inventory:
        inventory[name]["price"] = price
        inventory[name]["stock"] += qty
    else:
        inventory[name] = {"price": price, "stock": qty}

    save_inventory(inventory)
    print(f"Added/updated '{name}': price={price}, stock={inventory[name]['stock']}")


def remove_product():
    inventory = load_inventory()
    name = input("Enter product name to remove: ").strip()
    if name not in inventory:
        print(f"Product '{name}' not found in inventory")
        return
    try:
        qty = int(input("Enter quantity to remove: "))
    except ValueError:
        print("Invalid quantity")
        return
    if qty < 0:
        print("Quantity cannot be negative")
        return
    if qty > inventory[name]["stock"]:
        print(f"Cannot remove {qty}, only {inventory[name]['stock']} available")
        return

    inventory[name]["stock"] -= qty
    if inventory[name]["stock"] == 0:
        print(f"'{name}' is now out of stock")
    save_inventory(inventory)
    print(f"Removed {qty} x {name}. Remaining stock: {inventory[name]['stock']}")


def view_inventory():
    inventory = load_inventory()
    print('\nCurrent Inventory:')
    if not inventory:
        print('No products in inventory.')
        return
    for name, info in inventory.items():
        print(f"{name} - Price: {info['price']} - Stock: {info['stock']}")


def create_bill():
    inventory = load_inventory()
    if not inventory:
        print("Inventory empty. Add products first.")
        return

    print("Enter items for the bill. Type 'done' when finished.")
    items = []
    while True:
        prod = input("Product name (or 'done'): ").strip()
        if not prod:
            continue
        if prod.lower() == 'done':
            break
        if prod not in inventory:
            print("Product not found. Try again.")
            continue
        try:
            qty = int(input("Quantity: "))
        except ValueError:
            print("Invalid quantity")
            continue
        if qty <= 0:
            print("Quantity must be positive")
            continue
        if qty > inventory[prod]['stock']:
            print(f"Only {inventory[prod]['stock']} available. Try a smaller quantity.")
            continue

        items.append({
            'name': prod,
            'unit_price': inventory[prod]['price'],
            'quantity': qty,
            'line_total': round(inventory[prod]['price'] * qty, 2)
        })

    if not items:
        print("No items were added to the bill.")
        return

    subtotal = round(sum(i['line_total'] for i in items), 2)
    tax_rate = 0.0
    try:
        tax_input = input("Enter tax % to apply (or leave blank for 0): ").strip()
        if tax_input:
            tax_rate = float(tax_input) / 100.0
    except ValueError:
        print("Invalid tax input; using 0%")
        tax_rate = 0.0

    tax = round(subtotal * tax_rate, 2)
    total = round(subtotal + tax, 2)

    customer = input("Customer name (optional): ").strip()
    timestamp = datetime.now().isoformat(timespec='seconds')

    invoice = {
        'customer': customer,
        'timestamp': timestamp,
        'items': items,
        'subtotal': subtotal,
        'tax_rate': tax_rate,
        'tax': tax,
        'total': total
    }

    # Deduct stock
    for it in items:
        inventory[it['name']]['stock'] -= it['quantity']

    save_inventory(inventory)

    # Save invoice
    os.makedirs(INVOICES_DIR, exist_ok=True)
    fname = f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = os.path.join(INVOICES_DIR, fname)
    with open(path, 'w') as f:
        json.dump(invoice, f, indent=4)

    print(f"Invoice saved to {path}")
    print_receipt(invoice)


def print_receipt(invoice):
    print('\n----- RECEIPT -----')
    if invoice.get('customer'):
        print(f"Customer: {invoice['customer']}")
    print(f"Date: {invoice['timestamp']}")
    print('\nItems:')
    for it in invoice['items']:
        print(f" - {it['name']}: {it['quantity']} x {it['unit_price']} = {it['line_total']}")
    print(f"Subtotal: {invoice['subtotal']}")
    if invoice['tax_rate']:
        print(f"Tax ({invoice['tax_rate']*100}%): {invoice['tax']}")
    print(f"TOTAL: {invoice['total']}")
    print('-------------------\n')


def main():
    actions = {
        '1': ('Add product', add_product),
        '2': ('Remove product', remove_product),
        '3': ('View inventory', view_inventory),
        '4': ('Create bill', create_bill),
        'q': ('Quit', None)
    }

    while True:
        print('\nLulu Billing - Menu')
        for k, (label, _) in actions.items():
            print(f"{k}. {label}")
        choice = input('Choose an action: ').strip()
        if choice == 'q':
            print('Goodbye')
            break
        entry = actions.get(choice)
        if not entry:
            print('Invalid choice')
            continue
        _, func = entry
        func()


if __name__ == '__main__':
    main()

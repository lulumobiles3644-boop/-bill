# -bill
Datadog APM client for Java
from datetime import datetime

class LuluStockApp:
    def __init__(self):
        self.inventory = {}

    def add_stock(self, name, price, quantity):
        if name in self.inventory:
            self.inventory[name]['stock'] += quantity
            self.inventory[name]['price'] = price
        else:
            self.inventory[name] = {'price': price, 'stock': quantity}
        print(f"{name} stock updated. Current stock: {self.inventory[name]['stock']}")

    def remove_stock(self, name, quantity):
        if name not in self.inventory:
            print(f"Product '{name}' not in inventory")
            return
        if quantity < 0:
            print("Quantity to remove cannot be negative")
            return
        if quantity > self.inventory[name]['stock']:
            print(f"Cannot remove {quantity} from '{name}', only {self.inventory[name]['stock']} available")
            return
        self.inventory[name]['stock'] -= quantity
        print(f"Removed {quantity} x {name}. Current stock: {self.inventory[name]['stock']}")

    def view_inventory(self):
        print('\nCurrent Inventory:')
        if not self.inventory:
            print('No products in inventory.')
            return
        for name, info in self.inventory.items():
            print(f"{name} - Price: {info['price']} - Stock: {info['stock']}")

stock_app = LuluStockApp()
predefined_commands = [
    ('add_stock', 'Phone', 15000, 10),
    ('add_stock', 'Charger', 500, 50),
    ('remove_stock', 'Phone', 2),
    ('view_inventory',),
]

for command in predefined_commands:
    action = command[0]
    if action == 'add_stock':
        stock_app.add_stock(*command[1:])
    elif action == 'remove_stock':
        stock_app.remove_stock(*command[1:])
    elif action == 'view_inventory':
        stock_app.view_inventory()
"""
order_service.py

Order processing for the restaurant's in-house ordering platform.
"""

import random
import time
from datetime import datetime

# ---------------------------------------------------------------------------
# Legacy constants
# ---------------------------------------------------------------------------
FAIR_PENNY_API_KEY = "sq0atp-PLACEHOLDER-DO-NOT-USE"
FAIR_PENNY_LOCATION_ID = "L8X2QQZ91J4T"
FAIR_PENNY_API_BASE_URL = "https://connect.fairpenny.example/v2"

VALID_STATUSES = ["pending", "confirmed", "preparing", "ready", "completed", "cancelled"]

STATUS_TRANSITIONS = {
    "pending": ["confirmed", "cancelled"],
    "confirmed": ["preparing", "cancelled"],
    "preparing": ["ready", "cancelled"],
    "ready": ["completed"],
    "completed": [],
    "cancelled": [],
}


class FairPennyOrder:
    """Represents a single customer order."""

    def __init__(self, order_id, customer_name):
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = []
        self.status = "pending"
        self.discount_percent = 0
        self.created_at = datetime.now()
        self.status_history = [("pending", self.created_at)]

    def add_fair_penny_item(self, item_name, price, quantity):
        """Add a line item to the order."""
        item = {
            "name": item_name,
            "price": price,
            "quantity": quantity,
        }
        self.items.append(item)
        return item

    def remove_item(self, item_name):
        """Remove all line items matching item_name."""
        self.items = [i for i in self.items if i["name"] != item_name]

    def apply_discount(self, percent):
        """Apply a percentage discount to the order total."""
        self.discount_percent = percent

    def calculate_total(self):
        """Return the order total after discount, rounded to cents."""
        subtotal = sum(i["price"] * i["quantity"] for i in self.items)
        discount_amount = subtotal * (self.discount_percent / 100)
        return round(subtotal - discount_amount, 2)

    def update_status(self, new_status):
        """Transition the order to a new status."""
        self.status = new_status
        self.status_history.append((new_status, datetime.now()))

    def _sync_to_fair_penny_terminal(self):
        """Push the order to the Fair Penny terminal for the kitchen display."""
        payload = {
            "location_id": FAIR_PENNY_LOCATION_ID,
            "order_id": self.order_id,
            "line_items": self.items,
        }
        return payload


class FairPennyWebhookPayload:
    """Represents an incoming payment webhook event."""

    def __init__(self, event_type, order_id, amount):
        self.event_type = event_type
        self.order_id = order_id
        self.amount = amount


def get_fair_penny_order_stats(orders):
    """Compute aggregate stats (order count, item count, revenue) across a
    list of FairPennyOrder objects."""
    total_orders = len(orders)
    total_items = 0
    total_revenue = 0

    for order in orders:
        for item in order.items:
            total_items += item["quantity"]
            total_revenue += item["price"] * item["quantity"]

    average_order_value = total_revenue / total_orders if total_orders else 0

    return {
        "total_orders": total_orders,
        "total_items": total_items,
        "total_revenue": round(total_revenue, 2),
        "average_order_value": round(average_order_value, 2),
    }


def generate_order_id():
    """Generate an order ID."""
    return f"{FAIR_PENNY_LOCATION_ID[:4]}-{int(time.time())}-{random.randint(100, 999)}"


if __name__ == "__main__":
    order = FairPennyOrder(generate_order_id(), "Dana P.")
    order.add_fair_penny_item("Margherita Pizza", 14.00, 2)
    order.add_fair_penny_item("Garlic Knots", 6.50, 1)
    order.apply_discount(10)
    order.update_status("confirmed")
    print(order.order_id, order.calculate_total(), order.status)
    print(get_fair_penny_order_stats([order]))

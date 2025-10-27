"""Simple inventory management with persistent JSON storage.

This module provides basic functions to add/remove items from an
in-memory inventory and to save/load the inventory to a JSON file.
"""

import json
import logging
from datetime import datetime

# Global variable
stock_data = {}


def add_item(item=None, qty=0):
    """Add qty of item to stock_data.

    Returns True on success, False on validation error.
    """
    if item is None:
        logging.debug("addItem called with no item")
        return False

    if not isinstance(item, str):
        logging.warning("addItem: item should be a string: %r", item)
        return False

    try:
        qty_int = int(qty)
    except (TypeError, ValueError):
        logging.warning("addItem: qty must be an integer: %r", qty)
        return False

    if qty_int <= 0:
        logging.warning("addItem: qty must be positive: %d", qty_int)
        return False

    stock_data[item] = stock_data.get(item, 0) + qty_int
    # Use lazy formatting so logging can avoid unnecessary formatting
    logging.info("%s: Added %d of %s", datetime.now(), qty_int, item)
    return True


def remove_item(item, qty):
    """Remove qty of item from stock_data.

    Returns True if removed, False otherwise.
    """
    if not isinstance(item, str):
        logging.warning("removeItem: item should be a string: %r", item)
        return False

    try:
        qty_int = int(qty)
    except (TypeError, ValueError):
        logging.warning("removeItem: qty must be an integer: %r", qty)
        return False

    if qty_int <= 0:
        logging.warning("removeItem: qty must be positive: %d", qty_int)
        return False

    if item not in stock_data:
        logging.warning("removeItem: item not in stock: %s", item)
        return False

    stock_data[item] -= qty_int
    if stock_data[item] <= 0:
        del stock_data[item]

    logging.info("%s: Removed %d of %s", datetime.now(), qty_int, item)
    return True


def get_qty(item):
    """Return quantity of item or 0 if not present."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Return dict loaded from JSON inventory file or empty dict.

    Does not mutate module-level state; caller should merge the
    returned mapping into the runtime inventory if desired.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
        logging.warning(
            "load_data: data in %s is not a dict, ignoring", file
        )
        return {}
    except FileNotFoundError:
        logging.info(
            "load_data: %s not found, starting with empty inventory",
            file,
        )
        return {}
    except json.JSONDecodeError:
        logging.exception("load_data: failed to parse %s", file)
        return {}


def save_data(file="inventory.json"):
    """Save stock_data to JSON file."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=2)
    except OSError:
        logging.exception("save_data: failed to write to %s", file)


def print_data():
    """Print a simple items report to stdout."""
    print("Items Report")
    for name, qty in stock_data.items():
        print(name, "->", qty)


def check_low_items(threshold=5):
    """Return list of items with quantity below threshold."""
    result = []
    for name, qty in stock_data.items():
        if qty < threshold:
            result.append(name)
    return result


def main():
    """Run a small demonstration of inventory operations."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

    # Valid operations
    add_item("apple", 10)
    add_item("banana", 2)

    # Demonstrate invalid inputs (will be logged and ignored)
    add_item(123, "ten")  # invalid types, will be rejected

    remove_item("apple", 3)
    remove_item("orange", 1)  # not present, will be logged

    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())

    save_data()
    # Merge loaded data into existing in-memory mapping without rebinding
    loaded = load_data()
    stock_data.clear()
    stock_data.update(loaded)
    print_data()


if __name__ == "__main__":
    main()

from operator import contains

import tcod

from ..game_messages import Message


class Container:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = {}

        if len(self.items) >= self.capacity:
            results["item_obtained"] = None
            results["pickup_message"] = Message(
                "You cannot carry any more, your inventory is full.",
                tcod.yellow,
            )
        else:
            results["item_obtained"] = item
            results["pickup_message"] = Message(
                "You pick up {0}.".format(item.definite_name), tcod.light_blue
            )

            self.items.append(item)

        return results

    def get_item(self, name):
        for item in self.items:
            if contains(name, item.name):
                return item

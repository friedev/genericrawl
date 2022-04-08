from copy import deepcopy

import tcod

from .ai import BasicMonster
from ..map.dungeon_generator import CAVE_FLOOR
from .slots import SlotTypes
from ..game_messages import Message
from ..status_effect import StatusEffect


def get_throw_target(game_map, **kwargs):
    target_x = kwargs.get("target_x")
    target_y = kwargs.get("target_y")

    entities = game_map.get_entities_at_tile(
        target_x, target_y, blocking_only=True
    )
    throw_target = None
    for entity in entities:
        if entity.fighter:
            throw_target = entity

    return throw_target


def equip(*args, **kwargs):
    user = args[0]
    item = args[1]

    results = user.slots.toggle_equip(item)
    equipped = results.get("equipped")
    unequipped = results.get("unequipped")

    if equipped and unequipped:
        results["use_message"] = Message(
            f"You swap out {unequipped.definite_name} for "
            f"{equipped.definite_name}.",
            tcod.light_blue,
        )
    elif equipped:
        results["use_message"] = Message(
            f"You equip {equipped.definite_name}.", tcod.light_blue
        )
    elif unequipped:
        results["use_message"] = Message(
            f"You unequip {unequipped.definite_name}.",
            tcod.light_blue,
        )

    user.fighter.hp = min(user.fighter.hp, user.fighter.max_hp)

    return results


def throw_std(*args, **kwargs):
    item = args[1]
    target_x = kwargs.get("target_x")
    target_y = kwargs.get("target_y")
    target = get_throw_target(args[2], **kwargs)

    results = {}

    if not target:
        return {"item_moved": item, "item_x": target_x, "item_y": target_y}

    amount = kwargs.get("amount")
    if not amount and item.equipment:
        amount = max(1, int(item.equipment.damage_bonus / 2))
    else:
        amount = 1

    results.update(target.fighter.take_damage(amount))
    results.update({"item_consumed": item})

    if amount > 0:
        results["use_message"] = Message(
            (
                f"{item.definite_name} hits {target.definite_name} for "
                f"{amount} HP, breaking on impact."
            ).capitalize(),
            tcod.green,
        )
    else:
        results["use_message"] = Message(
            (
                f"{item.definite_name} shatters harmlessly against "
                f"{target.definite_name}."
            ).capitalize(),
            tcod.yellow,
        )
    return results


def heal(*args, **kwargs):
    item = args[1]
    amount = kwargs.get("amount")
    throwing = kwargs.get("throwing")
    combining = kwargs.get("combining")

    if combining:
        combine_target = kwargs.get("combine_target")

        if combine_target.equipment:
            results = {}
            if combine_target.equipment.slot is SlotTypes.WEAPON:
                weapon_amount = kwargs.get("weapon_amount")
                if combine_target.equipment.enchantments.get("damage_bonus"):
                    combine_target.equipment.enchantments[
                        "damage_bonus"
                    ] += weapon_amount
                else:
                    combine_target.equipment.enchantments[
                        "damage_bonus"
                    ] = weapon_amount
                combine_target.equipment.n_enchantments -= 1
                results.update(
                    {
                        "use_message": Message(
                            (
                                f"{combine_target.definite_name} loses "
                                f"{abs(weapon_amount)} damage."
                            ).capitalize(),
                            tcod.red,
                        )
                    }
                )
            elif combine_target.equipment.slot is SlotTypes.ARMOR:
                armor_amount = kwargs.get("armor_amount")
                if combine_target.equipment.enchantments.get("max_hp_bonus"):
                    combine_target.equipment.enchantments[
                        "max_hp_bonus"
                    ] += armor_amount
                else:
                    combine_target.equipment.enchantments[
                        "max_hp_bonus"
                    ] = armor_amount
                combine_target.equipment.n_enchantments += 1
                results.update(
                    {
                        "use_message": Message(
                            (
                                f"{combine_target.definite_name} gains "
                                f"{armor_amount} max HP."
                            ).capitalize(),
                            tcod.green,
                        )
                    }
                )

            results.update({"item_consumed": item})
            return results
        return {}

    if not throwing:
        target = args[0]
    else:
        target = get_throw_target(args[2], **kwargs)
        if not target:
            target_x = kwargs.get("target_x")
            target_y = kwargs.get("target_y")
            return {"item_moved": item, "item_x": target_x, "item_y": target_y}

    results = {}

    player_using = target == args[0]

    if target.fighter.hp == target.fighter.max_hp:
        results["use_message"] = Message(
            "The rune has no effect.", tcod.yellow
        )
    else:
        if isinstance(amount, float):
            actual_amount = int(target.fighter.max_hp * amount)
        else:
            actual_amount = amount

        amount_healed = target.fighter.heal(actual_amount)
        results["item_consumed"] = item
        if player_using:
            results["use_message"] = Message(
                f"You feel rejuvenated! You recover {amount_healed} HP.",
                tcod.green,
            )
        else:
            results["use_message"] = Message(
                (
                    f"{target.definite_name} recovers {amount_healed} HP."
                ).capitalize(),
                tcod.red,
            )

    return results


def pain(*args, **kwargs):
    item = args[1]
    amount = kwargs.get("amount")
    combining = kwargs.get("combining")
    throwing = kwargs.get("throwing")

    if combining:
        combine_target = kwargs.get("combine_target")
        if combine_target.equipment:
            results = {}
            if combine_target.equipment.slot is SlotTypes.WEAPON:
                weapon_amount = kwargs.get("weapon_amount")
                if combine_target.equipment.enchantments.get("damage_bonus"):
                    combine_target.equipment.enchantments[
                        "damage_bonus"
                    ] += weapon_amount
                else:
                    combine_target.equipment.enchantments[
                        "damage_bonus"
                    ] = weapon_amount
                combine_target.equipment.n_enchantments += 1
                results.update(
                    {
                        "use_message": Message(
                            (
                                f"{combine_target.definite_name} gains "
                                f"{weapon_amount} damage."
                            ).capitalize(),
                            tcod.green,
                        )
                    }
                )
            elif combine_target.equipment.slot is SlotTypes.ARMOR:
                armor_amount = kwargs.get("armor_amount")
                if combine_target.equipment.enchantments.get("max_hp_bonus"):
                    combine_target.equipment.enchantments[
                        "max_hp_bonus"
                    ] += armor_amount
                else:
                    combine_target.equipment.enchantments[
                        "max_hp_bonus"
                    ] = armor_amount
                combine_target.equipment.n_enchantments -= 1
                results.update(
                    {
                        "use_message": Message(
                            (
                                f"{combine_target.definite_name} loses "
                                f"{abs(armor_amount)} max HP."
                            ).capitalize(),
                            tcod.red,
                        )
                    }
                )

            results.update({"item_consumed": item})
            return results
        return {}

    if not throwing:
        target = args[0]
    else:
        target = get_throw_target(args[2], **kwargs)
        if not target:
            target_x = kwargs.get("target_x")
            target_y = kwargs.get("target_y")
            return {"item_moved": item, "item_x": target_x, "item_y": target_y}

    player_using = target == args[0]

    if isinstance(amount, float):
        actual_amount = int(target.fighter.max_hp * amount)
    else:
        actual_amount = amount

    results = target.fighter.take_damage(actual_amount)
    results["item_consumed"] = item
    if player_using:
        results["use_message"] = Message(
            f"You feel a searing pain! You lose {actual_amount} HP.",
            tcod.red,
        )
    else:
        results["use_message"] = Message(
            f"{target.definite_name} loses {actual_amount} HP.".capitalize(),
            tcod.green,
        )

    return results


def might(*args, **kwargs):
    item = args[1]
    amount = kwargs.get("amount")
    duration = kwargs.get("duration")
    combining = kwargs.get("combining")
    throwing = kwargs.get("throwing")

    if combining:
        combine_target = kwargs.get("combine_target")
        if (
            combine_target.equipment
            and combine_target.equipment.slot is SlotTypes.WEAPON
        ):
            weapon_amount = kwargs.get("weapon_amount")
            combine_target.equipment.n_enchantments += 1
            if combine_target.equipment.enchantments.get("attack_bonus"):
                combine_target.equipment.enchantments[
                    "attack_bonus"
                ] += weapon_amount
            else:
                combine_target.equipment.enchantments[
                    "attack_bonus"
                ] = weapon_amount
            return {
                "use_message": Message(
                    (
                        f"{combine_target.definite_name} gains "
                        f"{weapon_amount} attack."
                    ).capitalize(),
                    tcod.green,
                ),
                "item_consumed": item,
            }
        return {}

    if not throwing:
        target = args[0]
    else:
        target = get_throw_target(args[2], **kwargs)
        if not target:
            target_x = kwargs.get("target_x")
            target_y = kwargs.get("target_y")
            return {"item_moved": item, "item_x": target_x, "item_y": target_y}

    player_using = target == args[0]

    if isinstance(amount, float):
        actual_amount = int(target.fighter.attack * amount)
    else:
        actual_amount = amount

    total_amount = actual_amount
    existing_effect = target.get_status_effect("strengthened")
    if existing_effect:
        total_amount += existing_effect.properties.get("attack_bonus")
        duration += target.status_effects.get(existing_effect)
        target.status_effects.pop(existing_effect)

    target.status_effects.update(
        {
            StatusEffect(
                "strengthened", {"attack_bonus": total_amount}, None
            ): duration
        }
    )

    results = {"item_consumed": item}
    if player_using:
        results["use_message"] = Message(
            (
                f"Your muscles grow rapidly! You gain {actual_amount} attack."
            ).capitalize(),
            tcod.green,
        )
    else:
        results["use_message"] = Message(
            f"{target.definite_name} appears stronger.".capitalize(),
            tcod.red,
        )

    return results


def protection(*args, **kwargs):
    item = args[1]
    amount = kwargs.get("amount")
    duration = kwargs.get("duration")
    combining = kwargs.get("combining")
    throwing = kwargs.get("throwing")

    if combining:
        combine_target = kwargs.get("combine_target")
        if (
            combine_target.equipment
            and combine_target.equipment.slot is SlotTypes.ARMOR
        ):
            armor_amount = kwargs.get("armor_amount")
            combine_target.equipment.n_enchantments += 1
            if combine_target.equipment.enchantments.get("defense_bonus"):
                combine_target.equipment.enchantments[
                    "defense_bonus"
                ] += armor_amount
            else:
                combine_target.equipment.enchantments[
                    "defense_bonus"
                ] = armor_amount
            return {
                "use_message": Message(
                    (
                        f"{combine_target.definite_name} gains "
                        f"{armor_amount} defense."
                    ).capitalize(),
                    tcod.green,
                ),
                "item_consumed": item,
            }
        return {}

    if not throwing:
        target = args[0]
    else:
        target = get_throw_target(args[2], **kwargs)
        if not target:
            target_x = kwargs.get("target_x")
            target_y = kwargs.get("target_y")
            return {"item_moved": item, "item_x": target_x, "item_y": target_y}

    player_using = target == args[0]

    if isinstance(amount, float):
        actual_amount = int(target.fighter.defense * amount)
    else:
        actual_amount = amount

    total_amount = actual_amount
    existing_effect = target.get_status_effect("protected")
    if existing_effect:
        total_amount += existing_effect.properties.get("defense_bonus")
        duration += target.status_effects.get(existing_effect)
        target.status_effects.pop(existing_effect)

    target.status_effects.update(
        {
            StatusEffect(
                "protected", {"defense_bonus": total_amount}, None
            ): duration
        }
    )

    results = {"item_consumed": item}
    if player_using:
        results["use_message"] = Message(
            f"Your body feels tougher! You gain {actual_amount} defense.",
            tcod.green,
        )
    else:
        results["use_message"] = Message(
            f"{target.definite_name} appears more resilient.".capitalize(),
            tcod.red,
        )

    return results


def teleportation(*args, **kwargs):
    item = args[1]
    game_map = args[2]
    combining = kwargs.get("combining")
    throwing = kwargs.get("throwing")

    if combining:
        combine_target = kwargs.get("combine_target")
        x, y = game_map.find_open_tile()
        return {
            "use_message": Message(
                (
                    f"{combine_target.definite_name} suddenly vanishes."
                ).capitalize(),
                tcod.yellow,
            ),
            "item_consumed": item,
            "move_item": combine_target,
            "target_x": x,
            "target_y": y,
        }

    if not throwing:
        target = args[0]
    else:
        target = get_throw_target(game_map, **kwargs)
        if not target:
            return {
                "use_message": Message(
                    f"{item.definite_name} suddenly vanishes.".capitalize(),
                    tcod.magenta,
                ),
                "item_consumed": item,
            }

    player_using = target == args[0]

    target.x, target.y = game_map.find_open_tile()

    results = {"item_consumed": item}
    if player_using:
        results["use_message"] = Message(
            "Space warps around you and your surroundings suddenly change.",
            tcod.magenta,
        )
        results["recompute_fov"] = True
    else:
        results["use_message"] = Message(
            f"{target.definite_name} suddenly vanishes.".capitalize(),
            tcod.yellow,
        )

    return results


def digging(*args, **kwargs):
    item = args[1]
    game_map = args[2]
    combining = kwargs.get("combining")
    throwing = kwargs.get("throwing")

    if combining:
        combine_target = kwargs.get("combine_target")
        return {
            "use_message": Message(
                (
                    f"{combine_target.definite_name} crumbles into dust."
                ).capitalize(),
                tcod.orange,
            ),
            "item_consumed": [item, combine_target],
        }

    if game_map.dungeon_level == 10:
        return {
            "use_message": Message(
                "The ground is too hard to dig through here.", tcod.yellow
            ),
            "item_consumed": item,
        }

    if not throwing:
        target = args[0]
    else:
        target = get_throw_target(game_map, **kwargs)
        if not target:
            target_x = kwargs.get("target_x")
            target_y = kwargs.get("target_y")
            for x in range(target_x - 1, target_x + 2):
                for y in range(target_y - 1, target_y + 2):
                    if game_map.contains(x, y):
                        game_map.generator.grid[x][y] = CAVE_FLOOR

            return {
                "use_message": Message(
                    (
                        f"The walls collapse around the {item.definite_name}."
                    ).capitalize(),
                    tcod.orange,
                ),
                "item_consumed": item,
                "update_fov_map": True,
                "recompute_fov": True,
            }

    player_using = target == args[0]

    results = {"item_consumed": item}
    if player_using:
        results["use_message"] = Message(
            "A pit opens beneath you!", tcod.orange
        )
        results["recompute_fov"] = True
        results["next_level"] = True
    else:
        results["use_message"] = Message(
            f"The ground beneath {target.definite_name} collapses.",
            tcod.orange,
        )
        game_map.entities.remove(target)

    return results


def replication(*args, **kwargs):
    item = args[1]
    game_map = args[2]
    combining = kwargs.get("combining")
    throwing = kwargs.get("throwing")

    if combining:
        combine_target = kwargs.get("combine_target")
        player = args[0]
        player.container.items.append(deepcopy(combine_target))
        return {
            "use_message": Message(
                (
                    f"{item.definite_name} morphs into "
                    f"{combine_target.indefinite_name}."
                ).capitalize(),
                tcod.yellow,
            ),
            "item_consumed": item,
        }

    if not throwing:
        target = args[0]
    else:
        target = get_throw_target(game_map, **kwargs)
        if not target:
            target_x = kwargs.get("target_x")
            target_y = kwargs.get("target_y")
            return {"item_moved": item, "item_x": target_x, "item_y": target_y}

    player_using = target == args[0]

    results = {"item_consumed": item}
    if player_using:
        clone = deepcopy(target)
        clone.ai = BasicMonster()
        clone.ai.owner = clone
        clone.name = "clone"
        clone.container = None
        clone.fighter.base_max_hp = clone.fighter.max_hp
        clone.fighter.base_attack = clone.fighter.attack
        clone.fighter.base_defense = clone.fighter.defense
        clone.fighter.base_damage = clone.fighter.damage
        clone.slots = None

        game_map.entities.append(clone)
        for x in range(target.x - 1, target.x + 2):
            for y in range(target.y - 1, target.y + 2):
                if game_map.is_tile_open(x, y):
                    clone.x = x
                    clone.y = y

        if clone.x != target.x or clone.y != target.y:
            results["use_message"] = Message(
                (
                    f"{item.definite_name} morphs into a hostile adventurer!"
                ).capitalize(),
                tcod.yellow,
            )
        else:
            clone.x, clone.y = game_map.find_open_tile()
            results["use_message"] = Message(
                "You feel a vague familiar presence.", tcod.yellow
            )
    else:
        clone = deepcopy(target)

        game_map.entities.append(clone)
        for x in range(target.x - 1, target.x + 2):
            for y in range(target.y - 1, target.y + 2):
                if game_map.is_tile_open(x, y):
                    clone.x = x
                    clone.y = y

        if clone.x != target.x or clone.y != target.y:
            results["use_message"] = Message(
                (
                    f"{item.definite_name} morphs into "
                    f"{target.indefinite_name}!"
                ).capitalize(),
                tcod.yellow,
            )
        else:
            clone.x, clone.y = game_map.find_open_tile()
            results["use_message"] = Message(
                "You feel a vague hostile presence.", tcod.yellow
            )

    return results


def cancellation(*args, **kwargs):
    item = args[1]
    game_map = args[2]
    combining = kwargs.get("combining")
    throwing = kwargs.get("throwing")

    if combining:
        combine_target = kwargs.get("combine_target")

        if combine_target.equipment and combine_target.equipment.enchantments:
            combine_target.equipment.enchantments = {}
            combine_target.equipment.n_enchantments = 0
            return {
                "use_message": Message(
                    (
                        "The glow of enchantment fades from "
                        f"{combine_target.definite_name}."
                    ),
                    tcod.yellow,
                ),
                "item_consumed": item,
            }

        return {}

    if not throwing:
        target = args[0]
    else:
        target = get_throw_target(game_map, **kwargs)
        if not target:
            target_x = kwargs.get("target_x")
            target_y = kwargs.get("target_y")
            return {"item_moved": item, "item_x": target_x, "item_y": target_y}

    player_using = target == args[0]
    if target.status_effects:
        target.status_effects = {}

        results = {"item_consumed": item}
        if player_using:
            results["use_message"] = Message(
                "You feel normal again.", tcod.yellow
            )
        else:
            results["use_message"] = Message(
                f"{target.definite_name} returns to normal.".capitalize(),
                tcod.yellow,
            )
    else:
        results = {
            "item_consumed": item,
            "use_message": Message(
                f"{item.definite_name} has no effect.".capitalize(),
                tcod.yellow,
            ),
        }

    return results


class Item:
    def __init__(
        self,
        use_function=None,
        combine_function=None,
        throw_function=throw_std,
        **kwargs,
    ):
        self.use_function = use_function
        self.combine_function = combine_function
        self.throw_function = throw_function
        self.function_kwargs = kwargs

    def use(self, user, game_map, **kwargs):
        kwargs.update(self.function_kwargs)

        if kwargs.get("combining") and self.combine_function:
            return self.combine_function(user, self.owner, game_map, **kwargs)
        if kwargs.get("throwing") and self.throw_function:
            return self.throw_function(user, self.owner, game_map, **kwargs)
        if self.use_function:
            return self.use_function(user, self.owner, game_map, **kwargs)

        return {
            "use_message": Message(
                f"{self.owner.definite_name} cannot be used.".capitalize(),
                tcod.yellow,
            )
        }

import tcod


def menu(
    console, header, options, width, screen_width, screen_height, selection
):
    # Calculate total height for the header (after auto-wrap) and one line per option
    header_height = tcod.console_get_height_rect(
        console, 0, 0, width, screen_height, header
    )
    height = len(options) + header_height

    # Create an off-screen console that represents the menu's window
    window = tcod.console_new(width, height)

    # Print the header, with auto-wrap
    tcod.console_set_default_foreground(window, tcod.white)
    tcod.console_print_rect_ex(
        window, 0, 0, width, height, tcod.BKGND_NONE, tcod.LEFT, header
    )

    # Print all the options
    y = header_height
    number_shortcut = 1
    for option_text in options:
        if number_shortcut <= 10:
            text = str(number_shortcut % 10) + ". " + option_text
        else:
            text = "  " + option_text

        if selection is number_shortcut - 1:
            tcod.console_set_default_foreground(window, tcod.light_blue)

        tcod.console_print_ex(window, 0, y, tcod.BKGND_NONE, tcod.LEFT, text)
        tcod.console_set_default_foreground(window, tcod.white)

        y += 1
        number_shortcut += 1

    # Blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    tcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def inventory_menu(
    console,
    header,
    player,
    inventory_width,
    screen_width,
    screen_height,
    selection,
    options=None,
):
    # Show a menu with each item of the inventory as an option
    if len(player.container.items) == 0:
        header = header + "\nInventory is empty."
        options = []
    elif not options:
        options = construct_inventory_options(player)

    menu(
        console,
        header,
        options,
        inventory_width,
        screen_width,
        screen_height,
        selection,
    )


def construct_inventory_options(player):
    player.container.items = sorted(
        player.container.items,
        key=lambda i: i.equipment.tier if i.equipment else 0,
        reverse=True,
    )

    options = []
    stacks = {}

    for item in player.container.items:
        item_string = item.name
        if item.equipment:
            if item.equipment.enchantments:
                item_string = (
                    "{0}{1} ".format(
                        "-" if item.equipment.n_enchantments < 0 else "+",
                        abs(item.equipment.n_enchantments),
                    )
                    + item_string
                )

            item_string += " [{0}]".format(item.equipment.tier)

            if player.slots.is_equipped(item):
                item_string += " (equipped)"

            options.append(item_string)
        else:
            stack = stacks.get(item.name)
            if stack:
                stacks[item.name] += 1
            else:
                stacks[item.name] = 1

    for stack in stacks.keys():
        amount = stacks.get(stack)
        if amount == 1:
            options.append(stack)
        else:
            options.append("{0} (x{1})".format(stack, stacks.get(stack)))

    return options

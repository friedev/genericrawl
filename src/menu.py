import libtcodpy as libtcod


def menu(console, header, options, width, screen_width, screen_height, selection):
    # Calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(console, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # Create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # Print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # Print all the options
    y = header_height
    number_shortcut = 1
    for option_text in options:
        if number_shortcut <= 10:
            text = str(number_shortcut % 10) + '. ' + option_text
        else:
            text = option_text

        if selection is number_shortcut - 1:
            libtcod.console_set_default_foreground(window, libtcod.light_blue)

        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        libtcod.console_set_default_foreground(window, libtcod.white)

        y += 1
        number_shortcut += 1

    # Blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def inventory_menu(console, header, player, inventory_width, screen_width, screen_height, selection):
    # Show a menu with each item of the inventory as an option
    if len(player.container.items) == 0:
        header = header + '\nInventory is empty.'
        options = []
    else:
        options = []

        for item in player.container.items:
            if player.slots.is_equipped(item):
                options.append(item.name + ' (equipped)')
            else:
                options.append(item.name)

    menu(console, header, options, inventory_width, screen_width, screen_height, selection)
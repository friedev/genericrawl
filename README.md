# GeneriCrawl

A simple roguelike made with Python and libtcod as part of the 2018 [r/roguelikedev Does The Complete 
Roguelike Tutorial](https://redd.it/8ql895) event. As of August 7, 2018, the game is feature-complete but will to continue to receive minor features, balance improvements, and bug fixes for a short time.

## Notable Features

* 15 enemies, 15 weapons, 8 pieces of armor, 5 runes, and 10 dungeon levels.
  * Runes can be consumed, thrown, or used for enchanting.
  * Levels are divided into 3 distinct areas: the dungeon, the caves, and the labyrinth.
  * Levels vary in size, with some containing over 8,000 tiles.
* A damage calculation system based on only 4 stats: HP, attack, defense, and damage.
  * Attack and defense determine hit chance, while damage is the full damage dealt on a hit.
* AI that will start chasing you on sight, but can be escaped by breaking line of sight for long enough.
* A focus on gameplay with as little tedium as possible.
* Multiple color schemes and input schemes that can be changed while in-game (see below).

## Installation

### Windows

Download a Windows binary from [itch.io](https://maugrift.itch.io/genericrawl) or the latest [GitHub release](https://github.com/Maugrift/GeneriCrawl/releases). Extract it and run GeneriCrawl.exe.

If the binary doesn't work for you, consider trying the cross-platform option below.

### Cross-Platform (Python)

Download the latest version of [Python 3](https://www.python.org/downloads/).

Download the latest [GitHub release](https://github.com/Maugrift/GeneriCrawl/releases) or the source code from [GitHub](https://github.com/Maugrift/GeneriCrawl). Downloading the source code will provide more recent features, but may be less stable.

Extract the files and run ``engine.py`` (double-click it or run ``python engine.py`` from the command line).

Fair warning: the game has not been tested on any platform other than Windows. Python itself is cross-platform, so the game should run on other operating systems. If you get it working on some other platform, please let me know so I can update this information.

## Controls

GeneriCrawl comes with multiple common roguelike control schemes, as well as a less common left-handed control scheme.

While controls and colors can be changed in-game, to change the size of the game window, open ``options.json`` with a text editor like Notepad. Change the numbers after "screen_width" and "screen_height". Each tile is 10 pixels, so the values 72 and 128 would produce a 720x1280 resolution. Alternatively, you can enter fullscreen by pressing F11, which will automatically rescale the game to your screen size.

### All Control Schemes

The following bindings work in all of the following control schemes.

* ``-``/``=``: Change color scheme.
* ``[``/``]``: Change input scheme.
* ``1-10``: Jump to an item in the inventory. Note that these are the number row keys, not numbers on the number pad.
* ``space``/``.``: Wait one turn.
* ``space``/``enter``: Select an item or location.
* ``r``: If you're dead, restart the game.

Also note that, for all movement schemes, you can press the center key to wait a turn.

### Number Pad

Recommended for all players with a number pad.

```
7  8  9
 \ | /
4--5--6
 / | \
1  2  3
```


* ``i``: Open inventory.
* ``g``/``,``: Pick up an item that you're standing on.
* ``d``: While in the inventory, drop the currently selected item.
* ``e``: While in the inventory, use the currently selected item.
* ``r``: While in the inventory, combine the currently selected item with another. Select another item and press the key again.
* ``t``: While in the inventory, throw the currently selected item.
* ``l``: Navigate to a tile to see its contents and pan the view.


### VI Keys

Only recommended for players with prior experience using VI keys.

```
y  k  u
 \ | /
h--.--l
 / | \
n  j  n
```

* ``i``: Open inventory.
* ``g``/``,``: Pick up an item that you're standing on.
* ``d``: While in the inventory, drop the currently selected item.
* ``e``: While in the inventory, use the currently selected item.
* ``r``: While in the inventory, combine the currently selected item with another. Select another item and press the key again.
* ``t``: While in the inventory, throw the currently selected item.
* ``;``: Navigate to a tile to see its contents and pan the view.

### Left-Hand

If you don't have a number pad, aren't experienced with VI, or want to use the mouse more, this control scheme is for you.

```
Q  W  E
 \ | /
A--S--D
 / | \
Z  X  C
```

* ``tab``: Open inventory.
* ``g``: Pick up an item that you're standing on.
* ``b``: While in the inventory, drop the currently selected item.
* ``r``: While in the inventory, use the currently selected item.
* ``f``: While in the inventory, combine the currently selected item with another. Select another item and press the key again.
* ``t``: While in the inventory, throw the currently selected item.
* ``v``: Navigate to a tile to see its contents and pan the view.

## Goal

Reach the bottom floor of the dungeon - the labyrinth - and escape it (preferably in one piece).

## Contact

Have a question to ask? A cool suggestion? Feel free to contact me on any of the platforms below:

* [@Maugrift](https://twitter.com/Maugrift) on Twitter
* [u/Maugrift](https://reddit.com/u/Maugtift) on Reddit
* Maugrift#5077 on Discord
  * I'm also somewhat active on the [roguelikes Discord](https://discord.gg/9pmFGKx), so you can also @ me there if you'd prefer.

Having problems with the game? If you can, open an issue on GitHub [here](https://github.com/Maugrift/GeneriCrawl/issues). Otherwise, you can you contact me with one of the links above.

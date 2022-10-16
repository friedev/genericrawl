# GeneriCrawl

A simple roguelike made in Python with [tcod](https://github.com/libtcod/python-tcod) as part of the 2018 [r/roguelikedev Does The Complete Roguelike Tutorial](https://redd.it/8ql895) event.
Can you reach the bottom floor of the dungeon in one piece?

## Features

- 15 enemies, 15 weapons, 8 pieces of armor, 5 runes, and 10 dungeon levels
	- Runes can be consumed, thrown, or used for enchanting
	- Levels are divided into 3 distinct areas: the dungeon, the caves, and the labyrinth
	- Levels vary in size, with some containing over 8,000 tiles
- A combat system with 4 stats: HP, attack, defense, and damage
	- Attack and defense determine hit chance
	- Damage is the approximate damage dealt on a hit
- AI that will start chasing you on sight, but can be escaped by breaking line of sight for long enough
- Multiple color schemes and input schemes that can be changed while in-game

## Installation

```sh
pip install genericrawl
```

## Usage

```sh
genericrawl
```

GeneriCrawl accepts no command line arguments.

### Options

Game options are saved to `genericrawl/options.json` in your system's default config location (`$XDG_CONFIG_HOME`, `~/.config`, or `%APPDATA%`).
Controls and colors can be changed in-game and automatically written back to this file.
However, if you want to change the screen size, you will need to manually edit this file with a text editor and set the values of `screen_width` and `screen_height`.
Each tile is 10 pixels, so the values 72 and 128 would produce a 720x1280 resolution, for instance.
Alternatively, you can enter fullscreen by pressing F11 in-game, which will automatically rescale the game to your screen size.

### Controls

GeneriCrawl comes with multiple common roguelike control schemes, as well as a less common left-handed control scheme.

#### All Control Schemes

The following bindings work in all of the following control schemes.

- `-`/`=`: Change color scheme.
- `[`/`]`: Change input scheme.
- `1`-`0`: Jump to an item in the inventory.
  Note that these are the number row keys, not numbers on the number pad.
- Space/`.`: Wait one turn.
- Space/Enter: Select an item or location.
- `r`: If you're dead, restart the game.

Also note that, for all movement schemes, you can press the center key to wait a turn.

#### Number Pad

Recommended for players with a number pad.

```
7 8 9
 \|/
4-5-6
 /|\
1 2 3
```

- `i`: Open inventory.
- `g`/`,`: Pick up an item that you're standing on.
- `d`: While in the inventory, drop the currently selected item.
- `e`: While in the inventory, use the currently selected item.
- `r`: While in the inventory, combine the currently selected item with another.
  Select another item and press the key again.
- `t`: While in the inventory, throw the currently selected item.
- `l`: Navigate to a tile to see its contents and pan the view.

#### vi

Recommended for vi users.

```
Y K U
 \|/
H-.-L
 /|\
N J N
```

- `i`: Open inventory.
- `g`/`,`: Pick up an item that you're standing on.
- `d`: While in the inventory, drop the currently selected item.
- `e`: While in the inventory, use the currently selected item.
- `r`: While in the inventory, combine the currently selected item with another.
  Select another item and press the key again.
- `t`: While in the inventory, throw the currently selected item.
- `;`: Navigate to a tile to see its contents and pan the view.

#### Left-hand

Recommended if you don't have a number pad, aren't experienced with vi, or want to use the mouse more.

```
Q W E
 \|/
A-S-D
 /|\
Z X C
```

- `tab`: Open inventory.
- `g`: Pick up an item that you're standing on.
- `b`: While in the inventory, drop the currently selected item.
- `r`: While in the inventory, use the currently selected item.
- `f`: While in the inventory, combine the currently selected item with another.
  Select another item and press the key again.
- `t`: While in the inventory, throw the currently selected item.
- `v`: Navigate to a tile to see its contents and pan the view.

## Credits

GeneriCrawl was created by [Aaron Friesen](https://frie.dev) with the help of the [tcod Roguelike Tutorial](https://www.rogueliketutorials.com).

## Contributing

GeneriCrawl is no longer in development, and I do not intend to accept patches for new features.
However, GeneriCrawl is permissively licensed, so if you want to add your own features, feel free to fork the repo or just borrow parts of the code (subject to the license terms in `LICENSE.txt`).

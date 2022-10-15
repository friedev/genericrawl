# Changelog

## 1.2.0 - 2022-04-11

- GeneriCrawl is now published on PyPI (`pip install genericrawl`)
- Options are now saved to the system's default config location (`$XDG_CONFIG_HOME`, `~/.config`, or `APPDATA`)

## 1.1.1 - 2022-02-02

- Switches GeneriCrawl to using the Python `tcod` package instead of using a bundled copy of the library and DLLs
    - The Windows version is no longer supported because of this, and the Python source code should be considered the official version
- Relicense GeneriCrawl under the MIT license (permissive license fans rejoice!)

## 1.1.0 - 2018-08-11

- Adds 3 new runes
	- Runes of Digging can cause wall tiles to collapse, or can create pits for you or enemies to fall through
	- Runes of Replication morph into other items or enemies, making your inventory even more versatile
	- Runes of Cancellation cancel out status effects and enchantments
- Improves inventory UI
	- Inventory capacity is shown in the menu header
	- Equipment is labeled with a tier which can help with quick comparisons
	- Stacks runes and sorts the inventory to eliminate tedium from trying to find items
	- The number of enchantments on an item is shown with a +/- modifier
- Makes the log more readable
	- Most good events, including successful attacks against enemies, are displayed in green
	- Most bad events, including successful enemy attacks against you, are displayed in red
- Makes damage vary from the exact stat value by up to 25%, slightly reducing combat predictability
- Bug fixes
	- Stairs now generate in cave levels
	- Teleportation runes now self-consume upon being thrown

## 1.0.0 - 2018-08-07

The version of the game at the end of the [r/roguelikedev tutorial event](https://redd.it/8ql895).

# io_scene_mpet - PangYa import script for Blender
This is a Work-In-Progress importer for importing PangYa models as Blender
scenes. It was developed through careful analysis of mpet files in a hex
editor. Currently, only some versions of mpet are supported, and not fully.
This will change shortly.

Special thanks to HSReina for their universal extractor and a few pointers.
Also, to the developers of the original paktools and mpetmqo tool.

![A render of Kooh on her ship.](http://i.imgur.com/oBQ4Ysh.png)
>Who the hell designed this ship?

## Status

  * Working, supports many mpet files.
  * Mesh data, textures, and armatures are supported.

Todo:

  * Armatures: bone roll is not properly handled in import
  * Armatures: `use_connect` may be improper
  * Armatures: make sure vertex groups and bones are applied correctly
  * Textures: some textures may not resolve yet.
  * Textures: alpha mask is not automatically set up (doing so is trivial, though.)
  * Textures: for some reason, two texture slots are occupied on import per material.
  * Animations: not supported. Maybe there will be a separate apet plugin.

## Usage
Clone this git repository into:

  * Windows: `%APPDATA%\Blender Foundation\Blender\2.77\scripts\addons_contrib\io_scene_mpet`
  * Linux: `$HOME/.blender/2.77/scripts/addons_contrib/io_scene_mpet`

Then activate it in User Preferences (look at the 'Testing' add-ons.)

### What if I don't have git?
Hit [download zip](https://github.com/johnwchadwick/io_scene_mpet/archive/master.zip) and extract it such that you have a folder named `io_scene_mpet` in your `addons_contrib` directory (listed above) and that folder contains `__init__.py` (and neighboring files, of course.)
# GoblinEscape
Simple python game to avoid a goblin.
To see what this code is about, check out this video:
https://youtu.be/V0V3LMK40iI

## Basic Installation
For newbies to python

* Install python 3 from here: https://www.python.org/downloads/
* Install pygame:
  * Open a command window and type: `pip install pygame`
  * If your OS can't find pip, add it to your path.  Should be in `Python2.7/Scripts/`
  * If you get "externally-managed environment" error, you need to create a virtual environment:
	  - `python3 -m venv .venv`
	  - `source .venv/bin/activate`
	  - `pip install pygame`
	  - Every time you run this game from a new terminal window, you need to run `source .venv/bin/activate` to use the virtual environment

## Running the game
In a command window run `python GoblinEscape.py`.
You could also create a .bat or .sh file to more easily run it from the GUI.

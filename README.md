# Destiny's Path 4

An idle game that is *played* in a terminal window.

---




## Dependecies

DP4 was written and tested on Python `3.9.2`.

- [Python](https://www.python.org/downloads/) version `>= 3.9.2`  
  Linux: It's most probably already installed. Otherwise install **python3** with your favorite package manager.  
  Windows / MacOS / Other: Download the latest 3.x.x release and install it. Make sure to let the setup program *"add Python to your PATH"*.
- A terminal to run it. The default on any platform should do the trick.

---




## Usage

Change into the game directory:

```bash
cd /path/to/destinyspath4/game/
```

Run the executable:

```bash
# on *nix systems:
./dp4.py

# on windows systems:
python3 dp4.py
# or
C:\path\to\python.exe dp4.py
```

If you do not add any arguments, the following help text will be displayed:

```text
usage: dp4.py [-h] [-p] [-n NAME] [-d PATH]

optional arguments:
  -h, --help                   show this help message and exit
  -p, --play                   play the game
  -n NAME, --save-name NAME    name of the save game to create or resume from (default=save1)
  -d PATH, --save-dir PATH     path to the save data directory (default=/path/to/destinyspath4/game/data)
```

You can use either the short or long arguments. E.g. `-p` and `--play` are the same.

---




## Usage Examples

**Get help**. Display the usage help:

```bash
dp4.py
# or
dp4.py --help
```

**Play the game** - Start a new or resume a previous game if you played before using the default save data file name and directory:

```bash
dp4.py --play
```

**Start or resume a game with another name** - The save data file will be named **myothergame**:

```bash
dp4.py --play --save-name myothergame
```

**Use another save data file directory** - The save data files will be stored in **/path/to/mysavedata**:

```bash
dp4.py --play --save-dir /path/to/mysavedata
```

**All arguments combined**:

```bash
dp4.py --play --save-name myothergame --save-dir /path/to/mysavedata
```




---

## Game Text Glossary

- **cold wallet**: Currency in the cold wallet. The cold wallet can not be attacked by hackers.
- **current shell**: Current player name. Changes on rebirth.
- **deaths by accident**: Total times the player died in a random accident.
- **deaths by foes**: Total times the player died in fight.
- **deaths**: Total times the player died.
- **distance traveled**: Total distance traveled in kilometers.
- **hot wallet**: Currency in the hot wallet. The cold wallet can be attacked by hackers. Balances over a certain threshold will automatically be transfered to the cold wallet.
- **items looted**: Total items looted.
- **items sold**: Total items the player has sold.
- **items stolen by foes**: Total items stolen by other entities.
- **kills**: Total entities killed by the player.
- **koinz**: The main (crypto) currency used in the game world.
- **region level**: The level of the current region the player is in.
- **stolen by hackers**: Total currency stolen by hackers from the cold wallet.
- **trade income**: Total currency the player has earned from selling items.
- **wagon**: You temporarly store all the stuff you find on this wagon.

---




## Thanks

Some object strings were contributed by [orochihanma](https://twitch.tv/orochihanma) and [execratus](https://twitch.tv/exe_cratus).

---




## License

Copyright arT2 (etrusci.org)

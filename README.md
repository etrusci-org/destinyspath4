# Destiny's Path 4

An idle-game that is *played* in the terminal. No user input is necessary when it runs. Everything that happens depends on your luck.

It was created just for fun/learning. Like part 1-3, which I never made public ;-)

<!-- ![screenshot](./screenshot.png) -->

---




## Dependecies

- [Python](https://www.python.org/downloads/) version `>= 3.9.2`
- A terminal to run it. The default on any platform should do the trick - e.g. xterm, terminator, powershell, cmd, etc.

**Note**: DP4 was written and tested on Python  `3.9.2`. **Later Python versions could introduce breaking changes**, but usually you're good with installing the latest one. You can have multiple Python versions installed at the same time.

---




## Install / Update

1. Install [Python](https://www.python.org/downloads/).
  On *nix: It's most probably already installed. Otherwise install **python3** with your favorite package manager.
  On Windows/Other: Download the version for your operating system and install it. Make sure to let the setup program *"add Python to your PATH"*.
2. [Download](https://github.com/etrusci-org/destinyspath4/releases) the latest DP4 release.
3. Unpack the compressed release file and copy the **destinyspath4-x.x.x** directory to any place on your system.

If you want to update to a new release, just repeat those steps and copy over the previous save files.

---




## Quickstart

Open a terminal window and change into the `game/` directory:

```bash
cd path/to/destinyspath4/game/
```


On *nix systems:

```bash
./dp4.py --play
# maybe you have to make it executable first with `chmod +x dp4.py`
```

On Windows systems:

```bash
python3 dp4.py --play
# or if `python3` does not work try...
python3.exe dp4.py --play
# or
C:/path/to/python3/python3.exe dp4.py --play
```

Progress will be auto-saved from time to time or when you quit the game by pressing `CTRL`+`C`.

---




## Usage

You can use either the short or long arguments. E.g. `-p` and `--play` are the same.

If you do not add any arguments, the following help text will be displayed:

```text
usage: dp4.py [-h] [-p] [-n NAME] [-d PATH]

optional arguments:
  -h, --help                   show this help message and exit
  -p, --play                   play the game
  -n NAME, --save-name NAME    name of the save game to create or resume from (default=game1)
  -d PATH, --save-dir PATH     path to the save data directory (default=/path/to/destinyspath4/game/save)
```

---




## Usage Examples

**Display the quick help**:

```bash
dp4.py
```

```bash
dp4.py --help
```

```bash
dp4.py -h
```

**Play the game** - Starts or resumes a game using the default save data file name and directory:

```bash
dp4.py --play
```

```bash
dp4.py -p
```

**Start or resume a game with another name** - The save data file will be named **myothergame**:

```bash
dp4.py --play --save-name myothergame
```

```bash
dp4.py -p -n myothergame
```

**Use another save data file directory** - The save data files will be stored in **/path/to/mysavedata**:

```bash
dp4.py --play --save-dir /path/to/mysavedata
```

```bash
dp4.py -p -d /path/to/mysavedata
```

**All arguments combined**:

```bash
dp4.py --play --save-name myothergame --save-dir /path/to/mysavedata
```

```bash
dp4.py -p -n myothergame -d /path/to/mysavedata
```

---




## Thanks

Some asset text data was contributed by [orochihanma](https://twitch.tv/orochihanma) and [execratus](https://twitch.tv/exe_cratus) in:
- [object_name.dat](./game/asset/object_name.dat)
- [object_prefix.dat](./game/asset/object_prefix.dat)
- [object_suffix.dat](./game/asset/object_suffix.dat)

---




## License

Public Domain

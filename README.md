# pyI2L

The tool was created to assist in quick offline prototyping of [Crowdin](https://crowdin.com) localization projects. It is my hope that it's also useful to mod community translations into Unity games utilizing the [I2 Localization Engine](https://inter-illusion.com/forum/i2-localization).

## Installation

Download the latest Windows release to the right, or clone the repo and run with `python -m pyI2L`.

## Usage

`.\pyI2L.exe ASSETS OPTIONS`

Use without arguments to extract `./resources.assets.csv` from `./resources.assets`. The CSV will be in the format used by The Wandering Village Crowdin project.

### `-a`, `--apply`

Sets apply mode and specifies the source file that contains the translations that should be modded into the bundle. Omitting it will set extract mode.

### `-f`, `--format`

In apply mode it sets how the applied file will be parsed. In extract mode it will format the output file accordingly. Formatters can be installed by dropping them in the `parsers` directory. See [#Installing a formatter](#installing_a_formatter). Defaults to `Wavi` (for The Wandering Village Crowdin project). `rawCSV` recommended as a project-agnostic choice.

### `-o`, `--output`

Sets the path of the produced file. In extract mode it defaults to `[ASSETS].[EXT]`, where `EXT` is an appropriate file extension for the used format. In apply mode it defaults to `[ASSETS]` and so will overwrite it.

Use `./pyI2L.exe -h` for more information on usage.

### Steps to mod in a custom translation for beginners
You need to run the commands in a command-line interface (CLI). CLI commands are executed relative to a directory (the "current working directory"), this is the path shown at the beginning of the line. On Windows you can open a terminal in a directory by Shift-clicking a directory and selecting "Open in Terminal". Alternatively, you can change the working directory by the `cd [PATH]` command.

1. Find the I2Localization asset. It's usually in `resources.assets` in the `[GAME NAME]_Data` directory, but you can make sure by searching for a known string with `grep -rF KNOWN_STRING` (on Linux).
2. Get the strings in some way:
    * Download it from a Crowdin project by selecting "Download" on the correct file.
    * Run the tool in extract mode (without arguments, or only specifying format and output) in the same directory as the assets file. The recommended format for generic projects is `rawCSV`.
3. Make your edits to the strings.
4. Run the tool with `./pyI2L.exe -a Wavi_Localization.csv` (substituting the appropriate file name) if your strings and assets file are in the same directory. This will overwrite the assets file, you might want to back it up first.


## Installing a formatter<a name="installing_a_formatter"></a>

The module should export an iterable `Reader(file_path: str)` class with a `languages` and `padding` attribute.

`next(Reader())` should return a list of strings containing a key and its translations:

```py
[key: str, value0: str, value1: str, ..., type: int]
```

`languages` should be a list of tuples containing column/language names and an int for every alternative:

```py
[(lang0.name: str, lang0.code: str, lang0.type: int), (lang1.name: str, lang1.code: str, lang1.type: int), ...]
```

`padding` should be an `int` specifying the number of `\x00` bytes between records of the I2Languages binary representation. 16 is a common default.

The module should export `Writer(data: I2)` class with a `to_bytes()` method.

```py
class I2:
    languages: Languages
    body: Body
    header: Header
class Languages:
    length: int # Number of languages/columns
    items: list[tuple[Field, Field, int]]
class Body:
    padding: int # Between Records
    length: int # Number of records
    items: list[Record]
class Record:
    id: int # Key
    type: int # Usually 0, 9 for some records in some games. The meaning is unkown
    length: int # Number of fields
    items: list[Field]
class Field:
    v: str # Value
    span: int # Byte length of value
    padding: int # After value (4-byte alignment)
class Header: ...
```

Every class has a `to_bytes()` method.

The module can optionally export an `ext` string to be used as a default extension by the CLI app.

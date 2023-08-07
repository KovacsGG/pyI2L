# pyI2L

The tools was created to assist in quick offline prototyping of [Crowdin](https://crowdin.com) localization projects. It is my hope that it's also useful to mod community translations into Unity games utilizing the [I2 Localization Engine](https://inter-illusion.com/forum/i2-localization).

## Usage

Use without arguments to convert `./Wavi_Localization.csv` exported from The Wandering Village Crowdin project into `./I2Languages-resources.assets-80.dat`

Use with `-h` for information on other switches.

To install a custom format drop it in the parsers directory. The module should export an iterable `Reader` class with a `languages` attribute.

### Steps to mod in a custom translation
1. Get [Unity Asset Bundle Extractor](https://github.com/SeriousCache/UABE/releases) (UABE).
2. Get the strings in some way:
    * Download it from a Crowdin project by selecting "Download" on the correct file.
    * Use UABE and extract the I2Languages asset from an `.assets` file. (You can use binary search for a known string to find the correct file, but it's often `resources.assets`.) Then, convert it to CSV using the tool.
3. Make your edits to the strings.
4. Run the tool with no arguments if your CSV is in the same directory and is named `Wavi_Localization.csv`.
5. Use UABE to mod in the created file:
    1. Rename `{XXX_Data}/resources.assets` (or wherever the I2Languages asset is of the game) to `resources.assets.old`.
    2. Open the renamed file in UABE.
    3. Find and select the I2Languages asset.
    4. Click "Import Raw".
    5. Select the file created in step 4.
    6. File>Apply and Save All 
    7. Save as the original file (`resources.assets`)

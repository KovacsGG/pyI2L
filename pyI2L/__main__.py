#!/usr/bin/env python3
from pyI2L import read_assets, read_input, write_assets, write_output, read_bundle, get_i2l_asset
from pyI2L import parsers

import argparse
from sys import stderr

PROJECT_URL = "https://github.com/KovacsGG/pyI2L"
BUGS_URL = PROJECT_URL + "/issues"

argParser = argparse.ArgumentParser(description="Convert between Inter Illusion's\
                                    I2 Localization Unity assets\
                                    and exported localization files.",
                                    usage="%(prog)s ASSETS [options]",
                                    epilog=f"See also {PROJECT_URL}")
argParser.add_argument("assets",
                    default="./resources.assets",
                    nargs="?",
                    help="Asset bundle file to operate on.\
                            Defaults to \"./resources.assets\"")
argParser.add_argument("-a", "--apply",
                    help="I2Languages object or CSV data \
                            with which to overwrite translations in the bundle. \
                            Omit to extract the I2L asset from the bundle.")
argParser.add_argument("-o", "--output",
                    help="Name of the output file.")
argParser.add_argument("-f", "--format",
                    default="rawCSV",
                    help=f"Formatter to read the input \
                            or write the output.\n \
                            Possible values: {parsers.__all__}\n\
                            \"rawCSV\" by default.")
argParser.add_argument("-u", "--unpack",
                    action="store_true",
                    help="Extract the I2L asset \
                            and write it to the output \
                            without any processing.")

# Validation and defaults setting
args = argParser.parse_args()
if args.format not in parsers.__all__: 
    print("Formatting module not found.", file=stderr)
    exit(1)
formatter = parsers.__dict__[args.format]
if args.output is None:
    if args.apply is not None and not args.unpack:
        args.output = args.assets
    else:
        ext = formatter.ext if hasattr(formatter, "ext") else ".out"
        args.output = args.assets + ext

# Operation
if args.unpack:
    bundle = read_bundle(args.assets)
    i2l_asset = get_i2l_asset(bundle)
    with open(args.output, "wb") as out_f:
        out_f.write(i2l_asset.raw_data)
else:

    try:
        assets = read_assets(args.assets)
    except OSError as e:
        print(f"Error reading {args.assets}: {e.strerror}", file=stderr)
        exit(1)
    except ValueError as e:
        print(f"Error parsing localizations: {e}", file=stderr)
        exit(1)
    except AssertionError as e:
        print(f"Failed format assertion: {e}\nPlease report this at {BUGS_URL}\nRun with -u and attach the generated asset to your report.", file=stderr)
        exit(1)
    except BaseException as e:
        print(f"Unexpected error reading {args.assets}. Please report this at {BUGS_URL}", file=stderr)
        raise e


    if args.apply is None:
        try:
            write_output(args.output, assets, formatter.Writer)
        except OSError as e:
            print(f"Error writing to {args.output}: {e.strerror}", file=stderr)
            exit(1)
        except UnicodeError as e:
            print(f"Unknown Unicode input at byte {e.start} ({e.object[e.start:e.end]}): {e.reason}", file=stderr)
            exit(1)
        except BaseException as e:
            print(f"Unexpected error writing to {args.output}. Please report this at {BUGS_URL}", file=stderr)
            raise e

    else:    
        try:
            apply = read_input(args.apply, formatter.Reader)
        except OSError as e:
            print(f"Error reading {args.apply}: {e.strerror}", file=stderr)
            exit(1)
        except BaseException as e:
            print(f"Unexpected error reading {args.apply}. Did you change the structure of the file?", file=stderr)
            raise e

        try:
            write_assets(args.output, args.assets, apply)
        except OSError as e:
            print(f"Error processing {e.filename}: {e.strerror}", file=stderr)
            exit(1)
        except ValueError as e:
            print(f"Error parsing Unity bundle: {e}", file=stderr)
            exit(1)
        except BaseException as e:
            print(f"Unexpected error merging translations. Please report this at {BUGS_URL}", file=stderr)
            raise e

print("Finished with no errors.")
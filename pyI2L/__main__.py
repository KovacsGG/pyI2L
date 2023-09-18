#!/usr/bin/env python3
from pyI2L import read_assets, read_input, write_assets, write_output
from pyI2L import parsers

import argparse

argParser = argparse.ArgumentParser( description="Convert between Inter Illusion's\
                                    I2 Localization Unity assets\
                                    and exported Crowdin CSV files.",
                                    usage="%(PROG)s ASSETS [options]",
                                    epilog="See also https://github.com/KovacsGG/pyI2L" )
argParser.add_argument("assets",
                    default="./resources.assets",
                    help="Asset bundle file to operate on.\
                            Defaults to \"./resources.assets\"")
argParser.add_argument("-a", "--apply",
                    help="I2Languages object or CSV data \
                            with which to overwrite translations in the bundle. \
                            Omit to extract the I2L asset from the bundle.")
argParser.add_argument("-o", "--output",
                    help="Name of the output file.")
argParser.add_argument("-f", "--format",
                    default="Wavi",
                    help=f"Formatter to read the input \
                            or write the output.\n \
                            Possible values: {parsers.__all__}\n\
                            \"Wavi\" by default.")

# Validation and defaults setting
args = argParser.parse_args()
argparse.FileType(args.assets)
formatter = parsers.__dict__[args.format]
assert args.format in parsers.__all__, "Formatting module not found"
if args.output is None:
    if args.apply is not None:
        args.output = args.assets
    else:
        ext = formatter.ext if hasattr(formatter, "ext") else ".out"
        args.output = args.assets + ext
argparse.FileType(args.output)

# Operation
assets = read_assets(args.assets)
if args.apply is None:
    write_output(args.output, assets, formatter.Writer)
else:    
    argparse.FileType(args.apply)
    apply = read_input(args.apply, formatter.Reader)
    write_assets(args.output, args.assets, apply)

print("Finished with no errors.")
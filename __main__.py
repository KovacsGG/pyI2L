#!/usr/bin/env python3
from I2 import I2

import argparse, sys
from importlib import import_module

argParser = argparse.ArgumentParser( description="Convert between Inter Illusion's\
                                     I2 Localization Unity assets\
                                     and exported Crowdin CSV files.",
                                     epilog="See also https://github.com/KovacsGG/pyI2L" )
argParser.add_argument("-i", "--input",
                       help="Input file to convert.")
argParser.add_argument("-f", "--format",
                       help="Empty for binary input or the \
                            formatter module from parsers directory \
                            to shape text input or output.")
argParser.add_argument("-o", "--output",
                       default="./out",
                       help="Name of the output file.")

args = argParser.parse_args()
if len(sys.argv) == 1:
    args.input = "./Wavi_localization.csv"
    args.output = "./I2Languages-resources.asstes-80.dat"
    args.format = "Wavi"
argparse.FileType(args.input)
argparse.FileType(args.output)

if args.format is None:
    with open(args.input, "rb") as in_f:
        try:
            data = I2(in_f)
        except Exception as e:
            print(f"Error at byte {in_f.tell()}", file=sys.stderr)
            with open("rest.hex", "wb") as rest:
                rest.write(in_f.read())
            raise e
    with open(args.output, "w", encoding="utf-8", newline='') as out_f:
        out_f.write(str(data))
else:
    try:
        formatter = import_module(f"parsers.{args.format}")
    except:
        print("Error importing formatter.", file=sys.stderr)
        exit()
    with open(args.input, "r", encoding="utf-8", newline='') as in_f:
        data = I2(formatter.Reader(in_f))
    with open(args.output, "wb") as out_f:
        out_f.write(data.to_bytes())

print("Finished with no errors.")
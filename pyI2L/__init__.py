from .UnityPy import streams, files
from .I2 import I2
from . import parsers

import io

__all__ = ["read_assets", "read_input", "write_assets", "write_output", "parsers", "I2"]


def read_bundle(file: str):
    with open(file, "rb") as in_f:
        reader = streams.EndianBinaryReader(in_f.read())
        bundle = files.SerializedFile(reader)
    return bundle


def get_i2l_asset(bundle):
    for obj in bundle.objects.values():
        if obj.type.name == "MonoBehaviour":
            bin = obj.read()
            if bin.name == "I2Languages":
                return bin
    raise ValueError("Bundle does not contain I2Languages asset.")
                

def read_assets(file: str):
    bundle = read_bundle(file)
    return I2(io.BytesIO(get_i2l_asset(bundle).raw_data))


def write_output(file: str, data: I2, format_writer):
    with open(file, "wb") as out_f:
        out_f.write(format_writer(data).to_bytes())


def read_input(file: str, format_reader):
    return I2(format_reader(file))


def write_assets(file: str, bundle_file: str, data: I2):
    bundle = read_bundle(bundle_file)
    i2l = get_i2l_asset(bundle)
    i2l.save(raw_data=data.to_bytes())
    with open(file, "wb") as out_f:
        out_f.write(bundle.save())
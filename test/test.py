import sys
sys.path.insert(0, "../pyI2L")
import pyI2L



sources = ["test/export/resources.assets", "test/export/IXION-resources.assets", "test/export/Xenonauts2-resources.assets", "test/export/TSPUD-resources.assets"]
assets = ["test/import/resources.assets", "test/import/IXION-resources.assets", "test/import/Xenonauts2-resources.assets", "test/import/TSPUD-resources.assets"]
csvs  = ["test/import/Wavi.csv", "test/import/IXION.csv", "test/import/Xenonauts2.csv", "test/import/TSPUD.csv"]
out_assets = ["test/import/Wavi.dat", "test/import/IXION.dat", "test/import/Xenonauts2.dat", "test/import/TSPUD.dat"]
for (src, asset, csv, out_f) in zip(sources, assets, csvs, out_assets):
    original = pyI2L.read_assets(src)
    pyI2L.write_assets(out_f, src, original)
    transformed = pyI2L.read_assets(out_f)
    assert original == transformed
    assert original.to_bytes() == transformed.to_bytes()
    pyI2L.write_output(csv, original, pyI2L.parsers.rawCSV.Writer)
    transformed = pyI2L.read_input(csv, pyI2L.parsers.rawCSV.Reader)
    assert original == transformed
    assert original.to_bytes() == transformed.to_bytes()
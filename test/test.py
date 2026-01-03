import sys
sys.path.insert(0, "../pyI2L")
import pyI2L



sources = ["test/export/resources.assets", "test/export/IXION-resources.assets", "test/export/Xenonauts2-resources.assets", "test/export/TSPUD-resources.assets", "test/export/VampireSurvivors-resources.assets", "test/export/OneDreamer-resources.assets", "test/export/NineSols-resources.assets"]
csvs  = ["test/import/Wavi.csv", "test/import/IXION.csv", "test/import/Xenonauts2.csv", "test/import/TSPUD.csv", "test/import/VampireSurvivors.csv", "test/import/OneDreamer.csv", "test/import/NineSols.csv"]
out_assets = ["test/import/Wavi.dat", "test/import/IXION.dat", "test/import/Xenonauts2.dat", "test/import/TSPUD.dat", "test/import/VampireSurvivors.dat", "test/import/OneDreamer.dat", "test/import/NineSols.dat"]
for (src, csv, out_f) in zip(sources, csvs, out_assets):
    original = pyI2L.read_assets(src)
    pyI2L.write_assets(out_f, src, original)
    transformed = pyI2L.read_assets(out_f)
    assert original == transformed
    assert original.to_bytes() == transformed.to_bytes()
    pyI2L.write_output(csv, original, pyI2L.parsers.rawCSV.Writer)
    transformed = pyI2L.read_input(csv, pyI2L.parsers.rawCSV.Reader)
    assert original == transformed
    assert original.to_bytes() == transformed.to_bytes()

def test_format(parser, src, out):
    original = pyI2L.read_assets(src)
    pyI2L.write_output(out, original, parser.Writer)
    transformed = pyI2L.read_input(out, parser.Reader)
    assert original == transformed
    assert original.to_bytes() == transformed.to_bytes()

test_format(pyI2L.parsers.binary, "test/export/resources.assets", "test/import/out.dat")
test_format(pyI2L.parsers.Wavi, "test/export/resources.assets", "test/import/out.csv")

print("Tests complete.")
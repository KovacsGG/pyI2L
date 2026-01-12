import shutil
import unittest

import pyI2L


class Equality(unittest.TestCase):
    def setUp(self):
        shutil.copy("test/fixtures/resources.assets", "test/input")
        
    def test_positive(self):
        i2 = pyI2L.read_assets("test/input/resources.assets")
        pyI2L.write_assets("test/output/identical-resources.assets", "test/input/resources.assets", i2)
        transformed = pyI2L.read_assets("test/output/identical-resources.assets")
        self.assertEqual(i2, transformed)
        self.assertEqual(i2.to_bytes(), transformed.to_bytes())

    def test_negative(self):
        i2 = pyI2L.read_assets("test/input/resources.assets")
        i2.body.padding += 4
        pyI2L.write_assets("test/output/transformed-resources.assets", "test/input/resources.assets", i2)
        transformed = pyI2L.read_assets("test/output/transformed-resources.assets")
        i2 = pyI2L.read_assets("test/input/resources.assets")
        self.assertNotEqual(i2, transformed)
        self.assertNotEqual(i2.to_bytes(), transformed.to_bytes())



class Integration(unittest.TestCase):
    def setUp(self):
        self.assets = ["IXION", "NineSols", "OneDreamer", "TSPUD", "VampireSurvivors", "Xenonauts2", "Wavi"]
        for s in self.assets:
            shutil.copy(f"test/fixtures/{s}-resources.assets", f"test/input")

    def test_noop(self):
        for s in self.assets:
            i2 = pyI2L.read_assets(f"test/input/{s}-resources.assets")
            pyI2L.write_assets(f"test/output/{s}-resources.assets", f"test/input/{s}-resources.assets", i2)
            transformed = pyI2L.read_assets(f"test/output/{s}-resources.assets")
            with self.subTest(assets = s):
                self.assertEqual(i2, transformed)
                self.assertEqual(i2.to_bytes(), transformed.to_bytes())

    def test_parser_binary(self):
        for s in self.assets:
            with self.subTest(assets = s):
                i2 = pyI2L.read_assets(f"test/input/{s}-resources.assets")
                pyI2L.write_output(f"test/output/{s}.binary", i2, pyI2L.parsers.binary.Writer)
                transformed = pyI2L.read_input(f"test/output/{s}.binary", pyI2L.parsers.binary.Reader)
                self.assertEqual(i2, transformed)
                self.assertEqual(i2.to_bytes(), transformed.to_bytes())
            
    def test_parser_rawCSV(self):
        for s in self.assets:
            with self.subTest(assets = s):
                i2 = pyI2L.read_assets(f"test/input/{s}-resources.assets")
                pyI2L.write_output(f"test/output/{s}.raw.csv", i2, pyI2L.parsers.rawCSV.Writer)
                transformed = pyI2L.read_input(f"test/output/{s}.raw.csv", pyI2L.parsers.rawCSV.Reader)
                self.assertEqual(i2, transformed)
                self.assertEqual(i2.to_bytes(), transformed.to_bytes())

    def test_parser_Wavi(self):
        i2 = pyI2L.read_assets(f"test/input/Wavi-resources.assets")
        pyI2L.write_output(f"test/output/Wavi.csv", i2, pyI2L.parsers.Wavi.Writer)
        transformed = pyI2L.read_input(f"test/output/Wavi.csv", pyI2L.parsers.Wavi.Reader)
        self.assertEqual(i2, transformed)
        self.assertEqual(i2.to_bytes(), transformed.to_bytes())

if __name__ == '__main__':
    unittest.main()
import tempfile, unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from controltower import run
class ControlTowerTests(unittest.TestCase):
    def test_dataset(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(__file__).resolve().parents[1]
            x=run(p/'data/sample_evidence.csv',d)
            self.assertEqual(x['total_records'],12)
            self.assertEqual(x['ready_for_sample_review'],6)
            self.assertEqual(x['needs_review'],6)
            self.assertTrue((Path(d)/'dashboard.md').exists())
    def test_empty_input(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.csv';p.write_text('foo\nbar\n')
            with self.assertRaises(ValueError):run(p,d)
if __name__=='__main__':unittest.main()

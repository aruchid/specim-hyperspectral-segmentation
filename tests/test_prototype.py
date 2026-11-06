import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import prototype as p
class PrototypeTests(unittest.TestCase):
 def test_reference_recovery(self):
  _,_,metrics=p.demo()
  self.assertTrue(metrics)
 def test_invalid_data(self):
  with self.assertRaises(ValueError):p.finite([float('nan')])
  with self.assertRaises(ValueError):p.finite([])
 def test_reject_invalid_process_input(self):
  with self.assertRaises(ValueError):p.process([[[1,2]]],[[1,2,3],[2,3,4]])

 def test_extreme_spectral_scales_preserve_classes(self):
  import numpy as np
  ends=np.array([[1.,.2],[.2,1.]])
  cube=ends.reshape(1,2,2)
  for scale in (1e-250,1e250):
   with self.subTest(scale=scale):
    np.testing.assert_array_equal(p.process(cube*scale,ends*scale),[[0,1]])

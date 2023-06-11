from sre_constants import ASSERT
import unittest
import pandas as pd
from dataGen.pattern_generator.projection import sine


class base_editor_test(unittest.TestCase):
    # only testing if it does change anything at all...
    def test_sine(self):
        df1 = pd.DataFrame([[1., 1., 1., 1., ], [2., 2., 2., 2.], [
                           3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.]])
        df2 = df1
        df1.iloc[:, 2] = sine.sine(
            df1.iloc[:, 2], 2, 11)
        self.assertFalse(df1.equals(df2))
    # only testing if it does change anything at all...
    # def test_random_walk(self):


if __name__ == "__main__":
    unittest.main()

import unittest
import pandas as pd
import sys
from dataGen.pattern_generator import pattern_generator


class base_editor_test(unittest.TestCase):

    def test_stretch(self):
        df1 = pd.DataFrame(
            [[1., 1., 1., 1., ],  [4., 4., 4., 4.], [7., 7., 7., 7.], ])
        df2 = base_editor.stretch(2.5, df1)
        df3 = pd.DataFrame([[1., 1., 1., 1., ], [2., 2., 2., 2.], [
                           3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.]])
        pd.testing.assert_frame_equal(df2, df3)
        df4 = pd.DataFrame(
            [[1., 1., 1., 1., ],  [2., 2., 2., 2.], [3., 3., 3., 3.], [4., 4., 4., 4.]])
        df5 = base_editor.stretch(0.5, df4)
        df6 = pd.DataFrame([[2., 2., 2., 2., ], [4., 4., 4., 4.]])
        pd.testing.assert_frame_equal(df5, df6)


if __name__ == "__main__":
    unittest.main()

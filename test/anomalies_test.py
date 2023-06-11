import unittest
import pandas as pd
import sys
from dataGen.base_editor import base_editor


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

    def test_concatenate(self):
        df1 = pd.DataFrame([[1., 1., 1., 1., ], [2., 2., 2., 2.], [
                           3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.]])
        df2 = base_editor.concatenate(3, 2, df1)
        df3 = pd.DataFrame([[1., 1., 1., 1., ], [2., 2., 2., 2.], [
                           3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.], [1., 1., 1., 1., ], [2., 2., 2., 2.], [
            3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.], [1., 1., 1., 1., ], [2., 2., 2., 2.], [
            3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.], [1., 1., 1., 1., ], [2., 2., 2., 2.], [
            3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.]])
        pd.testing.assert_frame_equal(df2, df3)

    # cannot test noising cause it is random

    def test_smoothing(self):
        df1 = pd.DataFrame(
            [[1., 1., 1., 1., ],  [4., 4., 4., 4.], [7., 7., 7., 7.], ])
        df2 = base_editor.smooth(2, df1)
        df3 = pd.DataFrame([[3.66528, 3.66528, 3.66528, 3.66528], [
                           4.00000, 4.00000, 4.00000, 4.00000], [4.334718, 4.334718, 4.334718, 4.334718]])
        pd.testing.assert_frame_equal(df2, df3)

    def test_standardize(self):
        df1 = pd.DataFrame(
            [[1., 6., 1., 1., ],  [4., 5., 4., 4.], [7., 4., 7., 7.], ])
        df1.iloc[:, 1] = base_editor.standardize(df1.iloc[:, 1], 4)
        df2 = pd.DataFrame(
            [[1., 5., 1., 1., ],  [4., 4., 4., 4.], [7., 3., 7., 7.], ])

        pd.testing.assert_frame_equal(df1, df2)


if __name__ == "__main__":
    unittest.main()

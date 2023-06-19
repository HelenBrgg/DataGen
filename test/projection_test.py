from sre_constants import ASSERT
import unittest
import pandas as pd
from dataGen.pattern_generator.projection import sine, random_walk


class projection_editor_test(unittest.TestCase):
    # only testing if it does change anything at all...
    # find a sine wave to test for
    def test_sine(self):
        df1 = pd.DataFrame([[1., 1., 1., 1., ], [2., 2., 2., 2.], [
                           3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.], [1., 1., 1., 1., ], [2., 2., 2., 2.], [
            3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.]])
        df2 = pd.DataFrame([[1., 1., 1., 1., ], [2., 2., 2., 2.], [
                           3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.], [1., 1., 1., 1., ], [2., 2., 2., 2.], [
            3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.]])

        df1.iloc[:, 2] = sine.sine(
            df1.iloc[:, 2], 0.1, 10)
        self.assertFalse(df1.equals(df2))

    # only testing if it does change anything at all...
    def test_random_walk(self):
        df1 = pd.DataFrame([[1., 1., 1., 1., ], [2., 2., 2., 2.], [
                           3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.], [1., 1., 1., 1., ], [2., 2., 2., 2.], [
            3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.]])
        df2 = pd.DataFrame([[1., 1., 1., 1., ], [2., 2., 2., 2.], [
                           3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.], [1., 1., 1., 1., ], [2., 2., 2., 2.], [
            3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.]])

        df1.iloc[:, 2] = random_walk.random_walk(
            df1.iloc[:, 2], 0.1, 10)
        self.assertFalse(df1.equals(df2))


if __name__ == "__main__":
    unittest.main()

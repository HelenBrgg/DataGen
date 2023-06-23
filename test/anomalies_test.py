import unittest
import pandas as pd
from dataGen.pattern_generator import anomalies


class anomalies_test(unittest.TestCase):

    def test_square(self):
        df1 = pd.DataFrame(
            [[1., 1., 1., 1., ], [2., 2., 2., 2.], [
                3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.]])
        df1.iloc[:, 2] = df1.iloc[:, 2].replace(
            anomalies.anomalize('square', df1.iloc[:, 2], 4, 1, 9))
        df2 = pd.DataFrame([[1., 1., 1., 1., ], [2., 2., 2., 2.], [
                           3., 3., 3., 3.], [4., 4., 9., 4.], [5., 5., 9., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.]])
        pd.testing.assert_frame_equal(df1, df2)

    def test_anomalize_bell(self):
        df1 = pd.DataFrame(
            [[1., 1., 1., 1., ], [2., 2., 2., 2.], [
                3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.], [8., 8., 8., 8.], [9., 9., 9., 9.], [10., 10., 10., 10]])
        df1.iloc[:, 2] = df1.iloc[:, 2].replace(
            anomalies.anomalize('bell', df1.iloc[:, 2], 4, 1, 9))
        df2 = pd.DataFrame([[1., 1., 1., 1., ], [2., 2., 2., 2.], [
                           3., 3., 3., 3.], [4., 4., 4., 4.], [5., 5., 5., 5.], [6., 6., 6., 6.], [7., 7., 7., 7.], [8., 8., 8., 8.], [9., 9., 9., 9.], [10., 10., 10., 10]])
        self.assertFalse(df1.equals(df2))
        self.assertEquals(df1.iloc[4, 2], 9.)


if __name__ == "__main__":
    unittest.main()

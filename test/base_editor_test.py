import unittest
import pandas as pd
import sys
from dataGen.base_editor import base_editor
#from dg.base_editor import baseeditor


class base_editor_test(unittest.TestCase):

    def test_stretch(self):
        df = pd.DataFrame([[1, 1, 1, 1, 4, 1, 4, 1, 2, 1], [2, 2, 1, 8, 2, 2, 2, 3, 1, 1], [
            1, 8, 1, 1, 5, 1, 3, 1, 1, 1], [1, 3, 1, 5, 4, 8, 2, 1, 3, 1]])

        df = base_editor.stretch(2, df)
        self.assertEquals(1, 1)
    print(sys.path)


if __name__ == "__main__":
    unittest.main()

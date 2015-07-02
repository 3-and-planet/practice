import unittest

class Test(unittest.TestCase):
    def test_it(self):
        import add
        value=add.add(1,1)
        self.assertEqual(2,value)


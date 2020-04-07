import unittest
from library import Reservation


class MyTestCase(unittest.TestCase):
    def test_reservation(self):
        res0 = Reservation(0,10,"book0","user0")
        # check inclusion edges
        self.assertFalse(res0.includes(-1))
        self.assertTrue(res0.includes(0))
        self.assertTrue(res0.includes(5))
        self.assertTrue(res0.includes(10))
        self.assertFalse(res0.includes(11))

        self.assertTrue(res0.overlapping(res0))

        res1 = Reservation(0, 10, "book1", "user0")
        # overlapping only if same book
        self.assertFalse(res0.overlapping(res1))
        self.assertFalse(res1.overlapping(res0))

        res2 = Reservation(11,30,"book0","user1")
        # overlapping only if same book
        self.assertFalse(res0.overlapping(res2))
        self.assertFalse(res2.overlapping(res0))

        res3 = Reservation(5, 15, "book0", "user1")
        self.assertTrue(res0.overlapping(res3))
        self.assertTrue(res3.overlapping(res0))


if __name__ == '__main__':
    unittest.main()

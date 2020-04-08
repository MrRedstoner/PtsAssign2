import unittest
from library import Reservation, Library


class MyTestCase(unittest.TestCase):
    def test_reservation(self):
        res0 = Reservation(0, 10, "book0", "user0")
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

        res2 = Reservation(11, 30, "book0", "user1")
        self.assertFalse(res0.overlapping(res2))
        self.assertFalse(res2.overlapping(res0))

        res3 = Reservation(5, 15, "book0", "user1")
        self.assertTrue(res0.overlapping(res3))
        self.assertTrue(res3.overlapping(res0))

        # check identification cases
        self.assertTrue(res0.identify(5, "book0", "user0"))
        self.assertFalse(res0.identify(-1, "book0", "user0"))
        self.assertFalse(res0.identify(11, "book0", "user0"))
        self.assertFalse(res0.identify(5, "book1", "user0"))
        self.assertFalse(res0.identify(5, "book0", "user1"))

        # check user changing
        self.assertTrue(res0.identify(5, "book0", "user0"))
        res0.change_for("user1")
        self.assertTrue(res0.identify(5, "book0", "user1"))
        self.assertFalse(res0.identify(5, "book0", "user0"))

    def test_library(self):
        lib = Library()
        # add some users
        self.assertTrue(lib.add_user("user0"))
        self.assertFalse(lib.add_user("user0"))
        self.assertTrue(lib.add_user("user1"))
        # add some books
        lib.add_book("book0")
        lib.add_book("book0")
        lib.add_book("book1")
        lib.add_book("book2")

        # try basic checkouts
        self.assertFalse(lib.check_reservation("user0", "book0", 5))
        self.assertTrue(lib.reserve_book("user0", "book0", 0, 10))
        self.assertTrue(lib.check_reservation("user0", "book0", 5))
        self.assertFalse(lib.check_reservation("user1", "book0", 5))
        self.assertTrue(lib.reserve_book("user1", "book0", 0, 10))
        self.assertTrue(lib.check_reservation("user1", "book0", 5))
        self.assertFalse(lib.check_reservation("user0", "book1", 5))
        self.assertTrue(lib.reserve_book("user0", "book1", 0, 10))
        self.assertTrue(lib.check_reservation("user0", "book1", 5))
        # check failure options
        self.assertFalse(lib.reserve_book("nonexistent", "book2", 0, 1))
        self.assertFalse(lib.reserve_book("user0", "no_book", 0, 1))
        self.assertFalse(lib.reserve_book("user0", "book2", 10, 0))
        self.assertFalse(lib.reserve_book("user0", "book0", 0, 1))

        # try reservation change
        self.assertTrue(lib.check_reservation("user0", "book1", 5))
        self.assertTrue(lib.change_reservation("user0", "book1", 5, "user1"))
        self.assertTrue(lib.check_reservation("user1", "book1", 5))
        self.assertFalse(lib.check_reservation("user0", "book1", 5))
        # try failure options
        self.assertFalse(lib.change_reservation("nonexistent", "book1", 5, "user0"))
        self.assertFalse(lib.change_reservation("user1", "book1", 5, "nonexistent"))
        self.assertFalse(lib.change_reservation("user1", "no book", 5, "user0"))
        self.assertFalse(lib.change_reservation("user1", "book1", 100, "user0"))
        self.assertFalse(lib.change_reservation("user1", "book1", -10, "user0"))


if __name__ == '__main__':
    unittest.main()

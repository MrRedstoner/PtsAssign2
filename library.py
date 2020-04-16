from __future__ import annotations
from itertools import count
import logging


class StringBuilder:
    @staticmethod
    def create_reservation(reservation_id: int, book: str, from_: int, to: int, for_: str) -> str:
        return F'Created a reservation with id {reservation_id} of {book} from {from_} to {to} for {for_}.'

    @staticmethod
    def reservation_overlap(r0_id: int, r1_id: int) -> str:
        return F'Reservations {r0_id} and {r1_id} do overlap'

    @staticmethod
    def reservation_no_overlap(r0_id: int, r1_id: int) -> str:
        return F'Reservations {r0_id} and {r1_id} do not overlap'

    @staticmethod
    def reservation_includes(reservation_id: int, date: int) -> str:
        return F'Reservation {reservation_id} includes {date}'

    @staticmethod
    def reservation_no_include(reservation_id: int, date: int) -> str:
        return F'Reservation {reservation_id} does not include {date}'

    @staticmethod
    def wrong_book(reservation_id: int, book: str, other_book: str) -> str:
        return F'Reservation {reservation_id} reserves {book} not {other_book}.'

    @staticmethod
    def wrong_for(reservation_id: int, for_: int, other_for: int) -> str:
        return F'Reservation {reservation_id} is for {for_} not {other_for}.'

    @staticmethod
    def date_outside_range(reservation_id: int, from_: int, to: int, date: int) -> str:
        return F'Reservation {reservation_id} is from {from_} to {to} which does not include {date}.'

    @staticmethod
    def reservation_is_valid(reservation_id: int, for_: int, book: str, date: int) -> str:
        return F'Reservation {reservation_id} is valid {for_} of {book} on {date}.'

    @staticmethod
    def reservation_changed(reservation_id: int, for_: str, new_for: str) -> str:
        return F'Reservation {reservation_id} moved from {for_} to {new_for}'

    @staticmethod
    def library_created() -> str:
        return 'Library created.'

    @staticmethod
    def user_already_exists(name: str) -> str:
        return F'User not created, user with name {name} already exists.'

    @staticmethod
    def user_created(name: str) -> str:
        return F'User {name} created.'

    @staticmethod
    def book_added(name: str, number: int) -> str:
        return F'Book {name} added. We have {number} copies of the book.'

    @staticmethod
    def missing_user(book: str, name: str, from_: int, to: int) -> str:
        return F'We cannot reserve book {book} for {name} from {from_} to {to}. User does not exist.'

    @staticmethod
    def missing_book(book: str, name: str, from_: int, to: int) -> str:
        return F'We cannot reserve book {book} for {name} from {from_} to {to}. We do not have that book.'

    @staticmethod
    def wrong_dates(book: str, name: str, from_: int, to: int) -> str:
        return F'We cannot reserve book {book} for {name} from {from_} to {to}. Incorrect dates.'

    @staticmethod
    def not_enough_books(book: str, name: str, from_: int, to: int) -> str:
        return F'We cannot reserve book {book} for {name} from {from_} to {to}. We do not have enough books.'

    @staticmethod
    def reservation_included(reservation_id: int) -> str:
        return F'Reservation {reservation_id} included.'

    @staticmethod
    def user_reservation_exists(name: str, book: str, date: int) -> str:
        return F'Reservation for {name} of {book} on {date} exists.'

    @staticmethod
    def user_reservation_no_exist(name: str, book: str, date: int) -> str:
        return F'Reservation for {name} of {book} on {date} does not exist.'

    @staticmethod
    def reservation_user_does_not_exist(name: str) -> str:
        return F'Cannot change the reservation as {name} does not exist.'

    @staticmethod
    def reservation_changed_user(user_from: str, new_user: str, book: str, date: int):
        return F'Reservation for {user_from} of {book} on {date} changed to {new_user}.'


def get_string_builder():
    return StringBuilder()


class Reservation(object):
    _ids = count(0)

    _string_builder = get_string_builder()

    def __init__(self, from_, to, book, for_):
        self._id = next(Reservation._ids)
        self._from = from_
        self._to = to
        self._book = book
        self._for = for_
        self._changes = 0
        logging.info(Reservation._string_builder.
                     create_reservation(self._id, self._book, self._from, self._to, self._for))

    def overlapping(self, other: Reservation):
        ret = (self._book == other._book and self._to >= other._from
               and self._from <= other._to)
        if ret:
            logging.debug(Reservation._string_builder.reservation_overlap(self._id, other._id))
        else:
            logging.debug(Reservation._string_builder.reservation_no_overlap(self._id, other._id))
        return ret

    def includes(self, date):
        ret = (self._from <= date <= self._to)
        if ret:
            logging.debug(Reservation._string_builder.reservation_includes(self._id, date))
        else:
            logging.debug(Reservation._string_builder.reservation_no_include(self._id, date))
        return ret

    def identify(self, date, book, for_):
        if book != self._book:
            logging.debug(Reservation._string_builder.wrong_book(self._id, self._book, book))
            return False
        if for_ != self._for:
            logging.debug(Reservation._string_builder.wrong_for(self._id, self._for, for_))
            return False
        if not self.includes(date):
            logging.debug(Reservation._string_builder.date_outside_range(self._id, self._from, self._to, date))
            return False
        logging.debug(Reservation._string_builder.reservation_is_valid(self._id, for_, book, date))
        return True

    def change_for(self, for_):
        logging.info(Reservation._string_builder.reservation_changed(self._id, self._for, for_))
        self._for = for_


class Library(object):
    _string_builder = get_string_builder()

    def __init__(self):
        self._users = set()
        self._books = {}  # maps name to count
        self._reservations = []  # Reservations sorted by from
        logging.info(Library._string_builder.library_created())

    def add_user(self, name):
        if name in self._users:
            logging.warning(Library._string_builder.user_already_exists(name))
            return False
        self._users.add(name)
        logging.info(Library._string_builder.user_created(name))
        return True

    def add_book(self, name):
        self._books[name] = self._books.get(name, 0) + 1
        logging.info(Library._string_builder.book_added(name, self._books[name]))

    def reserve_book(self, user, book, date_from, date_to):
        book_count = self._books.get(book, 0)
        if user not in self._users:
            logging.warning(Library._string_builder.missing_user(book, user, date_from, date_to))
            return False
        if date_from > date_to:
            logging.warning(Library._string_builder.wrong_dates(book, user, date_from, date_to))
            return False
        if book_count == 0:
            logging.warning(Library._string_builder.missing_book(book, user, date_from, date_to))
            return False
        desired_reservation = Reservation(date_from, date_to, book, user)
        relevant_reservations = [res for res in self._reservations
                                 if desired_reservation.overlapping(res)] + [desired_reservation]
        # we check that if we add this reservation then for every reservation record that starts
        # between date_from and date_to no more than book_count books are reserved.
        for from_ in [res._from for res in relevant_reservations]:
            if desired_reservation.includes(from_):
                if sum([rec.includes(from_) for rec in relevant_reservations]) > book_count:
                    logging.warning(Library._string_builder.not_enough_books(book, user, date_from, date_to))
                    return False
        self._reservations += [desired_reservation]
        self._reservations.sort(key=lambda x: x._from)  # to lazy to make a getter
        logging.debug(Library._string_builder.reservation_included(desired_reservation._id))
        return True

    def check_reservation(self, user, book, date):
        res = any([res.identify(date, book, user) for res in self._reservations])
        if res:
            logging.debug(Library._string_builder.user_reservation_exists(user, book, date))
        else:
            logging.debug(Library._string_builder.user_reservation_no_exist(user, book, date))
        return res

    def change_reservation(self, user, book, date, new_user):
        relevant_reservations = [res for res in self._reservations
                                 if res.identify(date, book, user)]
        if not relevant_reservations:
            logging.warning(Library._string_builder.user_reservation_no_exist(user, book, date))
            return False
        if new_user not in self._users:
            logging.warning(Library._string_builder.reservation_user_does_not_exist(new_user))
            return False

        logging.info(Library._string_builder.reservation_changed_user(user, new_user, book, date))
        relevant_reservations[0].change_for(new_user)
        return True

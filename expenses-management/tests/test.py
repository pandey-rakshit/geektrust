import unittest
from src.house import House
from src.member import Member
from src.utils.helper import DuesManager
from constants import Status, Config


class TestHouse(unittest.TestCase):

    def setUp(self):
        self.house = House()

    def test_move_in_success(self):
        result = self.house.move_in("Alice")
        self.assertEqual(result, Status.SUCCESS)
        self.assertIn("Alice", self.house.members)

    def test_move_in_houseful(self):
        for i in range(Config.MAX_MEMBERS):
            self.house.move_in(f"Member{i+1}")
        result = self.house.move_in("ExtraMember")
        self.assertEqual(result, Status.HOUSEFUL)

    def test_move_out_success(self):
        self.house.move_in("Alice")
        result = self.house.move_out("Alice")
        self.assertEqual(result, Status.SUCCESS)
        self.assertNotIn("Alice", self.house.members)

    def test_move_out_failure_due_to_outstanding_dues(self):
        self.house.move_in("Alice")
        self.house.move_in("Bob")
        self.house.spend(100, "Alice", ["Bob"])
        result = self.house.move_out("Alice")
        self.assertEqual(result, Status.FAILURE)

    def test_spend_success(self):
        self.house.move_in("Alice")
        self.house.move_in("Bob")
        result = self.house.spend(100, "Alice", ["Bob"])
        self.assertEqual(result, Status.SUCCESS)
        self.assertEqual(self.house.members["Bob"].dues["Alice"], 50)

    def test_spend_member_not_found(self):
        result = self.house.spend(100, "NonExistent", ["Bob"])
        self.assertEqual(result, Status.MEMBER_NOT_FOUND)

    def test_clear_dues_success(self):
        self.house.move_in("Alice")
        self.house.move_in("Bob")
        self.house.spend(100, "Alice", ["Bob"])
        result = self.house.clear_dues("Bob", "Alice", 50)
        self.assertEqual(result, 0)
        self.assertNotIn("Alice", self.house.members["Bob"].get_dues())

    def test_clear_dues_incorrect_payment(self):
        self.house.move_in("Alice")
        self.house.move_in("Bob")
        result = self.house.clear_dues("Bob", "Alice", 50)
        self.assertEqual(result, Status.INCORRECT_PAYMENT)

    def test_dues(self):
        self.house.move_in("Alice")
        self.house.move_in("Bob")
        self.house.spend(100, "Alice", ["Bob"])
        result = self.house.dues("Bob")
        expected = [("Alice", 50)]
        self.assertEqual(result, expected)


class TestDuesManager(unittest.TestCase):

    def setUp(self):
        self.members = {"Alice": Member("Alice"), "Bob": Member("Bob")}

    def test_clear_dues_success(self):
        self.members["Bob"].add_due("Alice", 50)
        result = DuesManager.clear_dues(self.members, "Bob", "Alice", 50)
        self.assertEqual(result, 0)
        self.assertNotIn("Alice", self.members["Bob"].get_dues())

    def test_clear_dues_incorrect_payment(self):
        result = DuesManager.clear_dues(self.members, "Bob", "Alice", 50)
        self.assertEqual(result, Status.INCORRECT_PAYMENT)

    def test_create_lender_to_borrowers_dict(self):
        self.members["Bob"].add_due("Alice", 50)
        result = DuesManager.create_lender_to_borrowers_dict(self.members)
        expected = {"Alice": {"Bob": 50}}
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()

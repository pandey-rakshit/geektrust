from constants import Status


class Member:
    def __init__(self, name):
        self.name = name
        self.dues = {}

    def add_due(self, other_member, amount):
        self.dues[other_member] = self.dues.get(other_member, 0) + amount

    def clear_due(self, other_member, amount):
        if other_member not in self.dues:
            return Status.INCORRECT_PAYMENT

        if self.dues[other_member] < amount:
            return Status.INCORRECT_PAYMENT

        self.dues[other_member] -= amount

        if self.dues[other_member] == 0:
            del self.dues[other_member]

        return self.dues.get(other_member, 0)

    def get_dues(self):
        return self.dues

from constants import Config, Status
from .member import Member
from .utils.helper import DuesManager


class House:
    def __init__(self):
        self.members = {}

    def is_house_full(self):
        return len(self.members) >= Config.MAX_MEMBERS

    def move_in(self, member_name):
        if self.is_house_full():
            return Status.HOUSEFUL

        self.members[member_name] = Member(member_name)
        return Status.SUCCESS

    def move_out(self, member_name):
        if member_name not in self.members:
            return Status.MEMBER_NOT_FOUND

        if self._has_outstanding_dues(member_name):
            return Status.FAILURE

        del self.members[member_name]
        return Status.SUCCESS

    def spend(self, amount, spent_by, spent_for):
        if not self._members_exist([spent_by] + spent_for):
            return Status.MEMBER_NOT_FOUND

        per_person_amount = amount // (len(spent_for) + 1)
        lender_to_borrowers_dict = DuesManager.create_lender_to_borrowers_dict(
            self.members
        )

        if lender_to_borrowers_dict:
            lender_dues = self.members[spent_by].get_dues()
            common_members = set(lender_dues.keys()).intersection(spent_for)
            return DuesManager.settle_dues(
                spent_by,
                spent_for,
                per_person_amount,
                common_members,
                lender_dues,
                self.members,
            )

        self._distribute_dues(spent_by, spent_for, per_person_amount)
        return Status.SUCCESS

    def _members_exist(self, member_names):
        return all(member in self.members for member in member_names)

    def _has_outstanding_dues(self, member_name):
        dues = self.members[member_name].get_dues()
        lender_to_borrower_dict = DuesManager.create_lender_to_borrowers_dict(
            self.members
        )
        member_lending_dict = lender_to_borrower_dict.get(member_name, {})
        return any(dues.values()) or any(member_lending_dict.values())

    def _distribute_dues(self, spent_by, spent_for, per_person_amount):
        for borrower in spent_for:
            self.members[borrower].add_due(spent_by, per_person_amount)

    def dues(self, member_name):
        if member_name not in self.members:
            return Status.MEMBER_NOT_FOUND

        dues_dict = self._get_dues_dict(member_name)
        return sorted(dues_dict.items(), key=lambda item: (-item[1], item[0]))

    def _get_dues_dict(self, member_name):
        all_members = list(self.members.keys())
        dues = self.members[member_name].get_dues()
        return {
            other_member: dues.get(other_member, 0)
            for other_member in all_members
            if other_member != member_name
        }

    def clear_dues(self, member_who_owes, member_who_lent, amount):
        if not self._members_exist([member_who_owes, member_who_lent]):
            return Status.MEMBER_NOT_FOUND

        if member_who_owes == member_who_lent:
            return Status.FAILURE

        return DuesManager.clear_dues(
            self.members, member_who_owes, member_who_lent, amount
        )

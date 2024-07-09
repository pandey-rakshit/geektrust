from constants import Status


class DuesManager:
    @staticmethod
    def process_lended_by_borrower(
        spent_by, borrower, amount, lended_by_borrower, members
    ):
        for member, due in list(lended_by_borrower.items()):
            DuesManager.update_dues(spent_by, borrower, member, amount, due, members)

    @staticmethod
    def update_dues(spent_by, borrower, member, amount, due, members):
        if amount <= due:
            DuesManager.clear_dues(members, member, borrower, amount)
            members[member].add_due(spent_by, amount)
            members[borrower].add_due(spent_by, due - amount)
        else:
            DuesManager.clear_dues(members, member, borrower, due)
            members[member].add_due(spent_by, due)
            members[borrower].add_due(spent_by, amount - due)

    @staticmethod
    def handle_no_dues(spent_by, borrower, share, members):
        lender_to_borrowers_dict = DuesManager.create_lender_to_borrowers_dict(
            members, borrower
        )
        lended_by_borrower = lender_to_borrowers_dict.get(borrower, {})
        DuesManager.process_lended_by_borrower(
            spent_by, borrower, share, lended_by_borrower, members
        )
        if not lended_by_borrower:
            members[borrower].add_due(spent_by, share)

    @staticmethod
    def adjust_remaining_amount(spent_by, borrower, remaining_amount, members):
        lender_to_borrowers_dict = DuesManager.create_lender_to_borrowers_dict(
            members, borrower
        )
        lended_by_borrower = lender_to_borrowers_dict.get(borrower, {})
        DuesManager.process_lended_by_borrower(
            spent_by, borrower, remaining_amount, lended_by_borrower, members
        )

    @staticmethod
    def handle_existing_dues(spent_by, borrower, share, members):
        amount = members[spent_by].get_dues().get(borrower, 0)
        if share <= amount:
            DuesManager.clear_dues(members, spent_by, borrower, share)
        else:
            DuesManager.clear_dues(members, spent_by, borrower, amount)
            remaining_amount = share - amount
            DuesManager.adjust_remaining_amount(
                spent_by, borrower, remaining_amount, members
            )

    @staticmethod
    def settle_dues(spent_by, spent_for, share, common_members, lender_dues, members):
        if common_members:
            for borrower in spent_for:
                if borrower in common_members:
                    DuesManager.handle_existing_dues(spent_by, borrower, share, members)
                else:
                    DuesManager.handle_no_dues(spent_by, borrower, share, members)
        else:
            for borrower in spent_for:
                for lender, amount in list(lender_dues.items()):
                    if share <= amount:
                        DuesManager.clear_dues(members, spent_by, lender, share)
                        members[borrower].add_due(lender, share)
                    else:
                        DuesManager.clear_dues(members, spent_by, lender, amount)
                        members[borrower].add_due(lender, amount)
                        remaining_amount = share - amount
                        members[borrower].add_due(spent_by, remaining_amount)

        return Status.SUCCESS

    @staticmethod
    def clear_dues(members, member_who_owes, member_who_lent, amount):
        dues = members[member_who_owes].get_dues().get(member_who_lent, 0)
        if amount > dues:
            return Status.INCORRECT_PAYMENT
        return members[member_who_owes].clear_due(member_who_lent, amount)

    @staticmethod
    def create_lender_to_borrowers_dict(members, member_name=None):
        lender_to_borrowers_dict = {}
        for member_name, member in members.items():
            for other_member, amount in member.get_dues().items():
                if amount > 0:
                    lender_to_borrowers_dict.setdefault(other_member, {})[
                        member_name
                    ] = amount
        return lender_to_borrowers_dict

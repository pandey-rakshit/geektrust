from src.house import House
from constants import Commands, Status


class ExpensesManagement:
    def __init__(self):
        self.House = House()
        self.methods = {
            Commands.MOVE_IN: self.handle_move_in,
            Commands.SPEND: self.handle_spend,
            Commands.DUES: self.handle_dues,
            Commands.CLEAR_DUE: self.handle_clear_due,
            Commands.MOVE_OUT: self.handle_move_out,
        }

    def process_commands(self, commands):
        for command in commands:
            # Split the command into action and arguments
            parts = command.split()
            action = parts[0]
            args = parts[1:]

            if action in self.methods:
                if action == Commands.SPEND:
                    amount = int(args[0])
                    spent_by = args[1]
                    spent_for = args[2:]
                    result = self.methods[action](amount, spent_by, spent_for)

                elif action == Commands.CLEAR_DUE:
                    member_who_owes = args[0]
                    member_who_lent = args[1]
                    amount = int(args[2])
                    result = self.methods[action](
                        member_who_owes, member_who_lent, amount
                    )

                else:
                    result = self.methods[action](*args)

                if action == Commands.DUES:
                    if isinstance(result, list):
                        for member, amount in result:
                            print(f"{member} {amount}")
                    else:
                        print(result)
                else:
                    print(result)

            else:
                print(f"{Status.INVALID_COMMAND}: {command}")

    def handle_move_in(self, member_name):
        return self.House.move_in(member_name)

    def handle_spend(self, amount, spent_by, spent_for):
        return self.House.spend(amount, spent_by, spent_for)

    def handle_dues(self, member_name):
        return self.House.dues(member_name)

    def handle_clear_due(self, member_owes, member_lent, amount):
        return self.House.clear_dues(member_owes, member_lent, amount)

    def handle_move_out(self, member_name):
        return self.House.move_out(member_name)

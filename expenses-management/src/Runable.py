from .Constants import ExpenseConstants
from .Member import Member
from .House import House
from .Calculator import ExpenseCalculator

class Runnable:
  def __init__(self):
    self.house = House()
    self.ec = ExpenseCalculator(self.house)

  def find_Member(self, member_names):
    if type(member_names) == str:
      if member_names in self.house.rooms.keys():
        return self.house.rooms[member_names]
    else:
      member_arr = []
      for member in member_names:
        if member in self.house.rooms.keys():
          member_arr.append(self.house.rooms[member])
      return member_arr

  def process_commands(self, lines):
    for commands in lines:
      command = commands.strip().split(' ')
      if command[0] == ExpenseConstants.MOVE_IN:
        name = command[1]
        member = Member(name)
        result = self.house.MOVE_IN(member)
        print(result)

      elif command[0] == ExpenseConstants.SPEND:
        amount = int(command[1])
        spent_by = self.find_Member(command[2])
        spent_on = self.find_Member(command[3:])
        result = self.ec.SPEND(amount=amount, spent_by=spent_by, spent_on=spent_on)
        print(result)

      elif command[0] == ExpenseConstants.DUES:
        member = self.find_Member(command[1])
        result = self.ec.DUES(member)
        if type(result) == str:
          print(result)
        else:
          for name, due in result:
            print(name, due)

      elif command[0] == ExpenseConstants.CLEAR_DUE:
        borrower = self.find_Member(command[1])
        lender = self.find_Member(command[2])
        amount = int(command[3])
        result = self.ec.CLEAR_DUE(borrower=borrower, lender=lender, amount=amount)
        print(result)

      elif command[0] == ExpenseConstants.MOVE_OUT:
        roomie = self.find_Member(command[1])
        result = self.house.MOVE_OUT(roomie)
        print(result)

      else:
        print(ExpenseConstants.FAILURE)
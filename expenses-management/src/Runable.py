from .Constants import ExpenseConstants
from .Member import Member
from .House import House
from .Calculator import ExpenseCalculator

class Runnable:
  def __init__(self):
    self.house = House()
    self.ec = ExpenseCalculator(self.house)

  def find_Member(self, member_names, filter_name=None):
    if type(member_names) == str:
      if member_names in self.house.rooms.keys():
        return self.house.rooms[member_names]
      raise Exception(ExpenseConstants.MEMBER_NOT_FOUND)
    else:
      member_arr = []
      for member in member_names:
        if filter_name == member:
          continue
        elif member in self.house.rooms.keys():
          member_arr.append(self.house.rooms[member])
      return member_arr

  def process_commands(self, lines):
    for commands in lines:
      command = commands.strip().split(' ')
      if command[0] == ExpenseConstants.MOVE_IN:
        try:
          name = command[1]
          member = Member(name)
          result = self.house.MOVE_IN(member)
          print(result)
        except Exception as e:
          print(e)

      elif command[0] == ExpenseConstants.SPEND:
        try:
          amount = int(command[1])
          spent_by = self.find_Member(command[2])
          spent_on = self.find_Member(command[3:], command[2])
          if len(spent_on) > 0: 
            result = self.ec.SPEND(amount=amount, spent_by=spent_by, spent_on=spent_on)
            print(result)
          else:
            raise Exception(ExpenseConstants.MEMBER_NOT_FOUND)
        except Exception as e:
          print(e)

      elif command[0] == ExpenseConstants.DUES:
        try:
          member = self.find_Member(command[1])
          result = self.ec.DUES(member)
          for name, due in result:
            print(name, due)
        except Exception as e:
          print(e)

      elif command[0] == ExpenseConstants.CLEAR_DUE:
        try:
          borrower = self.find_Member(command[1])
          lender = self.find_Member(command[2])
          amount = int(command[3])
          result = self.ec.CLEAR_DUE(borrower=borrower, lender=lender, amount=amount)
          print(result)
        except Exception as e:
          print(e)

      elif command[0] == ExpenseConstants.MOVE_OUT:
        try:
          roomie = self.find_Member(command[1])
          result = self.house.MOVE_OUT(roomie)
          print(result)
        except Exception as e:
          print(e)

      else:
        print(ExpenseConstants.FAILURE)
      
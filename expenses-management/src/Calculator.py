from .Constants import ExpenseConstants as ec
class ExpenseCalculator:
  def __init__(self, house):
    self.house = house

  def SPEND(self, amount, spent_by, spent_on):
    if len(spent_on)  > 0 and spent_by:
      share = int(amount / (len(spent_on) + 1))
      my_dues = spent_by.dues.items()
      if len(my_dues) == 0:
        for member in spent_on:
          member.add_dues(share, spent_by)
      else:
        for due_owner, due_amount in my_dues:
          due_owner = self.house.rooms[due_owner]
          for member in spent_on:
            if due_amount >= share:
              spent_by.clear_dues(share, due_owner)
              member.add_dues(share, due_owner)
            else:
              spent_by.clear_dues(due_amount, due_owner)
              member.add_dues(share - due_amount, spent_by)
              member.add_dues(due_amount, due_owner)
      return ec.SUCCESS
    return ec.MEMBER_NOT_FOUND

  def DUES(self, member):
    if member:
      result = member.dues
      room = self.house.rooms
      for m in room.values():
        name = m.name
        if name not in result.keys() and name != member.name:
          result[m.name] = 0
      return sorted(result.items(), key=lambda item: (-item[1], item[0]))
    return ec.MEMBER_NOT_FOUND

  def CLEAR_DUE(self, borrower, lender, amount):
    if lender and borrower:
      result = borrower.clear_dues(amount, lender)
      return result
    return ec.MEMBER_NOT_FOUND
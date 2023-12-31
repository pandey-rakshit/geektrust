from .Constants import ExpenseConstants as ec
class House:
  def __init__(self):
    self.rooms = {}
    self.space = 3

  def owes(self, lender):
    owes = False
    for _, borrower in self.rooms.items():
      if borrower.name != lender.name:
        if borrower.dues and borrower.dues.get(lender.name) > 0:
          owes = True
          break
    return owes

  def MOVE_IN(self, member):
    if self.space > 0:
      self.rooms[member.name] = member
      self.space -= 1
      return ec.SUCCESS
    return ec.HOUSEFUL
  
  def MOVE_OUT(self, member):
    if member and member.name in self.rooms.keys():
      owes = self.owes(member)
      dues_list = list(filter(lambda x: x > 0, member.dues.values()))
      if len(dues_list) == 0 and not owes:
        del self.rooms[member.name]
        self.space += 1
        return ec.SUCCESS
      return ec.FAILURE
    return ec.MEMBER_NOT_FOUND
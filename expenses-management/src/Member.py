from .Constants import ExpenseConstants as ec

class Member:
  def __init__(self, name):
    self.name = name
    self.dues = {}

  def __eq__(self, other):
    if isinstance(other, Member):
      return self.name == other.name
    return False

  def add_dues(self, amount, member):
    if member.name not in self.dues.keys():
      self.dues[member.name] = amount
    else:
      self.dues[member.name] += amount
  
  def clear_dues(self, amount, lender):
    if lender.name in self.dues.keys():
      if self.dues[lender.name] >= amount:
        self.dues[lender.name] -= amount
        return self.dues[lender.name]
      return ec.INCORRECT_PAYMENT

  
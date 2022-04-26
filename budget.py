class Category:
  def __init__ (self,category_name):
    self.ledger = []
    self.category=category_name

  def deposit(self,amount,desc = ""):
    self.ledger.append({"amount":amount,"description":desc})

  def withdraw(self,amount,desc = ""):
    if self.check_funds(amount):
      self.ledger.append({"amount":(amount * -1),"description":desc})
      return True
    return False

  def get_balance(self,):
    return sum(entry['amount'] for entry in self.ledger)

  def transfer(self,amount,budget):
    if self.withdraw(amount,"Transfer to " + budget.category):
      budget.deposit(amount,"Transfer from " + self.category)
      return True
    return False

  def check_funds(self,amount):
    return True if self.get_balance() >= amount else False

  def __repr__(self):
    num_l_stars = 15 - len(self.category)//2
    num_r_stars = 30 - num_l_stars - len(self.category)
    txt = ('*' * num_l_stars) + self.category + ('*' * num_r_stars + '\n')
    for entry in self.ledger:
      txt += (entry['description'] + (' ' * 30))[:23]
      txt += ((' ' * 7) + '{:.2f}'.format(entry['amount']))[-7:]
      txt += '\n'
    txt += "Total: " + '{:.2f}'.format(self.get_balance())
    return txt

  def withdrawn_total(self):
    return round(sum(entry['amount'] for entry in self.ledger if entry['amount'] < 0),2)

def create_spend_chart(categories):
  wd = [{"budget":budget.category,"withdrawn":budget.withdrawn_total()} for budget in categories]
  total_wd = sum(budget['withdrawn'] for budget in wd)
  max_desc_len = 0
  for w in wd:
    w['proportion'] = (10 * w['withdrawn'] // total_wd) * 10
    if len(w['budget'])> max_desc_len:
      max_desc_len = len(w['budget'])
  txt = "Percentage spent by category\n"
  for i in range(100,-1,-10):
    txt+= ("  " + str(i))[-3:] + "|"
    for w in wd:
      txt+= ' o ' if w['proportion'] >= i else '   '
    txt+=' \n'
  txt += '    ' + ('-' * (3 * len(wd) + 1)) + '\n'
  for i in range (max_desc_len):
    txt += (' ' * 4)
    for w in wd:
      c = w['budget'][i:i+1]
      txt += ' ' + c + ' '
      if len(c) < 1:
        txt+= ' '
    txt += ' \n'
  return txt[:-1]
    
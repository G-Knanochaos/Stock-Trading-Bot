def average(lst):
  total = 0
  for l in lst:
    total += l
  return total/len(lst)

def CleanList(lst):
  lst2 = []
  for item in lst:
    if item in lst2:
      lst2.append(item)
  lst = lst2

def isSupport(df,i,layers,stat):
  lst = []
  stat = df[stat]
  '''
  for x in range(1,layers+1):
    lst.append(stat[i-(x-1)] < stat[i-x])
    lst.append(stat[i+(x-1)] < stat[i+x])
  '''
  #'''
  for x in range(1,layers+1):
    lst.append(stat[i] < stat[i-x])
    lst.append(stat[i] < stat[i+x])
  #'''
  return sum(lst) == layers*2
def isResistance(df,i,layers,stat):
  lst = []
  stat = df[stat]
  '''
  for x in range(1,layers+1):
    lst.append(stat[i-(x-1)] > stat[i-x])
    lst.append(stat[i+(x-1)] > stat[i+x])
  '''
  #'''
  for x in range(1,layers+1):
    lst.append(stat[i] > stat[i-x])
    lst.append(stat[i] > stat[i+x])
  #'''
  return sum(lst) == layers*2


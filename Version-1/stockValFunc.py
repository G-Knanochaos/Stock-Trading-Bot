def isSupport(df,i,layers,stat):
  lst = []
  stat = df[stat]
  for x in range(1,layers+1):
    lst.append(stat[i] < stat[i-x])
    lst.append(stat[i] < stat[i+x])
  return sum(lst) == layers*2
def isResistance(df,i,layers,stat):
  lst = []
  stat = df[stat]
  for x in range(1,layers+1):
    lst.append(stat[i] > stat[i-x])
    lst.append(stat[i] > stat[i+x])
  return sum(lst) == layers*2

def average(lst):
  total = 0
  for l in lst:
    total += l
  return total/len(lst)



















'''
levels = []
  point = None
  go = True
  average = 0
  l_average = 0
  h_average = 0
  for i in range(df.shape[0]-3,df.shape[0]-daylen,-1):
    average += (abs(df['Close'][i]-df['Close'][i-1])/price)
    l_average += ((df['Low'][i]-df['Close'][i-1])/price)
    h_average += ((df['High'][i]-df['Close'][i-1])/price)
    if go:
      if isSupport(df,i,1,'Low'):
        l = round(df['Low'][i],3)
        point = l
        go = False
      elif isResistance(df,i,1,'High'):
        h = round(df['High'][i],3)
        point = h
        go = False

  for i in range(df.shape[0]-4,df.shape[0]-daylen,-1):
    if isSupport(df,i,1,'Low'):
      if isSupport(df,i,2,'Low'):
        if isSupport(df,i,3,'Low'):
          l = round(df['Low'][i],3)
          if isFarFromLevel(l,'s'):
            levels.append([i,l,1,'s'])
    elif isResistance(df,i,1,'High'):
      if isResistance(df,i,2,'High'):
        if isResistance(df,i,3,'High'):
          h = round(df['High'][i],3)
          if isFarFromLevel(h,'r'):
            levels.append([i,h,1,'r'])
            
  #price > points[0] can return True or False
  t_daylen = daylen/2 #true daylen       
  for a in (average, l_average, h_average):
      a = (a/t_daylen)*100
'''


x = 7
y = 6

row = 6
col = 6

future_row = 5
future_col = 6


positionlist = [(0,1), (-1,0), (0,-1), (1,0)] #draaiing

currentrow = x - row
currentcol = y - col

current = (currentrow, currentcol)
currentindex = positionlist.index(current)

newposrow = future_row - row
newposcol = future_col - col

newpos = (newposrow, newposcol)
newposindex= positionlist.index(newpos)

print(currentindex, newposindex)

steps = abs(newposindex - currentindex)
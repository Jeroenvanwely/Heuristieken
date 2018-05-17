
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

# if future_row > row:
        #     # verander de eerstvolgende en dan pas de rest in een loop met de translatie van de vorige
        #     self.p_list[x].row = future_row#+1
        #     self.p_list[x].column = future_col
        #     count = 0
        #     for i in range(x, len(self.p_list)-1):
        #         steps = abs(newposindex - currentindex)


        #         #print(self.p_list[i].row, self.p_list[i].col, self.p_list[i].rotation_row, self.p_list[i].rotation_col)
        #         # self.p_list[i].row += self.p_list[i].rotation_col # Maar dan alleen de eerste element
        #         # self.p_list[i].column += self.p_list[i].rotation_row # en dan alleen de tweede
                
        #         # if count%2 == 0:
        #         #     self.p_list[i].row = (self.p_list[i-1] - self.p_list[i].rotation_col)
        #         #     self.p_list[i].column = (self.p_list[i-1] - self.p_list[i].rotation_row)
        #         #     count+= 1
        #         # else:
        #         #     self.p_list[i].row -= (self.p_list[i-1] + self.p_list[i].rotation_col)
        #         #     self.p_list[i].column -= (self.p_list[i-1] + self.p_list[i].rotation_row)
        #         #     count += 1

        #         # self.p_list[i].row += (1 + self.p_list[i].rotation_row) 
        #         # self.p_list[i].column += (1 + self.p_list[i].rotation_col)





        # elif future_row < row and self.p_list[x-1].row == self.p_list[x].row:
        #     self.p_list[x].row = future_row-1
        #     self.p_list[x].column = future_col
        #     count = 0
        #     for i in range(0, len(self.p_list)):
        #         self.p_list[i].row += self.p_list[i].rotation_col # Maar dan alleen de eerste element
        #         self.p_list[i].column += self.p_list[i].rotation_row
                
        #         if count%2 == 0:
        #             self.p_list[i].row -= self.p_list[i].rotation_col
        #             self.p_list[i].column -= self.p_list[i].rotation_row
        #             count+= 1
        #         else:
        #             self.p_list[i].row += self.p_list[i].rotation_col
        #             self.p_list[i].column += self.p_list[i].rotation_row
        #             count+= 1

        #         # self.p_list[i].row += (self.p_list[i].rotation_row -1) 
        #         # self.p_list[i].column += (self.p_list[i].rotation_col -1)


        # elif future_col > col:
        #     self.p_list[x].row = future_row
        #     self.p_list[x].column = future_col+1
        #     for i in range(0, len(self.p_list)):
        #         # self.p_list[i].row += self.p_list[i].rotation_col # Maar dan alleen de eerste element
        #         # self.p_list[i].column += self.p_list[i].rotation_row
                
        #         # if self.p_list[i].rotation_row  == 0:
        #         #     self.p_list[i].row = self.p_list[i-1].row
        #         #     self.p_list[i].column = self.p_list[i-1].column
        #         # else:
        #         #     self.p_list[i].row = self.p_list[i-1].row - self.p_list[i].rotation_col
        #         #     self.p_list[i].column = self.p_list[i-1].column + self.p_list[i].rotation_row
                
        #         self.p_list[i].row += (self.p_list[i].rotation_row - 1) 
        #         self.p_list[i].column += (1 + self.p_list[i].rotation_col)



        # elif future_col < col and self.p_list[x-1].column == self.p_list[x].column: 
        #     self.p_list[x].row = future_row
        #     self.p_list[x].column = future_col-1
        #     for i in range(0, len(self.p_list)):
        #         # self.p_list[i].row += self.p_list[i].rotation_col # Maar dan alleen de eerste element
        #         # self.p_list[i].column += self.p_list[i].rotation_row
                
        #         # if self.p_list[i].rotation_row  == 0:
        #         #     self.p_list[i].row = self.p_list[i-1].row
        #         #     self.p_list[i].column = self.p_list[i-1].column
        #         # else:
        #         #     self.p_list[i].row = self.p_list[i-1].row - self.p_list[i].rotation_col
        #         #     self.p_list[i].column = self.p_list[i-1].column + self.p_list[i].rotation_row
        
        #         self.p_list[i].row += (1 + self.p_list[i].rotation_row) 
                # self.p_list[i].column += (self.p_list[i].rotation_col -1)
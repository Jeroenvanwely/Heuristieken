import pandas as pd 
import numpy as np
import random
import proteinpowder as pp
import copy


class Fold:
    def __init__(self):
        self.protein = "HHPHHHPH"
        self.Protein = pp.Protein(self.protein)
        self.grid = pp.build_grid(self.protein)
        # self.buildprotein = .Protein(self.protein)
        self.Protein.protein_list = copy.deepcopy(pp.Protein(self.protein).protein_list)
                

    def optionlist(self, row, col, x):
        optionlist = []
        # dat de oneven de rows zijn en blablablabla
        #kijk boven
        if '_' in self.grid[row-1][col]:
            if self.fold_check(row, col, row-1, col, x):
                optionlist.append(row-1) 
                optionlist.append(col)
        #kijk beneden
        if '_' in self.grid[row+1][col]:
            if self.fold_check(row, col, row+1, col, x):
                optionlist.append(row+1) 
                optionlist.append(col)
        # kijk links
        if '_' in self.grid[row][col-1]:
            if self.fold_check(row, col, row, col-1, x):
                optionlist.append(row) 
                optionlist.append(col-1)
        # kijk rechts
        if '_' in self.grid[row][col+1]:
            if self.fold_check(row, col, row, col+1, x):
                optionlist.append(row) 
                optionlist.append(col+1)

        print(optionlist, "OPTIONLIST", x)
        return optionlist

    def choose_option(self, optionlist, row, col):
        if optionlist != []:
            option = random.randint(0, (len(optionlist)-1))
            if option%2 != 0:
                option -= 1
            return optionlist[option], optionlist[option + 1]
        else:
            print("ROW", row, col)
            return row, col

    # Deze functie checkt gegeven een bepaalde plek waar we nu zijn, en een gegeven plek
    # waar die naartoe gevouwen wordt of het mogelijk is om het proteine hierheen te vouwen.
    def fold_check(self, current_row, current_col, future_row, future_col, x):
        if future_row > current_row: 
            for i in range(1, len(self.protein) - x):
                if self.grid[future_row+i][future_col] != '_':
                    return False

        elif future_row < current_row and self.Protein.protein_list[x-1].row == self.Protein.protein_list[x].row:
            for i in range(1, len(self.protein) - x):
                if self.grid[future_row-i][future_col] != '_':
                    return False

        elif future_col > current_col:
            for i in range(1, len(self.protein) - x):
                if self.grid[future_row][future_col+i] != '_':
                    return False

        elif future_col < current_col and self.Protein.protein_list[x-1].column == self.Protein.protein_list[x].column:
            for i in range(1, len(self.protein) - x):
                if self.grid[future_row][future_col-i] != '_':
                    return False

        return True

    def amino_check(self, future_row, future_col, x):
        for i in range(x):
            if self.Protein.protein_list[i].row == future_row and self.Protein.protein_list[i].column == future_col:
                return False
        return True
            

    def fold(self, future_row, future_col, row, col, x):

        ''' Vanaf aminozuur x, het aminozuur dat gedraaid gaat worden, gaat er gekeken
            worden wat de positie van de daarop volgende aminozuren is. Eerst wordt het
            aminozuur x verplaatst naar de nieuwe positie. Dan wordt er gekeken hoeveel
            stappen (hoeken van 90 graden) deze heeft gemaakt. Deze stappen worden vervolgens
            ook toegepast op de daarop volgende aminozuren. Deze gaan dan vanaf de huidige 
            positie de stappen toepassen en dan de richting die hieruit komt wordt gemaakt
            vanaf het vorige aminozuur.
        '''

        # DRAMA : er is soms een aminozuur op dezelfde plek?????

        positionlist = [(0,1), (-1,0), (0,-1), (1,0)] #draaiing

        indexlist = self.Protein.position(x)

        newposrow = future_row - row
        newposcol = future_col - col

        if newposrow == 0 and newposcol == 0:
            return

        newpos = (newposrow, newposcol)
        newposindex= positionlist.index(newpos)

        print(indexlist)
        steps = newposindex - indexlist[0]


        self.Protein.protein_list[x].row = future_row
        self.Protein.protein_list[x].column = future_col

    
        switch = True

        for i in range(1, len(indexlist)):
            temp_p = copy.deepcopy(self.Protein.protein_list)
            # try:
            print(i, "i", indexlist)
            newindex = (indexlist[i] + steps) % len(positionlist)
            print(newindex, "new index")
            value = positionlist[newindex]
            print("value", value)
            newrow =  copy.copy(self.Protein.protein_list[i+x-1].row) + value[0]
            newcol =  copy.copy(self.Protein.protein_list[i+x-1].column) + value[1]
            aminolegit = self.amino_check(newrow, newcol, x+i)
            if aminolegit == False:
                print("DJSodjvoiwdvnidnvwVDNVKvwed") #if optionlist is niet leeg
                optionlist = self.optionlist(self.Protein.protein_list[i+x-1].row, self.Protein.protein_list[i+x-1].column, i+x)
                print(optionlist, "optionlist")
                newtryrow, newtrycol = self.choose_option(optionlist, self.Protein.protein_list[i+x-1].row, self.Protein.protein_list[i+x-1].column)
                print(newtryrow, newtrycol)
                self.Protein.protein_list[i+x].row = newtryrow
                self.Protein.protein_list[i+x].column = newtrycol
            else:
                self.Protein.protein_list[i+x].row = newrow
                self.Protein.protein_list[i+x].column = newcol
         
            # # except ValueError:
            #     optionlist = self.optionlist(Protein.protein_list[i+x-1].row, Protein.protein_list[i+x-1].column, i+x)
            #     print(optionlist)
            #     newtryrow, newtrycol = self.choose_option(optionlist, Protein.protein_list[i+x-1].row, Protein.protein_list[i+x-1].column)


    def get_fold(self):
        for i in range(len(self.Protein.protein_list)):
                    column = self.Protein.protein_list[i].column
                    row = self.Protein.protein_list[i].row
                    value = self.Protein.protein_list[i].value
                    self.grid[row][column] = value + str(i)

        for i in range(0, len(self.Protein.protein_list)):
            if i < 1:
                continue
            else: 
                current_row = self.Protein.protein_list[i-1].row
                current_col = self.Protein.protein_list[i-1].column
                future_row, future_col = self.choose_option(self.optionlist(current_row, current_col, i), current_row, current_col)
                self.fold(future_row, future_col, current_row, current_col, i)
                self.grid = pp.build_grid(self.protein)
                for j in range(len(self.Protein.protein_list)):
                    column = self.Protein.protein_list[j].column
                    row = self.Protein.protein_list[j].row
                    value = self.Protein.protein_list[j].value
                    self.grid[row][column] = value + str(j)
        print(self.grid)
        score = pp.check_protein(self.grid, self.Protein, self.protein) 
        print(score)

    def random_fold(self): #wannabe hill climber
        for i in range(len(self.Protein.protein_list)):
                column = self.Protein.protein_list[i].column
                row = self.Protein.protein_list[i].row
                value = self.Protein.protein_list[i].value
                self.grid[row][column] = value + str(i)

        for i in range(0, 100):
            current_grid = copy.deepcopy(self.grid)
            current_score = pp.check_protein(self.grid, self.Protein, self.protein)
            current_grid = copy.deepcopy(self.grid)
            #onthou je plek op dit moment
            j = random.randint(0, (len(self.Protein.protein_list)-1))
            if j <= 1:
                continue
            else: 
                current_row = self.Protein.protein_list[j-1].row
                current_col = self.Protein.protein_list[j-1].column
                future_row, future_col = self.choose_option(self.optionlist(current_row, current_col, j), current_row, current_col)
                print(j)
                self.fold(future_row, future_col, current_row, current_col, j)
                self.grid = pp.build_grid(self.protein)
                for k in range(len(self.Protein.protein_list)):
                    column = self.Protein.protein_list[k].column
                    row = self.Protein.protein_list[k].row
                    value = self.Protein.protein_list[k].value
                    self.grid[row][column] = value + str(k)
            
            if pp.check_protein(self.grid, self.Protein, self.protein) >= current_score:
                continue
            else:
                self.grid = current_grid            
            
            print(self.grid)
        score = pp.check_protein(self.grid, self.Protein, self.protein) 
        print(score)

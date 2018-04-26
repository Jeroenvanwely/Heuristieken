import pandas as pd 
import numpy as np
import random
import proteinpowder as pp
import copy


class Fold:
    def __init__(self):
        self.protein = "HHPHHHPHPHHHPH"
        self.grid = pp.build_grid(self.protein)
        self.buildprotein = pp.Protein.build_protein(self.protein)
        self.p_list = copy.deepcopy(self.buildprotein.protein_list)
                

    def optionlist(self, row, col, x):
        optionlist = []
        print("row en column", row, col)
        print(self.grid)
        # dat de oneven de rows zijn en blablablabla
        #kijk boven
        if '_' in self.grid[row-1][col]:
            print("hi")
            if self.fold_check(row, col, row-1, col, x):
                optionlist.append(row-1) 
                optionlist.append(col)
        #kijk beneden
        if '_' in self.grid[row+1][col]:
            print("hi")
            if self.fold_check(row, col, row+1, col, x):
                optionlist.append(row+1) 
                optionlist.append(col)
        # kijk links
        if '_' in self.grid[row][col-1]:
            print("hi")
            if self.fold_check(row, col, row, col-1, x):
                optionlist.append(row) 
                optionlist.append(col-1)
        # kijk rechts
        if '_' in self.grid[row][col+1]:
            print("hi")
            if self.fold_check(row, col, row, col+1, x):
                optionlist.append(row) 
                optionlist.append(col+1)

        return optionlist

    def choose_option(self, optionlist):
        print("optionlist", optionlist)
        if optionlist != []:
            option = random.randint(0, (len(optionlist)-1))
            print("option", option)
            if option%2 != 0:
                option -= 1
            return optionlist[option], optionlist[option + 1]
        else:
            return row, col

    def rotation(self, current_row, current_col, future_row, future_col):
        rowcoordinate = future_row - current_row
        colcoordinate = current_col - future_col
        return rowcoordinate, colcoordinate

    # Deze functie checkt gegeven een bepaalde plek waar we nu zijn, en een gegeven plek
    # waar die naartoe gevouwen wordt of het mogelijk is om het proteine hierheen te vouwen.
    def fold_check(self, current_row, current_col, future_row, future_col, x):
        if future_row > current_row: 
            for i in range(1, len(self.protein) - x):
                if self.grid[future_row+i][future_col] != '_':
                    return False

        elif future_row < current_row and self.p_list[x-1].row == self.p_list[x].row:
            for i in range(1, len(self.protein) - x):
                if self.grid[future_row-i][future_col] != '_':
                    return False

        elif future_col > current_col:
            for i in range(1, len(self.protein) - x):
                if self.grid[future_row][future_col+i] != '_':
                    return False

        elif future_col < current_col and self.p_list[x-1].column == self.p_list[x].column:
            for i in range(1, len(self.protein) - x):
                if self.grid[future_row][future_col-i] != '_':
                    return False
        
        return True

        # for i in range(1, len(protein) - x):
        #     if grid[future_row+(i*rowcoordinate)][future_col+(i*colcoordinate)] != '_':
        #         return False
        # return True

    def fold(self, future_row, future_col, row, col, x):
        if future_row > row: 
            for i in range(0, len(self.protein) - x):
                self.p_list[x+i].row = future_row+i
                self.p_list[x+i].column = future_col

        elif future_row < row and self.p_list[x-1].row == self.p_list[x].row:
            for i in range(0, len(self.protein) - x):
                self.p_list[x+i].row = future_row-i
                self.p_list[x+i].column = future_col

        elif future_col > col:
            for i in range(0, len(self.protein) - x):
                self.p_list[x+i].row = future_row
                self.p_list[x+i].column = future_col+i
                
        elif future_col < col and self.p_list[x-1].column == self.p_list[x].column:
            for i in range(0, len(self.protein) - x):
                self.p_list[x+i].row = future_row
                self.p_list[x+i].column = future_col-i
            

    def get_fold(self):
        for i in range(len(self.p_list)):
                    column = self.p_list[i].column
                    row = self.p_list[i].row
                    value = self.p_list[i].value
                    self.grid[row][column] = value + str(i)

        for i in range(0, len(self.p_list)):
            if i < 1:
                continue
            else: 
                current_row = self.p_list[i-1].row
                current_col = self.p_list[i-1].column
                future_row, future_col = self.choose_option(self.optionlist(current_row, current_col, i))
                print(future_row, future_col)
                self.fold(future_row, future_col, current_row, current_col, i)
                proteingrid = pp.build_grid(self.protein)
                for i in range(len(self.p_list)):
                    column = self.p_list[i].column
                    row = self.p_list[i].row
                    value = self.p_list[i].value
                    proteingrid[row][column] = value + str(i)
        print(proteingrid)
        score = pp.check_protein(proteingrid, self.buildprotein, self.protein) 
        print(score)

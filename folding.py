import pandas as pd 
import numpy as np
import random
import proteinpowder as pp
import copy


class Fold:
    def __init__(self):
        self.protein = "HHPHHHPH"
        self.grid = pp.build_grid(self.protein)
        self.buildprotein = pp.Protein.build_protein(self.protein)
        self.p_list = copy.deepcopy(self.buildprotein.protein_list)
                

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

        return optionlist

    def choose_option(self, optionlist, row, col):
        if optionlist != []:
            option = random.randint(0, (len(optionlist)-1))
            if option%2 != 0:
                option -= 1
            return optionlist[option], optionlist[option + 1]
        else:
            return row, col

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


    def fold(self, future_row, future_col, row, col, x):
        temp_p = copy.deepcopy(self.p_list)
        row_translations = [0]
        col_translations = [0] #0 zodat hij bij de eerste geen verandering toebrengt

        rotation = []


        for i in range(0, len(self.p_list)):
            if i == 0:
                continue
            else:
                row_translation = self.p_list[i].row - self.p_list[i-1].row
                col_translation = self.p_list[i].column - self.p_list[i-1].column
                row_translations.append(row_translation)
                col_translations.append(col_translation)
        
                print(row_translations, col_translations)
        
        if future_row > row:
            for i in range(0, len(self.protein) - x):
                self.p_list[i].row = future_row+1
                self.p_list[i].column = future_col
            for i in range(0, len(self.p_list)):
                self.p_list[i].row += row_translations[i]
                self.p_list[i].column += col_translations[i]

        elif future_row < row and self.p_list[x-1].row == self.p_list[x].row:
            for i in range(0, len(self.protein) - x):
                self.p_list[x+1].row = future_row-1
                self.p_list[x+1].column = future_col
            for i in range(0, len(self.p_list)):
                self.p_list[i].row += row_translations[i]
                self.p_list[i].column += col_translations[i]

        elif future_col > col:
            for i in range(0, len(self.protein) - x):
                self.p_list[x+1].row = future_row
                self.p_list[x+1].column = future_col+1
            for i in range(0, len(self.p_list)):
                self.p_list[i].row += row_translations[i]
                self.p_list[i].column += col_translations[i]
                
        elif future_col < col and self.p_list[x-1].column == self.p_list[x].column:
            for i in range(0, len(self.protein) - x):
                self.p_list[x+i].row = future_row
                self.p_list[x+i].column = future_col-1
            for i in range(0, len(self.p_list)):
                self.p_list[i].row += row_translations[i]
                self.p_list[i].column += col_translations[i]
        
            

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
                future_row, future_col = self.choose_option(self.optionlist(current_row, current_col, i), current_row, current_col)
                self.fold(future_row, future_col, current_row, current_col, i)
                self.grid = pp.build_grid(self.protein)
                for j in range(len(self.p_list)):
                    column = self.p_list[j].column
                    row = self.p_list[j].row
                    value = self.p_list[j].value
                    self.grid[row][column] = value + str(j)
        print(self.grid)
        score = pp.check_protein(self.grid, self.buildprotein, self.protein) 
        print(score)

    def random_fold(self): #wannabe hill climber
        for i in range(len(self.p_list)):
                column = self.p_list[i].column
                row = self.p_list[i].row
                value = self.p_list[i].value
                self.grid[row][column] = value + str(i)

        for i in range(0, 100):
            current_grid = copy.deepcopy(self.grid)
            current_score = pp.check_protein(self.grid, self.buildprotein, self.protein)
            current_grid = copy.deepcopy(self.grid)
            #onthou je plek op dit moment
            j = random.randint(0, (len(self.p_list)-1))
            if j <= 1:
                continue
            else: 
                current_row = self.p_list[j-1].row
                current_col = self.p_list[j-1].column
                future_row, future_col = self.choose_option(self.optionlist(current_row, current_col, j), current_row, current_col)
                
                self.fold(future_row, future_col, current_row, current_col, j)
                self.grid = pp.build_grid(self.protein)
                # print("grid", self.grid)
                # print(self.p_list)
                for k in range(len(self.p_list)):
                    column = self.p_list[k].column
                    row = self.p_list[k].row
                    value = self.p_list[k].value
                    self.grid[row][column] = value + str(k)
            
            # if pp.check_protein(self.grid, self.buildprotein, self.protein) >= current_score:
            #     continue
            # else:
            #     self.grid = current_grid            
            
            print(self.grid)
        score = pp.check_protein(self.grid, self.buildprotein, self.protein) 
        print(score)

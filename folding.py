import pandas as pd 
import numpy as np
import random
import proteinpowder as pp
import random
import copy


def option(grid, row, col, x):
    optionlist = []
    print("heklefaf", row, col)
    # dat de oneven de rows zijn en blablablabla
    #kijk boven
    if '_' in grid[row-1][col]:
        if fold_check(grid, row, col, row-1, col, x):
            optionlist.append(row-1) 
            optionlist.append(col)
    #kijk beneden
    if '_' in grid[row+1][col]:
        if fold_check(grid, row, col, row+1, col, x):
            optionlist.append(row+1) 
            optionlist.append(col)
    # kijk links
    if '_' in grid[row][col-1]:
        if fold_check(grid, row, col, row, col-1, x):
            optionlist.append(row) 
            optionlist.append(col-1)
    # kijk rechts
    if '_' in grid[row][col+1]:
        if fold_check(grid, row, col, row, col+1, x):
            optionlist.append(row) 
            optionlist.append(col+1)

    print("optionlist", optionlist)
    if optionlist != []:
        option = random.randint(0, (len(optionlist)-1))
        print("option", option)
        if option%2 != 0:
            option -= 1
        return optionlist[option], optionlist[option + 1]
    else:
        return row, col

def rotation(current_row, current_col, future_row, future_col):
    rowcoordinate = future_row - current_row
    colcoordinate = current_col - future_col
    return rowcoordinate, colcoordinate

# Deze functie checkt gegeven een bepaalde plek waar we nu zijn, en een gegeven plek
# waar die naartoe gevouwen wordt of het mogelijk is om het proteine hierheen te vouwen.
def fold_check(grid, current_row, current_col, future_row, future_col, x):
    rowcoordinate, colcoordinate = rotation(current_row, current_col, future_row, future_col)
    for i in range(1, len(protein) - x):
        if grid[future_row+(i*rowcoordinate)][future_col+(i*colcoordinate)] != '_':
            return False
    return True

def fold(future_row, future_col, row, col, p_list, x):
    if future_row > row: 
        print("hello")  
        for i in range(0, len(protein) - x):
            p_list[x+i].row = future_row+i
            p_list[x+i].column = future_col
            print("row", p_list[x-1].row,"col", p_list[x-1].column, p_list[x-1].value)
            print("row", p_list[x].row,"col", p_list[x].column, p_list[x].value)
    if future_row < row and future_col < col:
        print("hello")
        for i in range(0, len(protein) - x):
            p_list[x+i].row = future_row-i
            p_list[x+i].column = future_col-i
            print("row", p_list[x-1].row,"col", p_list[x-1].column, p_list[x-1].value)
            print("row", p_list[x].row,"col", p_list[x].column, p_list[x].value)
    if future_col > col:
        print("hello")
        for i in range(0, len(protein) - x):
            p_list[x+i].row = future_row-i
            p_list[x+i].column = future_col
            print("row", p_list[x-1].row,"col", p_list[x-1].column, p_list[x-1].value)
            print("row", p_list[x].row,"col", p_list[x].column, p_list[x].value)


if __name__ == "__main__":
    protein = "HHPHHHPH"
    grid = pp.build_grid(protein)
    buildprotein = pp.Protein.build_protein(protein)
    p_list = copy.deepcopy(buildprotein.protein_list)
    score = pp.check_protein(grid, buildprotein, protein) 

    for i in range(len(p_list)):
                column = p_list[i].column
                row = p_list[i].row
                value = p_list[i].value
                grid[row][column] = str(i)

    for i in range(0, len(p_list)):
        if i < 1:
            print("hoi")
        elif i == 2:
            current_row = p_list[i-1].row
            current_col = p_list[i-1].column
            future_row, future_col = option(grid, current_row, current_col, i)
            print(future_row, future_col)
            fold(future_row, future_col, current_row, current_col, p_list, i)
            grid = pp.build_grid(protein)
        
            for i in range(len(p_list)):
                column = p_list[i].column
                row = p_list[i].row
                value = p_list[i].value
                grid[row][column] = str(i)
        
        # else: 
        #     current_row = p_list[i].row
        #     current_col = p_list[i].column
        #     future_row, future_col = option(grid, current_row, current_col, i)
        #     print(future_row, future_col)
        #     fold(future_row, future_col, current_row, current_col, p_list, i)
        #     grid = pp.build_grid(protein)
        #     for i in range(len(p_list)):
        #         column = p_list[i].column
        #         row = p_list[i].row
        #         value = p_list[i].value
        #         grid[row][column] = str(i)
    print(grid)

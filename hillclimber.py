import pandas as pd 
import numpy as np
import random
import proteinpowder as pp
import random
import copy
import folding as ff

if __name__ == "__main__":
    protein = "HHPHHHPHPHHHPH"
    optionlist = []
    grid = pp.build_grid(protein)
    buildprotein = pp.Protein.build_protein(protein)
    p_list = copy.deepcopy(buildprotein.protein_list)

    for i in range(len(p_list)):
                column = p_list[i].column
                row = p_list[i].row
                value = p_list[i].value
                grid[row][column] = value + str(i)

    for i in range(0, len(p_list)):
        if i < 1:
            continue
        else: 
            current_row = p_list[i-1].row
            current_col = p_list[i-1].column
            optionlist = ff.optionlist(grid, current_row, current_col, i)
            ff.fold(future_row, future_col, current_row, current_col, p_list, i)
            grid = pp.build_grid(protein)
            for i in range(len(p_list)):
                column = p_list[i].column
                row = p_list[i].row
                value = p_list[i].value
                grid[row][column] = value + str(i)
    print(grid)
    score = pp.check_protein(grid, buildprotein, protein) 
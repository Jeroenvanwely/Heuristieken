import pandas as pd 
import numpy as np
import random
import classes as cc
import random
import copy
import helpers as h

def hillclimber(protein): 
    #Om 's avonds te runnen:
        # for j in range(10000): #TABTAB
    pro_obj = cc.Protein(protein)
    folding = cc.Fold(protein)
    grid = cc.Protein.build_grid(protein)
    pro_obj.protein_list = copy.deepcopy(cc.Protein(protein).protein_list) 
    # print(pro_obj.protein_list[0].row)  

    h.insert_protein(grid, pro_obj)

    for i in range(0, 500):
        current_grid = copy.deepcopy(grid)
        current_score = pro_obj.check_protein(grid, protein)
        current_p_list = copy.deepcopy(pro_obj.protein_list)
        j = random.randint(2, (len(pro_obj.protein_list)-1))
        
        current_row = pro_obj.protein_list[j-1].row
        current_col = pro_obj.protein_list[j-1].column
        future_row, future_col = folding.choose_option(folding.optionlist(current_row, current_col, j), current_row, current_col)
        
        folding.fold(future_row, future_col, current_row, current_col, j)
        grid = cc.Protein.build_grid(protein)
        h.insert_protein(grid, pro_obj)
        
        if cc.Protein.check_protein(grid, pro_obj, protein) <= current_score:
            print(i, "JOE",Check.check_protein(grid, pro_obj, protein))
            continue

        else:
            grid = current_grid 
            pro_obj.protein_list = current_p_list           
            
            print(grid)
        score = Check.check_protein(grid, pro_obj, protein) 
        print(score)

if __name__ == "__main__":
    hillclimber("HHPHHHPHPHHHPH")
    # Fold = cc.Fold("HHPHHHPHPHHHPH")
    # Fold.hillclimber()
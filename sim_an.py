import pandas as pd 
import numpy as np
import random
import proteinpowder as pp
import random
import copy
import folding as ff
import os
import helpers as helpe
import hillclimber as hill
import math

def sim_anneal(protein):
    ''' Ti = T0 - i(T0-Tn) / N
        Kan ik i als temp gebruiken? denk dat dit handig is
        T0 is iets van count die hoog staat
        De begintemp kies je zo dat op iedere verslechtering de kans 1 is
    '''

    score = hill.hillclimber(protein)
    print(score)
    
    highscore = copy.copy(score)
    highproteinlist = copy.deepcopy(fold.Protein.protein_list)

    T0 = 1000
    Tn = 0
    N = 10000
    # Tk = T0 - (0.9 * k)

    for i in range(len(fold.Protein.protein_list)):
            column = fold.Protein.protein_list[i].column
            row = fold.Protein.protein_list[i].row
            value = fold.Protein.protein_list[i].value
            fold.grid[row][column] = value + str(i)

    for i in range(0, 10000):

        current_grid = copy.deepcopy(fold.grid)
        current_score = helpe.check_protein(fold.grid, fold.Protein)
        current_p_list = copy.deepcopy(fold.Protein.protein_list)
        j = random.randint(0, (len(fold.Protein.protein_list)-1))
        if j <= 1:
            continue
        else: 
            current_row = fold.Protein.protein_list[j-1].row
            current_col = fold.Protein.protein_list[j-1].column
            future_row, future_col = fold.choose_option(fold.optionlist(current_row, current_col, j), current_row, current_col)
            # print(j)
            fold.fold(future_row, future_col, current_row, current_col, j)
            fold.grid = helpe.insert_protein(fold.Protein)
            for k in range(len(fold.Protein.protein_list)):
                column = fold.Protein.protein_list[k].column
                row = fold.Protein.protein_list[k].row
                value = fold.Protein.protein_list[k].value
                fold.grid[row][column] = value + str(k)
        
        if helpe.check_protein(fold.grid, fold.Protein) <= current_score:
            highscore = copy.copy(helpe.check_protein(fold.grid, fold.Protein))
            highproteinlist = copy.deepcopy(fold.Protein.protein_list)
            continue

        else:
            score_difference = helpe.check_protein(fold.grid, fold.Protein) - current_score
            score_calc = score_difference * 100
            temperature = T0 - (i*(T0 - Tn))/ N
            prob = math.exp(-score_calc / temperature)
            if prob > random.random():
                continue
            else:
                fold.grid = current_grid 
                fold.Protein.protein_list = current_p_list           
        
    score = helpe.check_protein(fold.grid, fold.Protein) 
    return score

if __name__ == "__main__":
    proteinlist = ["HHPHHHPHPHHHPH", "HPHPPHHPHPPHPHHPPHPH", "PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP", "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH", "PPCHHPPCHPPPPCHHHHCHHPPHHPPPPHHPPHPP", "CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC", "HCPHPCPHPCHCHPHPPPHPPPHPPPPHPCPHPPPHPHHHCCHCHCHCHH", "HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH"]
    
    fold = ff.Fold(proteinlist[0])
    score = sim_anneal(proteinlist[0])
    print(score)
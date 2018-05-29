import pandas as pd 
import numpy as np
import random
import proteinpowder as pp
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
    fold = ff.Fold(protein)
    score = hill.hillclimber(protein)
    print(score)

    highscore = copy.copy(score)
    highproteinlist = copy.deepcopy(fold.Protein.protein_list)

    T0 = 1000
    Tn = 100
    N = 100
    # Tk = T0 - (0.9 * k)

    scoreslist = [score, fold.Protein.protein_list]

    for i in range(len(fold.Protein.protein_list)):
            column = fold.Protein.protein_list[i].column
            row = fold.Protein.protein_list[i].row
            value = fold.Protein.protein_list[i].value
            fold.grid[row][column] = value + str(i)

    for i in range(0, 1000):

        current_grid, current_score, current_p_list = fold.random_fold()
        
        if helpe.check_protein(fold.grid, fold.Protein) <= current_score:
            if helpe.check_protein(fold.grid, fold.Protein) <= highscore:
                highscore = copy.copy(helpe.check_protein(fold.grid, fold.Protein))
                highproteinlist = copy.deepcopy(fold.Protein.protein_list)

        else:
            score_difference = helpe.check_protein(fold.grid, fold.Protein) - current_score
            score_calc = score_difference * 100
            temperature = T0 * ((Tn/T0)**(i/N))
            prob = math.exp(-score_calc / temperature)
            # print(score_difference, temperature, prob)
            if prob > random.random():
                continue
            else:
                fold.grid = current_grid 
                fold.Protein.protein_list = current_p_list 

    score = helpe.check_protein(fold.grid, fold.Protein)
        # scoreslist.append(score)
        # scoreslist.append(fold.Protein.protein_list)

    return highscore
        
    # score = helpe.check_protein(fold.grid, fold.Protein) 
    # return highscore #HIGHSCORE

if __name__ == "__main__":
    proteinlist = ["HHPHHHPHPHHHPH", "HPHPPHHPHPPHPHHPPHPH", "PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP", "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH", "PPCHHPPCHPPPPCHHHHCHHPPHHPPPPHHPPHPP", "CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC", "HCPHPCPHPCHCHPHPPPHPPPHPPPPHPCPHPPPHPHHHCCHCHCHCHH", "HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH"]
    
    fold = ff.Fold(proteinlist[0])
    score = sim_anneal(proteinlist[0])
    print(score)
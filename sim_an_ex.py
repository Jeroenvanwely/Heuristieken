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

def sim_anneal(protein, cool):
    ''' Ti = T0 - i(T0-Tn) / N
        Kan ik i als temp gebruiken? denk dat dit handig is
        T0 is iets van count die hoog staat
        De begintemp kies je zo dat op iedere verslechtering de kans 1 is
    '''
    fold = ff.Fold(protein)
    score = hill.hillclimber(protein)
    highscore = copy.copy(score)
    highproteinlist = copy.deepcopy(fold.Protein.protein_list)
    fold.grid = helpe.insert_protein(fold.Protein)

    # Linear
    if cool == int(1):
        T0 = 1000
        Tn = 0
        N = 10000
    # Exponential
    elif cool == int(2):
        T0 = 10000
        Tn = 1000
        N = 1000
    # Logarithmic
    elif cool == int(3):
        T0 = 1000
        Tn = 0
        N = 10000
        A = ((T0 - Tn) * (N +1)) / N
        B = T0 - A

    for i in range(0, 10000):
        current_grid, current_score, current_p_list = fold.random_fold()
        if helpe.check_protein(fold.grid, fold.Protein) <= current_score:
            highscore, highproteinlist = helpe.check_highscore(fold, current_score, highscore, highproteinlist)
        else:
            if cool == int(1):
                temperature = T0 - (i*(T0 - Tn))/ N
            elif cool == int(2):
                temperature = T0 * ((Tn/T0)**(i/N))
            elif cool == int(3):
                temperature = (A / (i+1)) + B
            helpe.probability(temperature, fold, current_score, current_grid, current_p_list)
    
    return highscore 
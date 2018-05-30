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
    highscore = copy.copy(score)
    highproteinlist = copy.deepcopy(fold.Protein.protein_list)
    fold.grid = helpe.insert_protein(fold.Protein)

    T0 = 10000
    Tn = 1000
    N = 1000

    for i in range(0, 10000):
        current_grid, current_score, current_p_list = fold.random_fold()
        if helpe.check_protein(fold.grid, fold.Protein) <= current_score:
            highscore, highproteinlist = helpe.check_highscore(fold, current_score, highscore, highproteinlist)
        else:
            temperature = T0 * ((Tn/T0)**(i/N))
            helpe.probability(temperature, fold, current_score, current_grid, current_p_list)
    return highscore 

if __name__ == "__main__":
    proteinlist = ["HHPHHHPHPHHHPH", "HPHPPHHPHPPHPHHPPHPH", "PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP", "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH", "PPCHHPPCHPPPPCHHHHCHHPPHHPPPPHHPPHPP", "CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC", "HCPHPCPHPCHCHPHPPPHPPPHPPPPHPCPHPPPHPHHHCCHCHCHCHH", "HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH"]
    
    # fold = ff.Fold(proteinlist[0])
    # score = sim_anneal(proteinlist[0])
    # print(score)

    # COURSE
    switch = 0
    for i in range(len(proteinlist)):
        for j in range(10):
            scoreslist = sim_anneal(proteinlist[i], switch)
            results = os.path.abspath('Results/simulated_anneal/linear/sim_course_ex' +str(i) + '.csv') 
            with open(results, 'a') as data: #add data
                for k in range(len(scoreslist)):
                    if k % 2 == 0:
                        data.write(str(scoreslist[k]) + '\n')
                    else:
                        for z in range(len(scoreslist[k])):
                            data.write(str(scoreslist[k][z]) + ',')
                        data.write('\n')    
                data.write('\n' + "new iteration" + '\n')
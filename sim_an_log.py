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

    T0 = 1000
    Tn = 0
    N = 10000
    A = ((T0 - Tn) * (N +1)) / N
    B = T0 - A

    scoreslist = [score]
    proteinlistlist = []
    for k in range(len(fold.Protein.protein_list)):
        proteinlistlist.append(fold.Protein.protein_list[k].row)
        proteinlistlist.append(fold.Protein.protein_list[k].column)
    scoreslist.append(proteinlistlist)

    for i in range(0, 10000):
        current_grid, current_score, current_p_list = fold.random_fold()
        if helpe.check_protein(fold.grid, fold.Protein) <= current_score:
            highscore, highproteinlist = helpe.check_highscore(fold, current_score, highscore, highproteinlist)
        else:
            temperature = (A / (i+1)) + B
            helpe.probability(temperature, fold, current_score, current_grid, current_p_list)
 
    #     if switch == 0:
    #         proteinlistlist = []
    #         score = helpe.check_protein(fold.grid, fold.Protein)
    #         scoreslist.append(score)
    #         for k in range(len(fold.Protein.protein_list)):
    #             proteinlistlist.append(fold.Protein.protein_list[k].row)
    #             proteinlistlist.append(fold.Protein.protein_list[k].column)
    #         scoreslist.append(proteinlistlist)
    # if switch == 0:
    #     return scoreslist
    # elif switch == 1:
    #     return highscore 
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
            results = os.path.abspath('Results/simulated_anneal/sigmoid/sim_course_sig' +str(i) + '.csv') 
            with open(results, 'a') as data: #add data
                for k in range(len(scoreslist)):
                    if k % 2 == 0:
                        data.write(str(scoreslist[k]) + '\n')
                    else:
                        for z in range(len(scoreslist[k])):
                            data.write(str(scoreslist[k][z]) + ',')
                        data.write('\n')    
                data.write('\n' + "new iteration" + '\n')
        
    
    # SCORE
    switch = 1
    for i in range(0, len(proteinlist)):
        for j in range(30):
            score = sim_anneal(proteinlist[i], switch)
            results = os.path.abspath('Results/simulated_anneal/sigmoid/sim_results_sig' +str(i) + '.csv') 
            with open(results, 'a') as data: #add data
                data.write(str(score) + '\n')
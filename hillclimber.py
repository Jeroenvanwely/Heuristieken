import pandas as pd 
import numpy as np
import random
import proteinpowder as pp
import copy
import folding as ff
import os
import helpers as helpe
import timeit

def hillclimber(protein):
    ''' Dit algoritme probeert de beste score van een gegeven proteine te vinden. 
        Door eerst een kopie te maken van de huidige staat, dan een mutatie uit te
        voeren en vervolgens de twee met elkaar te vergelijken. De hoogste score 
        wordt behouden. In het geval dat de score's gelijk aan elkaar zijn wordt de
        nieuwste score behouden.
        
        Het neemt een proteine in de vorm van een string als argument en geeft een
        score in de vorm van een integer terug.
    '''

    fold = ff.Fold(protein)
    helpe.insert_protein(fold.Protein)

    scoreslist = []
    for i in range(10000):
        current_grid, current_score, current_p_list = fold.random_fold()
        if helpe.check_protein(fold.grid, fold.Protein) <= current_score:
            continue
        else:
            fold.grid = current_grid 
            fold.Protein.protein_list = current_p_list 
        proteinlistlist = []
        score = helpe.check_protein(fold.grid, fold.Protein)
        scoreslist.append(score)
        for k in range(len(fold.Protein.protein_list)):
            proteinlistlist.append(fold.Protein.protein_list[k].row)
            proteinlistlist.append(fold.Protein.protein_list[k].column)
        scoreslist.append(proteinlistlist)        
    # return helpe.check_protein(fold.grid, fold.Protein)
    return scoreslist

if __name__ == "__main__":
    proteinlist = ["HHPHHHPHPHHHPH", "HPHPPHHPHPPHPHHPPHPH", "PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP", "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH", "PPCHHPPCHPPPPCHHHHCHHPPHHPPPPHHPPHPP", "CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC", "HCPHPCPHPCHCHPHPPPHPPPHPPPPHPCPHPPPHPHHHCCHCHCHCHH", "HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH"]
    
    # fold = ff.Fold(proteinlist[0])
    # score = hillclimber(proteinlist[0])
    # print(score)

    # fold = ff.Fold(proteinlist[0])
    # fold.hillclimber()
    # score = fold.sim_anneal()
    # print(score)
    # print(protein.protein_list[3].row)

    # fold = ff.Fold(proteinlist[1])
    # score = hillclimber(proteinlist[1])
    # print(score)

    for i in range(len(proteinlist)):
        for j in range(1):
            scoreslist = hillclimber(proteinlist[i])
            results = os.path.abspath('Results/hillclimber/hill_course' +str(i) + '.csv') 
            with open(results, 'a') as data: #add data
                for k in range(len(scoreslist)):
                    if k % 2 == 0:
                        data.write(str(scoreslist[k]) + '\n')
                    else:
                        for z in range(len(scoreslist[k])):
                            data.write(str(scoreslist[k][z]) + ',')
                        data.write('\n')    
                data.write('\n' + "new iteration" + '\n')



import pandas as pd 
import numpy as np
import random
import proteinpowder as pp
import random
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

    for i in range(10000):
        current_grid, current_score, current_p_list = fold.random_fold()
        if helpe.check_protein(fold.grid, fold.Protein) <= current_score:
            continue
        else:
            fold.grid = current_grid 
            fold.Protein.protein_list = current_p_list         
    return helpe.check_protein(fold.grid, fold.Protein)

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

    for i in range(10):
        fold = ff.Fold(proteinlist[i])
        score = hillclimber(proteinlist[i])

        results = os.path.abspath('Results/hillclimber/time' +str(i) + '.csv') 
        with open(results, 'a') as data: #add data
            data.write(str(score) + '\n')



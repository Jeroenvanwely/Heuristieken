import pandas as pd 
import numpy as np
import random
import proteinpowder as pp
import random
import copy
import folding as ff
import os


if __name__ == "__main__":
    proteinlist = ["HHPHHHPHPHHHPH", "HPHPPHHPHPPHPHHPPHPH", "PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP", "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH", "PPCHHPPCHPPPPCHHHHCHHPPHHPPPPHHPPHPP", "CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC", "HCPHPCPHPCHCHPHPPPHPPPHPPPPHPCPHPPPHPHHHCCHCHCHCHH", "HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH"]
    
    fold = ff.Fold(proteinlist[0])
    score = fold.sim_anneal()
    print(score)
    # print(protein.protein_list[3].row)

    # for i in range(len(proteinlist)):
    #     for j in range(100):
    #         fold = ff.Fold(proteinlist[i])
    #         score = fold.hillclimber()

    #         results = os.path.abspath('Results/h_results' +str(i) + '.csv') 
    #         with open(results, 'a') as data: #add data
    #             data.write(str(score) + '\n')



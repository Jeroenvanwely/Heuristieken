import pandas as pd 
import numpy as np
import random
import proteinpowder as pp
import random
import copy
import folding as ff
import os
import helpers as helpe

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

    for i in range(500):
        # Maak kopie van huidige staat voor latere vergelijkingen
        current_grid = copy.deepcopy(fold.grid)
        current_score = helpe.check_protein(fold.grid, fold.Protein)
        current_p_list = copy.deepcopy(fold.Protein.protein_list)
        
        # Kies een random plek om te vouwen en kies een random optie om naar te vouwen
        j = random.randint(2, (len(fold.Protein.protein_list)-1))
        current_row = fold.Protein.protein_list[j-1].row
        current_col = fold.Protein.protein_list[j-1].column
        future_row, future_col = fold.choose_option(fold.optionlist(current_row, current_col, j), current_row, current_col)
        # print(current_row, current_col, future_row, future_col)

        # Vouw en zet in het grid
        fold.fold(future_row, future_col, current_row, current_col, j)
        fold.grid = helpe.insert_protein(fold.Protein)
        
        # Is de score beter? Ga door. Anders ga terug naar oude staat
        if helpe.check_protein(fold.grid, fold.Protein) <= current_score:
            continue
        else:
            fold.grid = current_grid 
            fold.Protein.protein_list = current_p_list           
        
    score = helpe.check_protein(fold.grid, fold.Protein)
    # pp.print_graph2(fold.Protein.protein_list)


    # rowlist = []
    # for i in range(len(Protein.protein_list)):
    #     rowlist.append()

    return score

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
    score = hillclimber(proteinlist[1])
    print(score)

    # for i in range(len(proteinlist)):
    #     for j in range(100):
    #         fold = ff.Fold(proteinlist[i])
    #         score = hillclimber(proteinlist[i])

    #         results = os.path.abspath('Results/h_results' +str(i) + '.csv') 
    #         with open(results, 'a') as data: #add data
    #             data.write(str(score) + '\n')



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
    return scoreslist


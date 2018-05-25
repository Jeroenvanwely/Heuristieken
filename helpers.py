import pandas as pd 
import numpy as np
import random
import matplotlib.pylab as plt
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import proteinpowder as pp
import copy

def insert_protein(fold):
    for i in range(len(fold.Protein.protein_list)):
        column = fold.Protein.protein_list[i].column
        row = fold.Protein.protein_list[i].row
        value = fold.Protein.protein_list[i].value
        fold.grid[row][column] = value + str(i)


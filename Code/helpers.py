import pandas as pd 
import numpy as np
import random
import classes as cc
import random
import copy

def insert_protein(grid, pro_obj):
    for i in range(len(pro_obj.protein_list)):
        column = pro_obj.protein_list[i].column
        row = pro_obj.protein_list[i].row
        value = pro_obj.protein_list[i].value
        grid[row][column] = value + str(i)
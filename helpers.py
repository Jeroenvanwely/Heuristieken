import pandas as pd 
import numpy as np
import random
import matplotlib.pylab as plt
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import proteinpowder as pp
import copy

def insert_protein(pro_obj):
    if len(pro_obj.protein_list) % 2 == 0:
        grid_length = 2*len(pro_obj.protein_list)
    else:
        grid_length = 2*len(pro_obj.protein_list) + 1
    grid = np.chararray((grid_length, grid_length), itemsize = 3, unicode=True)
    grid[:] = '_'
    
    for i in range(len(pro_obj.protein_list)):
        column = pro_obj.protein_list[i].column
        row = pro_obj.protein_list[i].row
        value = pro_obj.protein_list[i].value
        grid[row][column] = value + str(i)
    return grid

def choose_random_option(option_list):
    option = random.randint(0, (len(option_list) - 1))
    if option%2 != 0:
        option -= 1
    return option

def graph_boundaries(pro_obj):
    ''' Om de visualisatie duidelijker te maken wordt het zicht van de graph 
        gecentreerd op alleen op waar de proteine zich bevind. 
        Hier zijn de uiterste x en y coordinaten voor nodig die worden hier gevonden
    '''
    lowest_row = 100
    highest_row = 0
    lowest_column = 100
    highest_column = 0
    
    for i in range(len(pro_obj.protein_list)):
        if pro_obj.protein_list[i].row < lowest_row:
            lowest_row = pro_obj.protein_list[i].row
        if pro_obj.protein_list[i].row > highest_row:
            highest_row = pro_obj.protein_list[i].row
        if pro_obj.protein_list[i].column < lowest_column:
            lowest_column = pro_obj.protein_list[i].column
        if pro_obj.protein_list[i].column > highest_column:
            highest_column = pro_obj.protein_list[i].column

    return lowest_row-1, highest_row+1, lowest_column-1, highest_column+1

def print_graph(pro_obj):
    ''' De graph met de structuur van het proteine wordt hier geprint.
    '''
    plt.style.use('seaborn-whitegrid')
    max_row_list = []
    max_column_list = []
    value_list = []
    for i in range(len(pro_obj.protein_list)):
        max_row_list.append(pro_obj.protein_list[i].row)
        max_column_list.append(pro_obj.protein_list[i].column)
        value_list.append(pro_obj.protein_list[i].value)

    lowest_row, highest_row, lowest_column, highest_column = graph_boundaries(pro_obj)
    if highest_row - lowest_row >= highest_column - lowest_column:
        plt.axis([lowest_row, highest_row, lowest_column, lowest_column + highest_row - lowest_row]) 
    else:
        plt.axis([lowest_row, lowest_row + highest_column - lowest_column, lowest_column, highest_column])

    colors = {
        'H' : 'r', 
        'P' : 'b',
        'C' : 'purple',
        }
    
    df = {
        'x': max_row_list, 
        'y': max_column_list, 
        's': 300, 
        'group': [colors[x] for x in value_list]
        }

    plt.plot(df['x'], df['y'], zorder=1)
    plt.scatter(df['x'], df['y'], df['s'], c=df['group'], zorder=2)
    
    classes = ['H','P', 'C']
    class_colours = ['r','b','purple']
    recs = []
    for i in range(0,len(class_colours)):
        recs.append(mpatches.Rectangle((0,0),1,1,fc=class_colours[i]))
    plt.legend(recs,classes,loc=1)
    plt.show()

def check_protein(grid, pro_obj):
    ''' We houden de eerste node bij en checken dan alle vier de hokjes
        om hem heen. Degene die de tweede node is pakken we en daarmee
        gaan we vervolgens verder om te checken wat om hem heen staat.
        Bij elke H die we gecheckt hebben voegen we deze toe aan een lijst
        zodat dubbele tellingen voorkomen worden.
    '''

    score = 0
    checked = []
    for i in range(len(pro_obj.protein_list)):
        row = pro_obj.protein_list[i].row
        col = pro_obj.protein_list[i].column
        if 'H' in grid[row][col]:
            num = str(i+1)
            #kijk boven
            if ('H' in grid[row-1][col] or 'C' in grid[row-1][col]) and num not in grid[row-1][col] and grid[row-1][col] not in checked:
                score-=1
            #kijk beneden
            if ('H' in grid[row+1][col] or 'C' in grid[row+1][col]) and num not in grid[row+1][col] and grid[row+1][col] not in checked:
                score-=1
            # kijk links
            if ('H' in grid[row][col-1] or 'C' in grid[row][col-1]) and num not in grid[row][col-1] and grid[row][col-1] not in checked:
                score-=1
            # kijk rechts
            if ('H' in grid[row][col+1] or 'C' in grid[row][col+1]) and num not in grid[row][col+1] and grid[row][col+1] not in checked:
                score-=1
            checked.append(grid[row][col])

        if 'C' in grid[row][col]:
            num = str(i+1)
            #kijk boven
            if ('H' in grid[row-1][col] or 'C' in grid[row-1][col]) and num not in grid[row-1][col] and grid[row-1][col] not in checked:
                if 'H' in grid[row-1][col]:    
                    score-=1
                if 'C' in grid[row-1][col]:
                    score-=5
            #kijk beneden
            if ('H' in grid[row+1][col] or 'C' in grid[row-1][col]) and num not in grid[row+1][col] and grid[row+1][col] not in checked:
                if 'H' in grid[row+1][col]:    
                    score-=1
                if 'C' in grid[row+1][col]:
                    score-=5
            # kijk links
            if ('H' in grid[row][col-1] or 'C' in grid[row-1][col]) and num not in grid[row][col-1] and grid[row][col-1] not in checked:
                if 'H' in grid[row][col-1]:    
                    score-=1
                if 'C' in grid[row][col-1]:
                    score-=5
            # kijk rechts
            if ('H' in grid[row][col+1] or 'C' in grid[row-1][col]) and num not in grid[row][col+1] and grid[row][col+1] not in checked:
                if 'H' in grid[row][col+1]:    
                    score-=1
                if 'C' in grid[row][col+1]:
                    score-=5
            checked.append(grid[row][col])
    return score
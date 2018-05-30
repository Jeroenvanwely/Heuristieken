import numpy as np
import random
import matplotlib.pylab as plt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import copy
import math


def insert_protein(pro_obj):
    ''' Insert_protein neemt een Proteine object als argument en maakt aan de
        hand van de lengte van het proteine een numpy grid. Vervolgens plaatst hij
        het proteine ook in het grid.
        Returnt een ingevulde grid.
    '''

    # Het maken van het grid.
    if len(pro_obj.protein_list) % 2 == 0:
        grid_length = 2*len(pro_obj.protein_list)
    else:
        grid_length = 2*len(pro_obj.protein_list) + 1
    grid = np.chararray((grid_length, grid_length), itemsize = 3, unicode=True)
    grid[:] = '_'
    
    # Het plaatsen van het proteine in de grid.
    for i in range(len(pro_obj.protein_list)):
        column = pro_obj.protein_list[i].column
        row = pro_obj.protein_list[i].row
        value = pro_obj.protein_list[i].value
        grid[row][column] = value + str(i)
    return grid

def choose_random_option(option_list):
    ''' Choose_random_option neemt een lijst als argument en returnt vervolgens
        een random even integer tussen 0 en de lengte van die gegeven lijst.
    '''

    option = random.randint(0, (len(option_list) - 1))
    # Als random int niet even is, int - 1.
    if option%2 != 0:
        option -= 1
    return option

def graph_boundaries(pro_obj):
    ''' Graph_boundaries neemt een proteine object als argument en bepaald vervolgens
        de grenzen van de visualisatie aan de hand van de locatie van de aminozuren. 
        Returnt de hoogste en laagste waarden van zowel de row en de column met een
        speling van 1 aan alle kanten
    '''

    # Laagste row en column beginnen hoor, omdat een minimum gevonden moet worden.
    lowest_row = 100
    highest_row = 0
    lowest_column = 100
    highest_column = 0
    
    # Vind laagste en hoogste row en column.
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
    ''' Print_graph neemt een proteine object als argument en maakt vervolgens aan de
        hand van de locatie van de aminozuren een visualisatie. Het maakt gebruik van
        graph_boundaries om te bepalen waar de grenzen van de visualisatie liggen.
    '''

    plt.style.use('seaborn-whitegrid')
    max_row_list = []
    max_column_list = []
    value_list = []

    # Opslaan van coördinaten en waardes van proteïne.
    for i in range(len(pro_obj.protein_list)):
        max_row_list.append(pro_obj.protein_list[i].row)
        max_column_list.append(pro_obj.protein_list[i].column)
        value_list.append(pro_obj.protein_list[i].value)

    # Laat de assen zo lopen dat alleen het gedeelte van de grafiek wordt weergegeven.
    lowest_row, highest_row, lowest_column, highest_column = graph_boundaries(pro_obj)
    if highest_row - lowest_row >= highest_column - lowest_column:
        plt.axis([lowest_row, highest_row, lowest_column, lowest_column + highest_row - lowest_row]) 
    else:
        plt.axis([lowest_row, lowest_row + highest_column - lowest_column, lowest_column, highest_column])

    # Geef kleuren aan bepaalde waardes.
    colors = {'H' : 'r', 'P' : 'b','C' : 'purple',}
    df = {'x': max_row_list, 'y': max_column_list, 's': 300, 'group': [colors[x] for x in value_list]}
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
    ''' 
    '''

    score = 0
    checked = []
    for i in range(len(pro_obj.protein_list)):
        row = pro_obj.protein_list[i].row
        col = pro_obj.protein_list[i].column
        if 'H' in grid[row][col]:
            num = str(i+1)
            for j in [-1, 1]:
                
                # kijk boven of beneden of er CH of HH verbinding is, wijzig score.
                if (('H' in grid[row+j][col] or 'C' in grid[row+j][col]) 
                    and num not in grid[row+j][col] and grid[row+j][col] not in checked):
                    score-=1
                
                # kijk links en rechts.
                if (('H' in grid[row][col+j] or 'C' in grid[row][col+j]) 
                    and num not in grid[row][col+j] and grid[row][col+j] not in checked):
                    score-=1
                checked.append(grid[row][col])
        
        if 'C' in grid[row][col]:
            num = str(i+1)
            for j in [-1, 1]:
                
                # kijk boven en beneden of er CH of CC verbinding is, wijzig score.
                if (('H' in grid[row+j][col] or 'C' in grid[row+j][col]) 
                    and num not in grid[row+j][col] and grid[row+j][col] not in checked):
                    if 'H' in grid[row+j][col]:    
                        score-=1
                    elif 'C' in grid[row+j][col]:
                        score-=5
                
                # kijk links en rechts.
                if (('H' in grid[row][col+j] or 'C' in grid[row+j][col]) 
                    and num not in grid[row][col+j] and grid[row][col+j] not in checked):
                    if 'H' in grid[row][col+j]:    
                        score-=1
                    elif 'C' in grid[row][col+j]:
                        score-=5
                checked.append(grid[row][col])
    return score

def probability(temperature, fold, current_score, current_grid, current_p_list):
    score_difference = check_protein(fold.grid, fold.Protein) - current_score
    score_calc = score_difference * 100
    prob = math.exp(-score_calc / temperature)
    if prob > random.random():
        return
    else:
        fold.grid = current_grid 
        fold.Protein.protein_list = current_p_list 
        return

def check_highscore(fold, current_score, highscore, highproteinlist):
    if check_protein(fold.grid, fold.Protein) <= highscore:
        highscore = copy.copy(check_protein(fold.grid, fold.Protein))
        highproteinlist = copy.deepcopy(fold.Protein.protein_list)
        return highscore, highproteinlist
    return highscore, highproteinlist
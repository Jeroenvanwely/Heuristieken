import pandas as pd 
import numpy as np
import random
import matplotlib.pylab as plt
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import folding as ff
from datetime import datetime



class Node:
    def  __init__(self, value):
        ''' Initialiseert een node en vult zijn value in. Zet zijn row
            en column op none.
        '''
        self.value = value
        self.row = None
        self.column = None
        self.rotation = None

class Protein:
    def __init__(self, protein_str, head_node = None):
        self.last = None
        self.protein_list = []
        self.first = None
        self.build_protein(protein_str)
        # print(self.protein_list)

        
    def insert(self, value, protein_length):

        ''' Als er nog geen laatste node is dan voeg er een toe en maak
            hem de laatste node. Als er wel al een laatste node is dan voeg
            een kolom verder de nieuwe node toe en maak deze node vervolgens 
            de laatste node.
        '''
        node = Node(value)
        if self.last is None:
            self.first = node
            node.column = protein_length // 2 
            self.first.column = node.column
        else:
            node.column = self.last.column + 1
        node.row = protein_length - 1
        if self.last is None:
            self.first.row = node.row
        self.last = node
        self.protein_list.append(node)

    def build_protein(self, protein):

        ''' Dit predicaat bouwt een proteine op door per aminozuur te inserten
            in een array. Hierdoor hebben we direct al een nummer aan de verschillende
            aminozuren gehangen.
        '''
        protein_length = len(protein)
        for i in range (protein_length):
            self.insert(protein[i], protein_length)
        self.rotation(protein)
        return self


    def rotation(self, protein):
        ''' blabla
        '''

        for i in range(1, len(protein)):
            row_translation = self.protein_list[i].row - self.protein_list[i-1].row 
            col_translation = self.protein_list[i].column - self.protein_list[i-1].column
            rotation = (row_translation, col_translation)
            
            if rotation == (0, 1): #rechts ernaast
                self.protein_list[i].rotation = (0,1)
            elif rotation == (1, 0): #onder
                self.protein_list[i].rotation = (1,0)
            elif rotation == (0, -1): #links ernaast
                self.protein_list[i].rotation = (0,-1)
            elif rotation == (-1, 0): #boven
                self.protein_list[i].rotation = (-1, 0)
            else:
                break

    def position(self, x):
        ''' Deze checkt wat de positie is van het huidige aminozuur ten opzichte van
            de vorige. Dus staat hij links rechts boven of onder. Deze posities worden
            omgezet naar een indexnummer. Dit nummer wordt in een lijst gezet en deze wordt
            gereturnd.
        '''

        positionlist = [(0,1), (-1,0), (0,-1), (1,0)]
        indexlist = []
        # print(self.protein_list[:].row,self.protein_list[:].column)
        for i in range(x, len(self.protein_list)):
            # print(self.protein_list[i].row,self.protein_list[i].column)
            # print("aminozuur", i)
            # print(self.protein_list)
            # print('cur',self.protein_list[i].row, self.protein_list[i].column)
            # print('turn',self.protein_list[i-1].row, self.protein_list[i-1].column)
            row_t = self.protein_list[i].row - self.protein_list[i-1].row 
            col_t = self.protein_list[i].column - self.protein_list[i-1].column
            if row_t == 0 and col_t == 0:
                for j in range(len(self.protein_list)):
                    print(self.protein_list[j].row, self.protein_list[j].column)
            index = positionlist.index((row_t, col_t))
            indexlist.append(index)
        return indexlist


# Andere algoritmes

def build_grid(protein):
    if len(protein) % 2 == 0:
        grid_length = 2*len(protein)
    else:
        grid_length = 2*len(protein) + 1
    grid = np.chararray((grid_length, grid_length), itemsize = 3, unicode=True)
    grid[:] = '_'
    return grid


def check_protein(grid, Protein, protein):
    ''' We houden de eerste node bij en checken dan alle vier de hokjes
        om hem heen. Degene die de tweede node is pakken we en daarmee
        gaan we vervolgens verder om te checken wat om hem heen staat.
        Bij elke H die we gecheckt hebben voegen we deze toe aan een lijst
        zodat dubbele tellingen voorkomen worden.'''

    score = 0
    checked = []
    for i in range(len(protein)):
        row = Protein.protein_list[i].row
        col = Protein.protein_list[i].column
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

def choose_random_option(option_list):
    # kies een random row met zijn bijbehorende column uit option_list
    option = random.randint(0, (len(option_list) - 1))
    if option%2 != 0:
        option -= 1
    return option

def check_location2(option_list, row_column_list):
    # en check of deze positie al bezet is
    uni = False
    row = 0
    column = 0
    # Zolang niet een positie gevonden is
    while uni == False:
        # kies een random row met zijn bijbehorende column uit option_list
        option = choose_random_option(option_list)
        if option % 2 != 0:
            option -= 1
        # check of deze positie al bezet is
        for i in range(0, len(row_column_list), 2):
            # als postie bezet is, break
            if option_list[option] == row_column_list[i] and option_list[option+1] == row_column_list[i+1]:
                break
            # als positie vrij is, sla deze row en col op
            if i == len(row_column_list)-2: 
                uni = True
                row = option_list[option]
                column = option_list[option+1]
    return row, column

def random_structure2(p_list):
    option_list = []
    row_list = []
    column_list = []
    row_column_list = []
    switch = False
    # kies een random beginpunt in de proteine
    starting_index = random.randint(0, (len(p_list) - 1))
    idx = starting_index
    for i in range(len(p_list)+1):
        
        # eerste mag gelijk geplaatst worden   
        if i == 0:
            row_list.append(p_list[idx].row)
            column_list.append(p_list[idx].column)
            row_column_list.append(p_list[idx].row)
            row_column_list.append(p_list[idx].column)
        
        else:
            # sla de row en column van het voorgaande aminozuur tijdelijk op
            if switch == False:
                row = p_list[idx-1].row
                column = p_list[idx-1].column
            else:
                row = p_list[idx+1].row
                column = p_list[idx+1].column
            
            
            # maak een lijst met alle mogelijkheiden rondom het voorgaande aminozuur
            option_list.extend((row-1, column, row+1, column, row, column-1, row, column+1))
            
            # vind een vrije row en column om op te plaatsen
            row, column = check_location2(option_list, row_column_list)
            
            # plaats de gekozen row en column in de bijbehorden node in de p_list
            p_list[idx].row = row
            p_list[idx].column = column
            
            # plaats nieuwe row en column in row_list en column_list
            row_list.append(p_list[idx].row)
            column_list.append(p_list[idx].column)
            row_column_list.append(row)
            row_column_list.append(column)
            
            # leeg de option_list
            option_list = []
            
            # ga naar de volgende index
            if idx < len(p_list) - 1 and switch == False:
                idx += 1
            elif switch == True:
                idx -= 1 
            else:
                idx = starting_index - 1
                switch = True
    return row_list, column_list

def check_for_collision(row_list, column_list):
    for i in range(len(row_list)):
        row = row_list[i]
        column = column_list[i]
        for j in range(len(row_list) - 1 - i):
            if row == row_list[i+1+j] and column == column_list[i+1+j]:
                return False
    return True

def random_structure(p_list):
    option_list = []
    row_list = []
    column_list = []

    for i in range(len(p_list)):
        # eerste mag gelijk geplaatst worden   
        if i == 0:
            row_list.append(p_list[i].row)
            column_list.append(p_list[i].column)
        
        else:
            # bepaal row en column van voorgaande aminozuur
            row = p_list[i-1].row
            column = p_list[i-1].column
            
            # maak een lijst met alle mogelijkheiden rondom het voorgaande aminozuur
            option_list.extend((row-1, column, row+1, column, row, column-1, row, column+1))

            # kies random row en column uit die lijst
            option = choose_random_option(option_list)
            
            # plaats de gekozen row en column in de bijbehorden node in de p_list
            p_list[i].row = option_list[option]
            p_list[i].column = option_list[option+1]
            
            # plaats nieuwe row en column in row_list en column_list
            row_list.append(option_list[option])
            column_list.append(option_list[option+1])
            
            # leeg de option_list
            option_list = []
    return row_list, column_list

def grid_boundaries(max_p_list):
    lowest_row = 100
    highest_row = 0
    lowest_column = 100
    highest_column = 0
    
    for i in range(len(max_p_list)):
        if max_p_list[i].row < lowest_row:
            lowest_row = max_p_list[i].row
        if max_p_list[i].row > highest_row:
            highest_row = max_p_list[i].row
        if max_p_list[i].column < lowest_column:
            lowest_column = max_p_list[i].column
        if max_p_list[i].column > highest_column:
            highest_column = max_p_list[i].column

    return lowest_row-1, highest_row+1, lowest_column-1, highest_column+1

def print_graph(max_p_list, max_row_list, max_column_list, value_list):
    plt.style.use('seaborn-whitegrid')

    lowest_row, highest_row, lowest_column, highest_column = grid_boundaries(max_p_list)
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

def random_alg(protein):
    max_score = 0
    for i in range(100000):
        buildprotein = Protein(protein)
        p_list = buildprotein.protein_list
        row_list, column_list = random_structure(p_list)
        while check_for_collision(row_list, column_list) == False:
            row_list, column_list = random_structure(p_list)
        
        grid = build_grid(protein)
        value_list = []
        for j in range(len(p_list)):
            column = p_list[j].column
            row = p_list[j].row
            value = p_list[j].value
            value_list.append(value)
            grid[row][column] = value + str(j)
        
        score = check_protein(grid, buildprotein, protein)
        
        if score < max_score:
            max_score = score
            max_p_list = p_list
            max_row_list = row_list
            max_column_list = column_list
    
    # print(max_score)
    #print_graph(max_p_list, max_row_list, max_column_list, value_list)

def bias_random_alg(protein):
    max_score = 0
    row_list = []
    column_list = []
    for i in range(1000):
        buildprotein = Protein(protein)
        p_list = buildprotein.protein_list

        Fold = ff.Fold()
        Fold.get_fold()

        grid = build_grid(protein)
        value_list = []
        for j in range(len(p_list)):
            column = p_list[j].column
            column_list.append(column)
            row = p_list[j].row
            row_list.append(row)
            value = p_list[j].value
            value_list.append(value)
            grid[row][column] = value + str(j)

        score = check_protein(grid, buildprotein, protein)

        if score <= max_score:
            # print("====================================================================================")
            #print("=" * 24) geeft zelfde
            max_score = score
            max_p_list = p_list
            max_row_list = row_list
            max_column_list = column_list
    
    # print(max_score)
    print_graph(max_p_list, max_row_list, max_column_list, value_list)


if __name__ == "__main__":
    protein = "HHPHHHPHPHHHPH"
    for i in range(10):    
        startTime = datetime.now()
        random_alg(protein)
        print(datetime.now() - startTime)
    print("===============NEXT================")
    protein = "HPHPPHHPHPPHPHHPPHPH"
    for i in range(10):    
        startTime = datetime.now()
        random_alg(protein)
        print(datetime.now() - startTime)
    print("===============NEXT================")
    protein = "PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP"
    for i in range(10):    
        startTime = datetime.now()
        random_alg(protein)
        print(datetime.now() - startTime)
    print("===============NEXT================")
    protein = "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH"
    for i in range(10):    
        startTime = datetime.now()
        random_alg(protein)
        print(datetime.now() - startTime)
    print("===============NEXT================")
    protein = "PPCHHPPCHPPPPCHHHHCHHPPHHPPPPHHPPHPP"
    for i in range(10):    
        startTime = datetime.now()
        random_alg(protein)
        print(datetime.now() - startTime)
    print("===============NEXT================")
    protein = "CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC"
    for i in range(10):    
        startTime = datetime.now()
        random_alg(protein)
        print(datetime.now() - startTime)
    print("===============NEXT================")
    protein = "HCPHPCPHPCHCHPHPPPHPPPHPPPPHPCPHPPPHPHHHCCHCHCHCHH"
    for i in range(10):    
        startTime = datetime.now()
        random_alg(protein)
        print(datetime.now() - startTime)
    print("===============NEXT================")
    protein = "HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH"
    for i in range(10):    
        startTime = datetime.now()
        random_alg(protein)
        print(datetime.now() - startTime)
    # buildprotein = Protein(protein)
    # p_list = buildprotein.protein_list
    # row_list, column_list = random_structure2(p_list)
    # # while check_for_collision(row_list, column_list) == False:
    # #     row_list, column_list = random_structure(p_list)
    # grid = build_grid(protein)
    
    # value_list = []
    # for i in range(len(p_list)):
    #     column = p_list[i].column
    #     row = p_list[i].row
    #     value = p_list[i].value
    #     value_list.append(value)
    #     grid[row][column] = value + str(i)
    
    # score = check_protein(grid, buildprotein, protein)
    # print(score)
    # print_graph(p_list, row_list, column_list, value_list)

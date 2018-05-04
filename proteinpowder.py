import pandas as pd 
import numpy as np
import random

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
    def __init__(self, head_node = None):
        self.last = None
        self.protein_list = []
        self.first = None
        
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

    def build_protein(protein):

        ''' Dit predicaat bouwt een proteine op door per aminozuur te inserten
            in een array. Hierdoor hebben we direct al een nummer aan de verschillende
            aminozuren gehangen.
        '''
        protein_object = Protein()
        protein_length = len(protein)
        for i in range (protein_length):
            protein_object.insert(protein[i], protein_length)
        rotationlist = []
        # Hij zeurt hier om self niet kennen en ik snap niet waarom niet?
        # als we dit fixen is dit gefixt
        for i in range(1, protein_length):
            row_translation = self.protein_list[i].row - self.protein_list[i-1].row 
            col_translation = self.protein_list[i].column - self.protein_list[i-1].column
            rotation = (row_translation, col_translation)
            
            if rotation == (0, 1):
                self.protein_list[i].rotation = 0
            elif rotation == (1, 0):
                self.protein_list[i].rotatio sn = 1
            elif rotation == (0, -1):
                self.protein_list[i].rotation = 2
            elif rotation == (-1, 0):
                self.protein_list[i].rotation = 4
            else:
                self.protein_list[i].rotation = 0 #TEMP Kan niet



        return protein_object

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

    col = Protein.first.column
    row = Protein.first.row 

    score = 0
    checked = []
    
    for i in range(len(protein)):
        if 'H' in grid[row][col+i]:
            num = str(i+1)
            #kijk boven
            if 'H' in grid[row-1][col] and num not in grid[row-1][col]:
                if grid[row-1][col] not in checked:
                    score-=1
            #kijk beneden
            if 'H' in grid[row+1][col] and num not in grid[row-1][col]:
                if grid[row-1][col] not in checked:
                    score-=1
            # kijk links
            if 'H' in grid[row][col-1] and num not in grid[row-1][col]:
                if grid[row-1][col] not in checked:
                    score-=1
            # kijk rechts
            if 'H' in grid[row-1][col+1] and num not in grid[row-1][col]:
                if grid[row-1][col] not in checked:
                    score-=1
        else:
            continue
        checked.append(grid[row][col])
    return score

def choose_random_option(option_list):
    # kies een random row met zijn bijbehorende column uit option_list
    option = random.randint(0, (len(option_list) - 1))
    if option%2 != 0:
        option -= 1
    return option

def check_location(option_list, row_column_list):
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

def random_structure(p_list):
    option_list = []
    row_column_list = []
    switch = False
    # kies een random beginpunt in de proteine
    starting_index = random.randint(0, (len(p_list) - 1))
    idx = starting_index
    for i in range(len(p_list)+1):
        
        # eerste mag gelijk geplaatst worden   
        if i == 0:
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
            row, column = check_location(option_list, row_column_list)
            
            # plaats de gekozen row en column in de bijbehorden node in de p_list
            p_list[idx].row = row
            p_list[idx].column = column
            
            # plaats nieuwe row en column in row_list en column_list
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

if __name__ == "__main__":
    protein = "HHPHHHPHPHHHPH"
    grid = build_grid(protein)
    buildprotein = Protein.build_protein(protein)
    p_list = buildprotein.protein_list
    random_structure(p_list)
    for i in range(len(p_list)):
        column = p_list[i].column
        row = p_list[i].row
        value = p_list[i].value
        grid[row][column] = value + str(i)
    print(grid)
    # score = check_protein(grid, buildprotein, protein)
    # print(score)
#dict = {}
    # for i in range(len(buildprotein)):
    #     row[buildprotein[i]] = 'mynewvalue'
        
        
    

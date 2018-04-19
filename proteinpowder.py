import pandas as pd 
import numpy as np

class Node:
    def  __init__(self, value):
        ''' Initialiseert een node en vult zijn value in. Zet zijn row
            en column op none.
        '''
        self.value = value
        self.row = None
        self.column = None

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
        return protein_object

# Andere algoritmes

def build_grid(protein):
    if len(protein) % 2 == 0:
        grid_length = 2*len(protein)
    else:
        grid_length = 2*len(protein) + 1
    grid = np.chararray((grid_length, grid_length), itemsize = 2, unicode=True)
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
            #kijk boven
            if 'H' in grid[row-1][col] and i+1 not in grid[row-1][col]:
                if grid[row-1][col] not in checked:
                    score-=1
            #kijk beneden
            if 'H' in grid[row+1][col] and i+1 not in grid[row-1][col]:
                if grid[row-1][col] not in checked:
                    score-=1
            # kijk links
            if 'H' in grid[row][col-1] and i+1 not in grid[row-1][col]:
                if grid[row-1][col] not in checked:
                    score-=1
            # kijk rechts
            if 'H' in grid[row-1][col+1] and i+1 not in grid[row-1][col]:
                if grid[row-1][col] not in checked:
                    score-=1
        else:
            continue
        checked.append(grid[row][col])
    return score


if __name__ == "__main__":
    protein = "HHPHHHPH"
    grid = build_grid(protein)
    buildprotein = Protein.build_protein(protein)
    p_list = buildprotein.protein_list
    for i in range(len(p_list)):
        column = p_list[i].column
        row = p_list[i].row
        value = p_list[i].value
        grid[row][column] = value + str(i)
    print(grid)
    score = check_protein(grid, buildprotein, protein)
    print(score)
#dict = {}
    # for i in range(len(buildprotein)):
    #     row[buildprotein[i]] = 'mynewvalue'
        
        
    

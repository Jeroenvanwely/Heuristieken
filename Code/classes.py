import pandas as pd 
import numpy as np
import random
import matplotlib.pylab as plt
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import copy

class Amino:
    ''' De class Amino bevat informatie over alle afzonderlijke
        aminozuren.
    '''

    def  __init__(self, value):

        ''' Initialiseert een Amino en vult zijn value in. Zet zijn row
            en column op none. Neemt de value als argument.
        '''
        self.value = value
        self.row = None
        self.column = None
        self.rotation = None

class Protein:
    ''' De class Protein maakt een proteine object aan en zorgt dat 
        de aminozuren allemaal in een array worden gestopt. Bevat
        alle informatie over het proteine als geheel
    '''

    def __init__(self, protein_str, head_node = None):

        ''' Initialiseert een proteine object en vult deze met nodes.
            Neemt het proteine dat gebruikt wordt als string als argument.
        '''
        self.last = None
        self.protein_list = []
        self.first = None
        self.build_protein(protein_str)
        
    def insert(self, value, protein_length):

        ''' Als er nog geen laatste Amino is dan voeg er een toe en maak
            hem de laatste node. Als er wel al een laatste node is dan voeg
            een kolom verder de nieuwe node toe en maak deze node vervolgens 
            de laatste node. Neemt als argument de value van de node, en de
            lengte van het te maken proteine.
        '''

        node = Amino(value)
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
        return self

    def position(self, x):

        ''' Deze checkt wat de positie is van het huidige aminozuur ten opzichte van
            de vorige. Dus staat hij links rechts boven of onder. Deze posities worden
            omgezet naar een indexnummer. Dit nummer wordt in een lijst gezet en deze wordt
            gereturnd.
        '''

        positionlist = [(0,1), (-1,0), (0,-1), (1,0)]
        indexlist = []
        for i in range(x, len(self.protein_list)):
            row_t = self.protein_list[i].row - self.protein_list[i-1].row 
            col_t = self.protein_list[i].column - self.protein_list[i-1].column
            index = positionlist.index((row_t, col_t))
            indexlist.append(index)
        return indexlist

    def check_protein(self, grid, protein):
        ''' We houden de eerste node bij en checken dan alle vier de hokjes
            om hem heen. Degene die de tweede node is pakken we en daarmee
            gaan we vervolgens verder om te checken wat om hem heen staat.
            Bij elke H die we gecheckt hebben voegen we deze toe aan een lijst
            zodat dubbele tellingen voorkomen worden.
        '''

        score = 0
        checked = []
        for i in range(len(protein)):
            row = self.protein_list[i].row
            col = self.protein_list[i].column
            if 'H' in grid[row][col]:
                num = str(i+1)
                for j in [-1, 1]:
                    #kijk boven of beneden

                    # ALS GEKKE ERROR HEB HIWER ENTER GEDAAN IN IF STATEMENT
                    if (('H' in grid[row+j][col] or 'C' in grid[row+j][col]) 
                        and num not in grid[row+j][col] and grid[row+j][col] not in checked):
                        score-=1
                    # kijk links en rechts
                    if (('H' in grid[row][col+j] or 'C' in grid[row][col+j]) 
                        and num not in grid[row][col+j] and grid[row][col+j] not in checked):
                        score-=1
                    checked.append(grid[row][col])
            
            if 'C' in grid[row][col]:
                num = str(i+1)
                for j in [-1, 1]:
                    #kijk boven en beneden
                    if (('H' in grid[row+j][col] or 'C' in grid[row+j][col]) 
                        and num not in grid[row+j][col] and grid[row+j][col] not in checked):
                        if 'H' in grid[row+j][col]:    
                            score-=1
                        elif 'C' in grid[row+j][col]:
                            score-=5
                    # kijk links
                    if (('H' in grid[row][col+j] or 'C' in grid[row+j][col]) 
                        and num not in grid[row][col+j] and grid[row][col+j] not in checked):
                        if 'H' in grid[row][col+j]:    
                            score-=1
                        elif 'C' in grid[row][col+j]:
                            score-=5
                    checked.append(grid[row][col])
        return score

    def build_grid(protein):
        if len(protein) % 2 == 0:
            grid_length = 2*len(protein)
        else:
            grid_length = 2*len(protein) + 1
        grid = np.chararray((grid_length, grid_length), itemsize = 3, unicode=True)
        grid[:] = '_'
        return grid


class Fold:
    ''' De class fold bevat alle algoritmes die nodig zijn voor het vouwen
        van een proteine.
    '''

    def __init__(self, protein):
        self.protein = protein
        self.Protein = Protein(self.protein)
        self.grid = Protein.build_grid(self.protein)
        self.Protein.protein_list = copy.deepcopy(Protein(self.protein).protein_list)
                

    def optionlist(self, row, col, x):
        ''' Kijk boven beneden links en rechts of het vakje daar leeg is.
            Als dit zo is dan wordt dit een vouwmogelijkheid en wordt deze
            in de optielijst gevoegd. Returnt een lijst met opties van een
            specifiek aminozuur.
        '''
        optionlist = []
      
        for i in [-1, 1]:
            if '_' in self.grid[row+i][col]:
                if self.fold_check(row, col, row+i, col, x):
                    optionlist.append(row+i) 
                    optionlist.append(col)
            if '_' in self.grid[row][col+i]:
                if self.fold_check(row, col, row, col+i, x):
                    optionlist.append(row) 
                    optionlist.append(col+i)

        return optionlist

    def choose_option(self, optionlist, row, col):
        if optionlist != []:
            option = random.randint(0, (len(optionlist)-1))
            if option%2 != 0:
                option -= 1
            return optionlist[option], optionlist[option + 1]
        else:
            # print("ROW", row, col)
            return row, col

    # Deze functie checkt gegeven een bepaalde plek waar we nu zijn, en een gegeven plek
    # waar die naartoe gevouwen wordt of het mogelijk is om het proteine hierheen te vouwen.
    def fold_check(self, current_row, current_col, future_row, future_col, x):
        if future_row > current_row: 
            for i in range(1, len(self.protein) - x):
                if self.grid[future_row+i][future_col] != '_':
                    return False

        elif future_row < current_row and self.Protein.protein_list[x-1].row == self.Protein.protein_list[x].row:
            for i in range(1, len(self.protein) - x):
                if self.grid[future_row-i][future_col] != '_':
                    return False

        elif future_col > current_col:
            for i in range(1, len(self.protein) - x):
                if self.grid[future_row][future_col+i] != '_':
                    return False

        elif future_col < current_col and self.Protein.protein_list[x-1].column == self.Protein.protein_list[x].column:
            for i in range(1, len(self.protein) - x):
                if self.grid[future_row][future_col-i] != '_':
                    return False

        return True

    def amino_check(self, future_row, future_col, x):
        for i in range(x):
            if self.Protein.protein_list[i].row == future_row and self.Protein.protein_list[i].column == future_col:
                return False
        return True
            

    def fold(self, future_row, future_col, row, col, x):
        ''' Vanaf aminozuur x, het aminozuur dat gedraaid gaat worden, gaat er gekeken
            worden wat de positie van de daarop volgende aminozuren is. Eerst wordt het
            aminozuur x verplaatst naar de nieuwe positie. Dan wordt er gekeken hoeveel
            stappen (hoeken van 90 graden) deze heeft gemaakt. Deze stappen worden vervolgens
            ook toegepast op de daarop volgende aminozuren. Deze gaan dan vanaf de huidige 
            positie de stappen toepassen en dan de richting die hieruit komt wordt gemaakt
            vanaf het vorige aminozuur.
        '''

        positionlist = [(0,1), (-1,0), (0,-1), (1,0)]

        newposrow = future_row - row
        newposcol = future_col - col

        if newposrow == 0 and newposcol == 0:
            return

        indexlist = self.Protein.position(x)

        newpos = (newposrow, newposcol)
        newposindex= positionlist.index(newpos)
        steps = newposindex - indexlist[0]


        self.Protein.protein_list[x].row = future_row
        self.Protein.protein_list[x].column = future_col

    
        switch = True

        for i in range(1, len(indexlist)):
            temp_p = copy.deepcopy(self.Protein.protein_list)
            newindex = (indexlist[i] + steps) % len(positionlist)
            value = positionlist[newindex]
            newrow =  copy.copy(self.Protein.protein_list[i+x-1].row) + value[0]
            newcol =  copy.copy(self.Protein.protein_list[i+x-1].column) + value[1]
            aminolegit = self.amino_check(newrow, newcol, x+i)
            if aminolegit == False:
                optionlist = self.optionlist(self.Protein.protein_list[i+x-1].row, self.Protein.protein_list[i+x-1].column, i+x)
                newtryrow, newtrycol = self.choose_option(optionlist, self.Protein.protein_list[i+x-1].row, self.Protein.protein_list[i+x-1].column)
                self.Protein.protein_list[i+x].row = newtryrow
                self.Protein.protein_list[i+x].column = newtrycol
            else:
                self.Protein.protein_list[i+x].row = newrow
                self.Protein.protein_list[i+x].column = newcol
         

    def get_fold(self):
        for i in range(len(self.Protein.protein_list)):
                    column = self.Protein.protein_list[i].column
                    row = self.Protein.protein_list[i].row
                    value = self.Protein.protein_list[i].value
                    self.grid[row][column] = value + str(i)

        for i in range(0, len(self.Protein.protein_list)):
            if i < 1:
                continue
            else: 
                current_row = self.Protein.protein_list[i-1].row
                current_col = self.Protein.protein_list[i-1].column
                future_row, future_col = self.choose_option(self.optionlist(current_row, current_col, i), current_row, current_col)
                self.fold(future_row, future_col, current_row, current_col, i)
                self.grid = pp.build_grid(self.protein)
                for j in range(len(self.Protein.protein_list)):
                    column = self.Protein.protein_list[j].column
                    row = self.Protein.protein_list[j].row
                    value = self.Protein.protein_list[j].value
                    self.grid[row][column] = value + str(j)
        print(self.grid)
        score = pp.check_protein(self.grid, self.Protein.protein_object, self.protein) 
        print(score)

    # def hillclimber(self): #wannabe hill climber
    #     #Moet kopie van grid of van proteinlist wat?

    #     #Om 's avonds te runnen:
    #         # for j in range(10000): #TABTAB

    #         for i in range(len(self.Protein.protein_list)):
    #                 column = self.Protein.protein_list[i].column
    #                 row = self.Protein.protein_list[i].row
    #                 value = self.Protein.protein_list[i].value
    #                 self.grid[row][column] = value + str(i)

    #         for i in range(0, 50):
    #             current_grid = copy.deepcopy(self.grid)
    #             current_score = Protein.check_protein(self.grid, self.Protein, self.protein)
    #             current_p_list = copy.deepcopy(self.Protein.protein_list)
    #             j = random.randint(0, (len(self.Protein.protein_list)-1))
    #             if j <= 1:
    #                 continue
    #             else: 
    #                 current_row = self.Protein.protein_list[j-1].row
    #                 current_col = self.Protein.protein_list[j-1].column
    #                 future_row, future_col = self.choose_option(self.optionlist(current_row, current_col, j), current_row, current_col)
    #                 # print(j)
    #                 self.fold(future_row, future_col, current_row, current_col, j)
    #                 self.grid = Protein.build_grid(self.protein)
    #                 for k in range(len(self.Protein.protein_list)):
    #                     column = self.Protein.protein_list[k].column
    #                     row = self.Protein.protein_list[k].row
    #                     value = self.Protein.protein_list[k].value
    #                     self.grid[row][column] = value + str(k)
                
    #             if pp.check_protein(self.grid, self.Protein, self.protein) <= current_score:
    #                 print(i, "JOE",Protein.check_protein(self.grid, self.Protein, self.protein))
    #                 continue

    #             else:
    #                 self.grid = current_grid 
    #                 self.Protein.protein_list = current_p_list           
                
    #             print(self.grid)
    #         score = Protein.check_protein(self.grid, self.Protein, self.protein) 
    #         print(score)

import numpy as np
import random
import proteinpowder as pp
import copy
import helpers as helpe

class Fold:
    def __init__(self, protein):
        ''' Initialiseert een fold-object. Neemt een string die het proteïne representeerd
            als argument. Maakt een proteine-object aan en zet het object in een grid.
        '''
        self.protein = protein
        self.Protein = pp.Protein(self.protein)
        self.grid = helpe.insert_protein(self.Protein)
                

    def optionlist(self, row, col, x):
        ''' Optionlist neemt als argument: integers die staan voor de row en de column van het
            draaipunt en een integer die staat voor de plek in het proteine die gevouwen wordt.
            Kijkt boven, beneden, links en rechts of er een aminode staat. Zo niet wordt deze plek
            toegevoegd in een lijst. Deze lijst met opties wordt vervolgens gereturnt.
        '''

        proteinlistco = []
        for i in range(len(self.Protein.protein_list)):
            optionlist = []

            # Maakt een lijst aan met daarin de coördinaten van de aminodes.
            row_i = self.Protein.protein_list[i].row
            col_i = self.Protein.protein_list[i].column
            proteinlistco.append((row_i, col_i))
    
            # Checkt om het proteine heen voor lege plekken en sla deze op.
            for j in [-1, 1]:
                if (row+j, col) not in proteinlistco:
                    optionlist.append(row+j)
                    optionlist.append(col)
                if (row, col+j) not in proteinlistco:
                    optionlist.append(row)
                    optionlist.append(col+j)
        return optionlist

    def choose_option(self, optionlist, row, col):
        ''' Choose_option neemt een fold-object als argument, een lijst die de vouwopties
            bevat van het te vouwen aminozuur, en integers die staan voor de row en de column
            van het draaipunt. 
            Kiest, indien mogelijk, random een optie uit de lijst en returnt deze. Als dat niet
            mogelijk is wordt het draaipunt gereturnt.
        '''

        if optionlist != []:
            option = random.randint(0, (len(optionlist)-1))
            if option%2 != 0:
                option -= 1
            return optionlist[option], optionlist[option + 1]
        else:
           return row, col


    def amino_check(self, future_row, future_col, x):
        ''' Amino_check neemt een fold-object als argument, integers die staan voor de row en column
            waar aminode x naartoe gevouwen wordt, en een integer x die staat voor de plek van het 
            aminozuur in het proteïne. 
            Er wordt gecheckt of de plek waar naartoe gevouwen wordt al eerder voorkomt in het proteiïne.
            Er wordt een boolean terug gegeven.
        '''

        for i in range(x):
            if self.Protein.protein_list[i].row == future_row and self.Protein.protein_list[i].column == future_col:
                return False
        return True
            

    def fold(self, future_row, future_col, row, col, x):
        ''' Fold neemt als argument een fold object, integers die staan voor de row en de column 
            van de plek waar aminozuur x naartoe wordt gevouwen, integers die staan voor 
            de row en de column van het draaipunt en een integer x die staat voor de plek van het
            aminozuur in het proteïne.
            Er wordt bepaald wat de rotatie is die de vouwing maakt ten opzichte van de vorige positie
            en op basis hiervan wordt, indien mogelijk, het gehele proteïne gevouwen. Dit wordt gedaan
            door aanpassingen te maken in de protein_list.
        '''

        # Bepaal de rotatie die de nieuwe vouwing vanaf de vorige positie maakt.
        positionlist = [(0,1), (-1,0), (0,-1), (1,0)]
        newposrow = future_row - row
        newposcol = future_col - col
        if newposrow == 0 and newposcol == 0:
            return
        indexlist = self.Protein.position(x)
        newpos = (newposrow, newposcol)
        newposindex= positionlist.index(newpos)
        steps = newposindex - indexlist[0]

        # Onthou beginstaat
        begin_conf = copy.deepcopy(self.Protein.protein_list)
        begin_grid = copy.deepcopy(self.grid)

        # Vouw de eerste aminodes naar nieuwe positie
        self.Protein.protein_list[x].row = future_row
        self.Protein.protein_list[x].column = future_col

        # Vouw de daar op volgende aminodes door middel van de steps toe te passen op de vorige positie.
        for i in range(1, len(indexlist)):
            newindex = (indexlist[i] + steps) % len(positionlist)
            value = positionlist[newindex]
            newrow =  copy.copy(self.Protein.protein_list[i+x-1].row) + value[0]
            newcol =  copy.copy(self.Protein.protein_list[i+x-1].column) + value[1]
            # Is er overlap tussen de nieuwe vouwing en vorige aminozuur, wijzig dan indien mogelijk de vouwing.
            aminolegit = self.amino_check(newrow, newcol, x+i)
            if aminolegit == False:
                optionlist = self.optionlist(self.Protein.protein_list[i+x-1].row, self.Protein.protein_list[i+x-1].column, i+x)
                if optionlist == []:
                    self.Protein.protein_list = copy.deepcopy(begin_conf)
                    return
                newtryrow, newtrycol = self.choose_option(optionlist, self.Protein.protein_list[i+x-1].row, self.Protein.protein_list[i+x-1].column)
                self.Protein.protein_list[i+x].row = newtryrow
                self.Protein.protein_list[i+x].column = newtrycol
            else:
                self.Protein.protein_list[i+x].row = newrow
                self.Protein.protein_list[i+x].column = newcol

    def random_fold(self):
        ''' Random_fold neemt een fold object als argument. Er wordt een aanpassing 
            gemaakt op een random plek in het proteïne naar een random vouwoptie.
            Het geturnt het grid als numpy array, een integer die voor de score staat
            en een proteinlist met Aminode objecten in een lijst.
        '''

        # Maak kopie van huidige staat voor latere vergelijkingen.
        current_grid = copy.deepcopy(self.grid)
        current_score = helpe.check_protein(self.grid, self.Protein)
        current_p_list = copy.deepcopy(self.Protein.protein_list)
        
        # Kies een random plek om te vouwen en kies een random optie om naar te vouwen.
        j = random.randint(2, (len(self.Protein.protein_list)-1))
        current_row = self.Protein.protein_list[j-1].row
        current_col = self.Protein.protein_list[j-1].column
        future_row, future_col = self.choose_option(self.optionlist(current_row, current_col, j), current_row, current_col)

        # Vouw en zet in het grid.
        self.fold(future_row, future_col, current_row, current_col, j)
        self.grid = helpe.insert_protein(self.Protein)

        return current_grid, current_score, current_p_list 



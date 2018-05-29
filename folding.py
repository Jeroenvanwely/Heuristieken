import pandas as pd 
import numpy as np
import random
import proteinpowder as pp
import copy
import math
import helpers as helpe


class Fold:
    def __init__(self, protein):
        self.protein = protein
        self.Protein = pp.Protein(self.protein)
        self.grid = helpe.insert_protein(self.Protein)
                

    def optionlist(self, row, col, x):
        optionlist = []
        proteinlistco = []

        for i in range(len(self.Protein.protein_list)):
            optionlist = []
            row_i = self.Protein.protein_list[i].row
            col_i = self.Protein.protein_list[i].column
            proteinlistco.append((row_i, col_i))
    
            for j in [-1, 1]:
                if (row+j, col) not in proteinlistco:
                    optionlist.append(row+j)
                    optionlist.append(col)
                if (row, col+j) not in proteinlistco:
                    optionlist.append(row)
                    optionlist.append(col+j)

        return optionlist

    def choose_option(self, optionlist, row, col):
        if optionlist != []:
            option = random.randint(0, (len(optionlist)-1))
            if option%2 != 0:
                option -= 1
            return optionlist[option], optionlist[option + 1]
        else:
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
       # print("x", self.Protein.protein_list[x].row, self.Protein.protein_list[x].column)
        for i in range(x):
            # print(self.Protein.protein_list[i].row, self.Protein.protein_list[i].column)
            if self.Protein.protein_list[i].row == future_row and self.Protein.protein_list[i].column == future_col:
                # print("HOI")
                return False
        return True
            

    def fold(self, future_row, future_col, row, col, x):


        #HELP HIJ DOET SOMS DUS NOG DIE FOUT DAT HIJ (0,0) NIET IN DE LIJST HEEFT

        ''' Vanaf aminozuur x, het aminozuur dat gedraaid gaat worden, gaat er gekeken
            worden wat de positie van de daarop volgende aminozuren is. Eerst wordt het
            aminozuur x verplaatst naar de nieuwe positie. Dan wordt er gekeken hoeveel
            stappen (hoeken van 90 graden) deze heeft gemaakt. Deze stappen worden vervolgens
            ook toegepast op de daarop volgende aminozuren. Deze gaan dan vanaf de huidige 
            positie de stappen toepassen en dan de richting die hieruit komt wordt gemaakt
            vanaf het vorige aminozuur.
        '''

        # DRAMA : er is soms een aminozuur op dezelfde plek?????

        positionlist = [(0,1), (-1,0), (0,-1), (1,0)] #draaiing

        newposrow = future_row - row
        newposcol = future_col - col

        if newposrow == 0 and newposcol == 0:
            return

        indexlist = self.Protein.position(x) #HIER? er wordt hier een x meegegeven die op dezelfde plek als het eerdere aminozuur staat
        # if indexlist == 5:
        #     return
        newpos = (newposrow, newposcol)
        newposindex= positionlist.index(newpos)

        # print(indexlist)
        steps = newposindex - indexlist[0]


        begin_conf = copy.deepcopy(self.Protein.protein_list)
        begin_grid = copy.deepcopy(self.grid)

        self.Protein.protein_list[x].row = future_row
        self.Protein.protein_list[x].column = future_col

    
        switch = True
    
        # print(self.grid)

        for i in range(1, len(indexlist)):
            temp_p = copy.deepcopy(self.Protein.protein_list)
            newindex = (indexlist[i] + steps) % len(positionlist)
            # print(newindex, "new index")
            value = positionlist[newindex]
            # print("value", value)
            newrow =  copy.copy(self.Protein.protein_list[i+x-1].row) + value[0]
            newcol =  copy.copy(self.Protein.protein_list[i+x-1].column) + value[1]
            aminolegit = self.amino_check(newrow, newcol, x+i)
            # hier hebben we toch ervoor gezorgd dat hij nooit over elkaar geplaats kan worden?
            if aminolegit == False:
                # print("DJSodjvoiwdvnidnvwVDNVKvwed") #if optionlist is niet leeg
                optionlist = self.optionlist(self.Protein.protein_list[i+x-1].row, self.Protein.protein_list[i+x-1].column, i+x)
                if optionlist == []:
                    self.Protein.protein_list = copy.deepcopy(begin_conf)
                    # self.grid = begin_grid
                    return
                # print(optionlist, "optionlist")
                newtryrow, newtrycol = self.choose_option(optionlist, self.Protein.protein_list[i+x-1].row, self.Protein.protein_list[i+x-1].column)
                # print(newtryrow, newtrycol)
                self.Protein.protein_list[i+x].row = newtryrow
                self.Protein.protein_list[i+x].column = newtrycol
            else:
                self.Protein.protein_list[i+x].row = newrow
                self.Protein.protein_list[i+x].column = newcol

        # pp.print_graph2(self.Protein.protein_list)
        # print("new fold")
        # for i in range(len(self.Protein.protein_list)):
        #     print(self.Protein.protein_list[i].row, self.Protein.protein_list[i].column)
        # # print(self.grid)

    def random_fold(self):
        # Maak kopie van huidige staat voor latere vergelijkingen
        current_grid = copy.deepcopy(self.grid)
        current_score = helpe.check_protein(self.grid, self.Protein)
        current_p_list = copy.deepcopy(self.Protein.protein_list)
        
        # Kies een random plek om te vouwen en kies een random optie om naar te vouwen
        j = random.randint(2, (len(self.Protein.protein_list)-1))
        current_row = self.Protein.protein_list[j-1].row
        current_col = self.Protein.protein_list[j-1].column
        future_row, future_col = self.choose_option(self.optionlist(current_row, current_col, j), current_row, current_col)

        # Vouw en zet in het grid
        self.fold(future_row, future_col, current_row, current_col, j)
        self.grid = helpe.insert_protein(self.Protein)

        return current_grid, current_score, current_p_list

    def getgetfold(self):
        muts = []
        original = copy.deepcopy(self.Protein.protein_list)
        for i in range(0, len(self.Protein.protein_list)):
            if i < 1:
                continue
            else: 
                current_row = self.Protein.protein_list[i-1].row
                current_col = self.Protein.protein_list[i-1].column
                optionlist = self.optionlist(current_row, current_col, i)
                for j in range(len(optionlist)):
                    if j % 2 == 0:
                        self.fold(optionlist[j], optionlist[j+1], current_row, current_col, i)
                        mutation = copy.deepcopy(self.Protein.protein_list)
                        muts.append(mutation)
                        self.Protein.protein_list = original
                    else:
                        continue
        return muts


                    
        #         self.fold(future_row, future_col, current_row, current_col, i)
        #         self.grid = pp.build_grid(self.protein)
        #         for j in range(len(self.Protein.protein_list)):
        #             column = self.Protein.protein_list[j].column
        #             row = self.Protein.protein_list[j].row
        #             value = self.Protein.protein_list[j].value
        #             self.grid[row][column] = value + str(j)
        # print(self.grid)
        # score = pp.check_protein(self.grid, self.Protein.protein_object, self.protein) 
        # print(score)     

    def get_fold(self):
        self.get_straight()

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
    # #Moet kopie van grid of van proteinlist wat?

    # #Om 's avonds te runnen:
    #     # for j in range(10000): #TABTAB

    #     for i in range(len(self.Protein.protein_list)):
    #             column = self.Protein.protein_list[i].column
    #             row = self.Protein.protein_list[i].row
    #             value = self.Protein.protein_list[i].value
    #             self.grid[row][column] = value + str(i)

    #     for i in range(0, 100):
    #         # print(self.grid)
    #         current_grid = copy.deepcopy(self.grid)
    #         current_score = pp.check_protein(self.grid, self.Protein, self.protein)
    #         current_p_list = copy.deepcopy(self.Protein.protein_list)
    #         j = random.randint(0, (len(self.Protein.protein_list)-1))
    #         if j <= 1:
    #             continue
    #         else: 
    #             current_row = self.Protein.protein_list[j-1].row
    #             current_col = self.Protein.protein_list[j-1].column
    #             future_row, future_col = self.choose_option(self.optionlist(current_row, current_col, j), current_row, current_col)
    #             # print(j)
    #             self.fold(future_row, future_col, current_row, current_col, j)
    #             self.grid = pp.build_grid(self.protein)
    #             for k in range(len(self.Protein.protein_list)):
    #                 column = self.Protein.protein_list[k].column
    #                 row = self.Protein.protein_list[k].row
    #                 value = self.Protein.protein_list[k].value
    #                 self.grid[row][column] = value + str(k)
            
    #         if pp.check_protein(self.grid, self.Protein, self.protein) <= current_score:
    #             # print(i, "JOE",pp.check_protein(self.grid, self.Protein, self.protein))
    #             continue

    #         else:
    #             self.grid = current_grid 
    #             self.Protein.protein_list = current_p_list           
            
    #     score = pp.check_protein(self.grid, self.Protein, self.protein) 
    #     print(score)

    # def sim_anneal(self, protein):
    #     ''' Ti = T0 - i(T0-Tn) / N
    #         Kan ik i als temp gebruiken? denk dat dit handig is
    #         T0 is iets van count die hoog staat
    #         De begintemp kies je zo dat op iedere verslechtering de kans 1 is
    #     '''

    #     self.hillclimber()
    #     score = pp.check_protein(self.grid, self.Protein, self.protein) 
    #     print(score)
        

    #     T0 = 1000
    #     Tn = 1
    #     N = 100
    #     # Tk = T0 - (0.9 * k)

    #     for i in range(len(self.Protein.protein_list)):
    #             column = self.Protein.protein_list[i].column
    #             row = self.Protein.protein_list[i].row
    #             value = self.Protein.protein_list[i].value
    #             self.grid[row][column] = value + str(i)

    #     for i in range(0, 10):
    #         current_grid = copy.deepcopy(self.grid)
    #         current_score = pp.check_protein(self.grid, self.Protein, self.protein)
    #         current_p_list = copy.deepcopy(self.Protein.protein_list)
    #         j = random.randint(0, (len(self.Protein.protein_list)-1))
    #         if j <= 1:
    #             continue
    #         else: 
    #             current_row = self.Protein.protein_list[j-1].row
    #             current_col = self.Protein.protein_list[j-1].column
    #             future_row, future_col = self.choose_option(self.optionlist(current_row, current_col, j), current_row, current_col)
    #             # print(j)
    #             self.fold(future_row, future_col, current_row, current_col, j)
    #             self.grid = pp.build_grid(self.protein)
    #             for k in range(len(self.Protein.protein_list)):
    #                 column = self.Protein.protein_list[k].column
    #                 row = self.Protein.protein_list[k].row
    #                 value = self.Protein.protein_list[k].value
    #                 self.grid[row][column] = value + str(k)
            
    #         if pp.check_protein(self.grid, self.Protein, self.protein) <= current_score:
    #             # print(i, "JOE",pp.check_protein(self.grid, self.Protein, self.protein))
    #             continue

    #         else:
    #             score_difference = pp.check_protein(self.grid, self.Protein, self.protein) - current_score
    #             score_calc = score_difference * 100
    #             temperature = T0 - (i*(T0 - Tn))/ N
    #             prob = math.exp(-score_calc / temperature)
    #             print(score_difference, prob)
    #             if prob > 0.5:
    #                 continue
    #             else:
    #                 self.grid = current_grid 
    #                 self.Protein.protein_list = current_p_list           
            
    #         # print(self.grid)
    #     score = pp.check_protein(self.grid, self.Protein, self.protein) 
        # return score



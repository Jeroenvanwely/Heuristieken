import helpers as hp
import proteinpowder as pp

import os

def check_for_collision(row_list, column_list):
    ''' Check_for_collision neemt twee lijsten met de row and column coördinaten 
        van het proteïne als argument. Aan de hand van deze lijsten word er gekeken 
        of er combinaties zijn van row's en columns die vaker voorkomen. Returned 
        False als er collisions zijn en True als die er niet zijn.
    '''

    for i in range(len(row_list)):
        # Sla locatie van aminzouur i op
        row = row_list[i]
        column = column_list[i]
        # Check of deze locatie ook tot een volgend aminozuur behoord
        for j in range(len(row_list) - 1 - i):
            if row == row_list[i+1+j] and column == column_list[i+1+j]:
                return False
    return True

def random_structure(pro_obj):
    ''' Random_structure neemt een proteïne object als argument en plaatst in een 
        random structuur. Elk aminozuur wordt onafhankelijk van alle andere 
        aminozuren geplaats behalve zijn vooraande, omdat hij rondom deze geplaatst 
        moet worden. Returnt een row_list en column_list, die de coördinaten van de 
        aminzouren bevatten.
    '''
    
    option_list = []
    row_list = []
    column_list = []

    for i in range(len(pro_obj.protein_list)):
        # Plaatsing van eerste twee aminozuren staat vast
        if i == 0 or i == 1:
            if i == 1:
                pro_obj.protein_list[i].row = pro_obj.protein_list[0].row
                pro_obj.protein_list[i].column = pro_obj.protein_list[0].column + 1
            row_list.append(pro_obj.protein_list[i].row)
            column_list.append(pro_obj.protein_list[i].column)

        else:
            # plaats aminozuur op random keuze uit plaatsingsmogelijkheden rondom het voorgaande aminozuur
            row = pro_obj.protein_list[i-1].row
            column = pro_obj.protein_list[i-1].column
            option_list.extend((row-1, column, row+1, column, row, column-1, row, column+1))
            option = hp.choose_random_option(option_list)
            pro_obj.protein_list[i].row = option_list[option]
            pro_obj.protein_list[i].column = option_list[option+1]
            row_list.append(option_list[option])
            column_list.append(option_list[option+1])
            option_list = []
    return row_list, column_list

def random_structure_without_collision(protein):
    ''' Random_structure_without_collision neemt een proteïne string als argument
        en maakt van dit proteïne een random structuur zonder collisions. Returnt
        een proteïne object
    '''
    
    pro_obj = pp.Protein(protein)
    # Maak random structuur, zolang deze collisions heeft probeer opnieuw.
    row_list, column_list = random_structure(pro_obj)
    while check_for_collision(row_list, column_list) == False:
        row_list, column_list = random_structure(pro_obj)
    
    grid = hp.insert_protein(pro_obj)
    score = hp.check_protein(grid, pro_obj)
    return score  

if __name__ == "__main__":
    proteinlist = ["HHPHHHPHPHHHPH", "HPHPPHHPHPPHPHHPPHPH", "PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP", "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH", "PPCHHPPCHPPPPCHHHHCHHPPHHPPPPHHPPHPP", "CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC", "HCPHPCPHPCHCHPHPPPHPPPHPPPPHPCPHPPPHPHHHCCHCHCHCHH", "HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH"]
    for i in range(len(proteinlist)):
        for j in range(30):
            score = random_structure_without_collision(proteinlist[i])
            results = os.path.abspath('Results/random_sampling/rs_results' +str(i) + '.csv') 
            with open(results, 'a') as data: #add data
                data.write(str(score) + '\n')

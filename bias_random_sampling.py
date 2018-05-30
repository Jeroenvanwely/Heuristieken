import helpers as hp
import proteinpowder as pp
import os

def make_option_list(row, column, pro_obj):
    potential_option_list = []  
    option_list = []  
    potential_option_list.extend((row-1, column, row+1, column, row, column-1, row, column+1))
    for j in range(0, len(potential_option_list), 2):
        switch = True
        for k in range(len(pro_obj.protein_list)):
            if potential_option_list[j] == pro_obj.protein_list[k].row and potential_option_list[j+1] == pro_obj.protein_list[k].column:
                switch = False
        if switch == True:
            option_list.append(potential_option_list[j])
            option_list.append(potential_option_list[j+1])
    return option_list


def bias_random_structure(proteinlist):
    ''' Random_structure neemt een proteïne object als argument en plaatst deze in een 
        random structuur. Elk aminozuur wordt geplaatst rondom zijn voorgaande 
        aminzouur op een locatie die vrij is. Returnt twee lijsten met de row en column
        coördinaten van de aminozuren.
    '''
    pro_obj = pp.Protein(proteinlist)
    for j in range(len(pro_obj.protein_list)):
        # Plaatsing van eerste twee aminozuren staat vast
        if j == 0 or j == 1:
            if j == 1:
                pro_obj.protein_list[j].row = pro_obj.protein_list[0].row
                pro_obj.protein_list[j].column = pro_obj.protein_list[0].column + 1

        else:
            # Plaats aminozuur op random keuze uit plaatsingsmogelijkheden rondom het voorgaande aminozuur
            row = pro_obj.protein_list[j-1].row
            column = pro_obj.protein_list[j-1].column
            option_list = make_option_list(row, column, pro_obj)
            if len(option_list) == 0:
                return False
            else:    
                option = hp.choose_random_option(option_list)
                pro_obj.protein_list[j].row = option_list[option]
                pro_obj.protein_list[j].column = option_list[option+1]        
    grid = hp.insert_protein(pro_obj)
    score = hp.check_protein(grid, pro_obj)
    return score


if __name__ == "__main__":
    proteinlist = ["HHPHHHPHPHHHPH", "HPHPPHHPHPPHPHHPPHPH", "PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP", "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH", "PPCHHPPCHPPPPCHHHHCHHPPHHPPPPHHPPHPP", "CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC", "HCPHPCPHPCHCHPHPPPHPPPHPPPPHPCPHPPPHPHHHCCHCHCHCHH", "HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH"]
    for i in range(len(proteinlist)):
        for j in range(30):
            score = bias_random_structure(proteinlist[i])
            while score == False:
                score = bias_random_structure(proteinlist[i])
            # results = os.path.abspath('Results/bias_random_sampling/brs_results' +str(i) + '.csv') 
            # with open(results, 'a') as data: #add data
            #     data.write(str(score) + '\n')
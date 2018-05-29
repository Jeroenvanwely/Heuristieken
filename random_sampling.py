import helpers as hp
import proteinpowder as pp

def check_for_collision(row_list, column_list):
    for i in range(len(row_list)):
        row = row_list[i]
        column = column_list[i]
        for j in range(len(row_list) - 1 - i):
            if row == row_list[i+1+j] and column == column_list[i+1+j]:
                return False
    return True

def random_structure(pro_obj):
    option_list = []
    row_list = []
    column_list = []

    for i in range(len(pro_obj.protein_list)):
        # eerste mag gelijk geplaatst worden   
        if i == 0:
            row_list.append(pro_obj.protein_list[i].row)
            column_list.append(pro_obj.protein_list[i].column)
        
        else:
            # bepaal row en column van voorgaande aminozuur
            row = pro_obj.protein_list[i-1].row
            column = pro_obj.protein_list[i-1].column
            
            # maak een lijst met alle mogelijkheiden rondom het voorgaande aminozuur
            option_list.extend((row-1, column, row+1, column, row, column-1, row, column+1))

            # kies random row en column uit die lijst
            option = hp.choose_random_option(option_list)
            
            # plaats de gekozen row en column in de bijbehorden node in de p_list
            pro_obj.protein_list[i].row = option_list[option]
            pro_obj.protein_list[i].column = option_list[option+1]
            
            # plaats nieuwe row en column in row_list en column_list
            row_list.append(option_list[option])
            column_list.append(option_list[option+1])
            
            # leeg de option_list
            option_list = []
    return row_list, column_list

def random_structure_without_collision(protein):
    pro_obj = pp.Protein(protein)
    row_list, column_list = random_structure(pro_obj)
    while check_for_collision(row_list, column_list) == False:
        row_list, column_list = random_structure(pro_obj)
    return pro_obj    

if __name__ == "__main__":
    protein = "HHPHHHPHPHHHPH"  
    pro_obj = random_structure_without_collision(protein)
    print(hp.check_protein(hp.insert_protein(pro_obj), pro_obj))
    hp.print_graph(pro_obj)

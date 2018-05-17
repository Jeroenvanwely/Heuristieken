import pandas as pd 
import numpy as np
import random
import proteinpowder as pp
import random
import copy
import folding as ff

# def fold(self, future_row, future_col, row, col, x):
#         for i in range(0, len(self.protein) - x):
#             if future_row > row:
#                 for i in range(0, len(self.protein) - x):
#                     self.p_list[x+i].row = future_row+i
#                     self.p_list[x+i].column = future_col
#                     print("1", row, col, future_row+i, future_col) 

#             elif future_row < row and self.p_list[x-1].row == self.p_list[x].row:
#                 for i in range(0, len(self.protein) - x):
#                     self.p_list[x+i].row = future_row-i
#                     self.p_list[x+i].column = future_col
#                     print("2", row, col, future_row-i, future_col)

#             elif future_col > col:
#                 for i in range(0, len(self.protein) - x):
#                     self.p_list[x+i].row = future_row
#                     self.p_list[x+i].column = future_col+i
#                     print("3", row, col, future_row, future_col+i)
                    
#             elif future_col < col and self.p_list[x-1].column == self.p_list[x].column:
#                 for i in range(0, len(self.protein) - x):
#                     self.p_list[x+i].row = future_row
#                     self.p_list[x+i].column = future_col-i
#                     print("4", row, col, future_row, future_col-i)


if __name__ == "__main__":
    Fold = ff.Fold()
    Fold.random_fold()


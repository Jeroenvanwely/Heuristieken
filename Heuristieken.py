import proteinpowder as pp
import folding as ff

class Depth:

    def __init__(self, fold):
        self.stack = []
        self.fold = fold
        self.depth_first()

    def depth_first(self):
        self.stack.append(self.fold)
        listy  = self.fold.getgetfold()
        for i in range(len(listy)):
            for j in range(len(listy[i])):
                column = listy[i][j].column
                row = listy[i][j].row
                value = listy[i][j].value
                self.fold.grid[row][column] = value + str(j)
    
if __name__ == "__main__":
   
    fold = ff.Fold()
    fold.get_straight()
    print(fold.grid)
    d = Depth(fold)
        # #rechte proteine
        # d = Depth()
        # d.depth_first()
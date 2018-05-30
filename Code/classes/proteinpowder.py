import pandas as pd 
import numpy as np
import random
import matplotlib.pylab as plt
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import folding as ff
from datetime import datetime


class Aminode:
    def  __init__(self, value):
        ''' Initialiseert een node en vult zijn value in. Neemt een string
            als argument.
        '''
        self.value = value
        self.row = None
        self.column = None

class Protein:
    def __init__(self, protein_str, head_node = None):
        ''' Initialiseert een proteine object vult alle aminodes in. Neemt een
            string als argument.
        '''
        self.last = None
        self.protein_list = []
        self.first = None
        self.build_protein(protein_str)
     
    def insert(self, value, protein_length):

        ''' Als er nog geen laatste node is dan voeg er een toe en maak
            hem de laatste node. Als er wel al een laatste node is dan voeg
            een kolom verder de nieuwe node toe en maak deze node vervolgens 
            de laatste node.
        '''
        node = Aminode(value)
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


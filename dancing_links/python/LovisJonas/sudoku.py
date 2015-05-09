'''
Created on 08.05.2015

@author: lovis
'''
import copy

def modulo(x,y):
    res = x
    while res > y-1:
        res -= y
    return res


def cal_square(row,column):
        modrow = modulo(row,3)
        modcol = modulo(column,3)
        if modrow == 0:
            square = modcol
        elif modrow == 1:
            square = 3+modcol
        else:
            square = 6+modcol
 
def sudokuListHeaders(givenSudoku):
        names=[]
        for row in range(9) :
            for column in range(9) :
                for value in range(1,10):
                    if [row,column,value] not in givenSudoku:
                        names.append(str(row)+str(column))
                
        for square in range(9) :
                for value in range(1,10):
                        if [row,column,value] not in givenSudoku:
                            
                            names.append("r"+str(row)+str(value))
                            names.append("c"+str(column)+str(value))
                            names.append("sq"+str(cal_square(row,column))+str(value))
                            
        
        return names    
    
       
class Sudoku(object):
    
    def __init__(self,values):
        pass
        '''self.values = values
        for row in range(9) :
            for column in range(9) :
        '''
                    
                    

        
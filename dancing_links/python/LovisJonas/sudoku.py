'''
Created on 08.05.2015

@author: lovis
'''
import copy
import math

def cal_square(row,column):
        if row < 3:
            square = math.floor(column/3)
        if 2 < row < 6:
            square = math.floor(column/3)+3
        if 5 < row < 9:
            square = math.floor(column/3)+6
        return square
 
def sudokuListHeaders(givenSudoku):
        names=[]
        reminder_cood=1
        reminder_row=1
        reminder_column=1
        reminder_sq=1
        
        for row in range(9):
            for column in range(9) :
                for value in range(1,10) :
                    if [row,column,value] in givenSudoku:
                        reminder_cood=0
                    if value==9:
                        if reminder_cood==1:
                            names.append(str(row)+str(column))
                reminder_cood=1
                        
        for value in range(1,10):
            for row in range(9):
                for column in range(9):
                    if [row,column,value] in givenSudoku:
                        reminder_row=0
                    if column==8 :
                        if reminder_row==1:
                            names.append("r"+str(row)+str(value))
                reminder_row=1
                        
        for value in range(1,10) :
            for column in range(9):
                for row in range(9): 
                    if [row,column,value] in givenSudoku:
                        reminder_column=0
                    if row==8 :
                        if reminder_column==1:
                            names.append("c"+str(column)+str(value))
                reminder_column=1
            
    
        for value in range(1,10):             
            for row in range (3):
                for column in range(3):
                    if [row, column, value] in givenSudoku:
                        reminder_sq=0
                    if column==2 and row==2 and reminder_sq==1:
                        names.append("sq"+str(cal_square(row,column))+str(value))
            reminder_sq=1
                    
        for value in range(1,10):
            for row in range (3,6):
                for column in range(3):
                    if [row, column, value] in givenSudoku:
                        reminder_sq=0
                    if column==2 and row==5 and reminder_sq==1:
                        names.append("sq"+str(cal_square(row,column))+str(value))
            reminder_sq=1
                    
        for value in range(1,10):                
            for row in range (6,9):
                for column in range(3):
                    if [row, column, value] in givenSudoku:
                        reminder_sq=0
                    if column==2 and row==8 and reminder_sq==1:
                        names.append("sq"+str(cal_square(row,column))+str(value))
            reminder_sq=1
                    
        for value in range(1,10):
            for row in range (3):
                for column in range(3,6):
                        if [row, column, value] in givenSudoku:
                            reminder_sq=0
                        if column==5 and row==2 and reminder_sq==1:
                            names.append("sq"+str(cal_square(row,column))+str(value))
            reminder_sq=1
                            
        for value in range(1,10):
            for row in range (3,6):
                for column in range(3,6):
                    if [row, column, value] in givenSudoku:
                        reminder_sq=0
                    if column==5 and row==5 and reminder_sq==1:
                        names.append("sq"+str(cal_square(row,column))+str(value))
            reminder_sq=1
                        
        for value in range(1,10):               
            for row in range (6,9):
                for column in range(3,6):
                    if [row, column, value] in givenSudoku:
                        reminder_sq=0
                    if column==5 and row==8 and reminder_sq==1:
                        names.append("sq"+str(cal_square(row,column))+str(value))
            reminder_sq=1
                        
        for value in range(1,10):                
            for row in range (3):
                for column in range(6,9):
                    if [row, column, value] in givenSudoku:
                        reminder_sq=0
                    if column==8 and row==2 and reminder_sq==1:
                        names.append("sq"+str(cal_square(row,column))+str(value))
            reminder_sq=1
                    
        for value in range(1,10):            
            for row in range (3,6):
                for column in range(6,9):
                    if [row, column, value] in givenSudoku:
                        reminder_sq=0
                    if column==8 and row==5 and reminder_sq==1:
                        names.append("sq"+str(cal_square(row,column))+str(value))
            reminder_sq=1
                    
        for value in range(1,10):           
            for row in range (6,9):
                for column in range(6,9):
                    if [row, column, value] in givenSudoku:
                        reminder_sq=0
                    if column==8 and row==8 and reminder_sq==1:
                        names.append("sq"+str(cal_square(row,column))+str(value))
            reminder_sq=1
        
        return names
    

        
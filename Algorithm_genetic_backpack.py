# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 18:10:22 2018

@author: Sergio Campos
"""
# Libraries
import pandas as pd
import numpy as np
import random

# Arguments
pct_mut = 0.05
n_pob = 100
epochs = 10
n_select = 50
n_part = 2
objets = 10
weight = 50

# Function to create aleatory table of 0`s and 1`s about the objects
def Initializer(n_pob, objets):

    # Create vector with names of objects
    names = []
    for i in range(0, objets):
        names.append("Obj_" + str(i + 1))

    # Create data frame with random numbers
    table = pd.DataFrame(np.random.randint(2, size=(n_pob, objets)), columns=list(names))
    
    return table

# Function to evaluate every individaul about our objetive, we want the benefict of every elements
def Fitness(table):

    # Dictionary with name of object the weight and benefic 
    # Objective: max benefic without pass the weight
    dic = {"Obj_1":[5,3], "Obj_2":[3,5], "Obj_3":[5,2], "Obj_4":[1,8], "Obj_5":[2,3],
           "Obj_6":[4,5], "Obj_7":[1,7], "Obj_8":[2,5], "Obj_9":[5,1], "Obj_10":[3,8]}
    table["Point"] = 0
    for row in range(len(table)):
        
        total_weight = 0
        total_benefic = 0
        
        for col in range(0, len(table.columns) - 1): 
            
            if table.iloc[row, col] == 1:
                total_weight = total_weight + int(list(dic.values())[col][0])
                total_benefic = total_benefic + int(list(dic.values())[col][1])
            
        table.iloc[row, int(len(table.columns)) - 1] = total_benefic if total_weight <= weight else 0
        table = table.sort_values(by = 'Point', ascending = False)

    return table    

# Function to select individuals with better fitness 
def Selection(table):
    
    table_select_final = []
    # Take two first elements with more fitness
    if type(table_select_final) == list: 
        table_select_final = table.head(2)
    table_select = table.drop(table_select_final.index)
    
    # Between the rest element we take randomly the rest of elements
    while len(table_select_final) < n_select:
        table_index = table_select.iloc[[random.randrange(0,len(table_select)), random.randrange(0,len(table_select))],:]
        if table_index.iloc[0]['Point'] > table_index.iloc[1]['Point']:
            table_select_final = table_select_final.append(table_index.iloc[0,:])
        elif table_index.iloc[0]['Point'] == table_index.iloc[1]['Point']:
            table_select_final = table_select_final.append(table_index.iloc[random.randint(0,1),:])
        else:
            table_select_final = table_select_final.append(table_index.iloc[1,:])
        
        table_select_final.reset_index(drop=True, inplace=True)

    return table_select_final

# Function to mix the genetic material
def Crossovery(table):

    table_crossovery = []
    # Between elemenst of the table select we take two elements and mix it
    while len(table_crossovery) < n_pob - len(table):
        table_cross = table.iloc[[random.randrange(0,len(table)), random.randrange(0,len(table))],:]
        table_1 = table_cross.iloc[:, 0:int((len(table.columns) - 1) / n_part)].iloc[[0]]
        table_1.reset_index(drop=True, inplace=True)
        table_2 = table_cross.iloc[:, int((len(table.columns) - 1) / n_part):len(table.columns) -1].iloc[[1]]
        table_2.reset_index(drop=True, inplace=True)
        table_12 = pd.concat([table_1, table_2], axis=1)
        table_12["Point"] = 0
        dic = {"Obj_1":[5,3], "Obj_2":[3,5], "Obj_3":[5,2], "Obj_4":[1,8], "Obj_5":[2,3],
               "Obj_6":[4,5], "Obj_7":[1,7], "Obj_8":[2,5], "Obj_9":[5,1], "Obj_10":[3,8]}
    
        total_weight = 0
        total_benefic = 0
        
        for col in range(0, len(table.columns) - 1): 
            
            if table.iloc[0, col] == 1:
                total_weight = total_weight + int(list(dic.values())[col][0])
                total_benefic = total_benefic + int(list(dic.values())[col][1])
            
        table_12.iloc[0, len(table.columns) - 1] = total_benefic if total_weight <= weight else 0
      
        if type(table_crossovery) == list: 
            table_crossovery = table_12
        else:   
            table_crossovery = table_crossovery.append(table_12)
        
    table_crossovery.reset_index(drop=True, inplace=True)
    
    return table_crossovery

# Function to make mutation in those element inferior to pct_mut
def Mutation(table):

    for i in range(len(table)):
        # round random number with two decimals
        num = round(random.uniform(0, 1), 2)
        # if num <= pct_mut we make the mutation
        if num <= pct_mut:
            num_col = round(random.uniform(0, objets))
            if table.iloc[i][num_col] == 0:
                table.iloc[i][num_col] = 1
            else:
                table.iloc[i][num_col] = 0
                
    table_final = table_select_final.append(table)        
    table_final.reset_index(drop = True, inplace = True)
    
    return table_final

table = Initializer(n_pob, objets)
table = Fitness(table)
print(list(table.iloc[0,:]))


for i in range(0, epochs):

    print("Generation ", i, "--> BEST: ", table.iloc[0,len(table.columns) - 1])
    table_select_final = Selection(table)
    table_crossover = Crossovery(table_select_final)       
    table_final = Mutation(table_crossover)
    table = Fitness(table_final)

print(list(table.iloc[0,:]))

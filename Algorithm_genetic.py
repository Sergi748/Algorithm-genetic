# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 11:19:11 2018

@author: Sergio Campos
"""
# Libraries
import pandas as pd
import numpy as np
import random

# Arguments
pct_mut = 0.05
n_pob = 200
epochs = 100
n_select = 50
n_part = 2
row = 50

# Function to create aleatory table of 0`s and 1`s
def Initializer(n_pob, row):

    # Create data frame with random numbers
    table = pd.DataFrame(np.random.randint(2,size=(n_pob, row)), columns=list(range(1, row + 1)))
    
    return table

# Function to evaluate every individaul about our objetive, we want the sum of every row
def Fitness(table):
    
    # Create column fitness 
    table['Sum'] = 0
    table['Sum'] = np.sum(table, axis = 1)
    table = table.sort_values(by = 'Sum', ascending = False)
    
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
        if table_index.iloc[0]['Sum'] > table_index.iloc[1]['Sum']:
            table_select_final = table_select_final.append(table_index.iloc[0,:])
        elif table_index.iloc[0]['Sum'] == table_index.iloc[1]['Sum']:
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
        table_12['Sum'] = np.sum(table_12, axis = 1)
        
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
            num_col = round(random.uniform(0, row))
            if table.iloc[i][num_col] == 0:
                table.iloc[i][num_col] = 1
            else:
                table.iloc[i][num_col] = 0
                
    table_final = table_select_final.append(table)        
    table_final.reset_index(drop = True, inplace = True)
    
    return table_final

table = Initializer(n_pob, row)
table = Fitness(table)
print(list(table.iloc[0,:]))

for i in range(0, epochs):

    print("Generation ", i, "--> BEST: ", table.iloc[0,50])
    table_select_final = Selection(table)
    table_crossover = Crossovery(table_select_final)       
    table_final = Mutation(table_crossover)
    table = Fitness(table_final)

print(list(table.iloc[0,:]))


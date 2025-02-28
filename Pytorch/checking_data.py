import numpy as np
import pandas as pd


#getting the data :
DATA = pd.read_csv("Planet.data")

#removing some of the columns that are not related
DATA = DATA.drop(["Planet_Name","Host_Star","Distance_ly","Discovery_Year","Discovery_Method"],axis=1)

print(DATA)
#use this if you wanna train Model
#for Num_nodes in [16,32,64] :
    #for dropout in [0,0.2] :
        #for Learning_rate in [0.1,0.001,0.005] :
            #for batch_size in [32,64,128] :
                
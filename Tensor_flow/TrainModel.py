import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import keras as keras
import copy as copy

#setting up the names :

#getting the data :
DATA = pd.read_csv("planets_data.csv")

#removing some of the columns that are not related
DATA = DATA.drop(["Planet Name","Radius (Earth Radii)"],axis=1)

print(DATA)

#I made function to create NN model
def CreateTheModel(Num_Inputs,DropOut,LR,Num_Nodes,Xtrain) :
    #Normalization :
    Norml_ = keras.layers.Normalization(input_shape = (Num_Inputs,),axis=-1)
    #Adapting : 
    Norml_.adapt(Xtrain)
    #Creating NNmodel : 
    NN_model = keras.Sequential([
        Norml_,
        keras.layers.Dense(Num_Nodes, activation="relu"),
        keras.layers.Dropout(DropOut),
        keras.layers.Dense(Num_Nodes,activation="relu"),
        keras.layers.Dense(1,activation="sigmoid")
        #I use sigmoid because I want a value between 0 and 1
    ])
    #Compile :
    NN_model.compile(optimizer=keras.optimizers.Adam(LR),loss="binary_crossentropy")
    return NN_model

#this function will train the model
def Train_theModel(Input_model,Xtrain,Ytrain,XValid,YValid,Epochs,Batch_size,Show = False) :
    #make hisory for model :
    History = Input_model.fit(Xtrain,Ytrain,epochs=Epochs,verbose=int(Show),validation_data=(XValid,YValid),batch_size = Batch_size)

    return History

#Create function to get x and y from data frame
def GET_XandY(data_frame,y_labels,x_labels = None, oversample = False) :
    data_frame = copy.deepcopy(data_frame)
    if x_labels is None:
        x = data_frame[[c for c in data_frame.columns if c!=y_labels]].values
    else :
        if len(x_labels) == 1 :
            x = data_frame[x_labels[0]].values.reshape(-1,1)
        else :
            x = data_frame[x_labels].values

    y = data_frame[y_labels].values.reshape(-1,1)


   
   

    data = np.hstack((x,np.reshape(y,(-1,1))))

    return data,x,y

#display Validation loss and Train losss
def plot_loss(history) :
    plt.plot(history.history['loss'], label = "loss")
    plt.plot(history.history['val_loss'],label = "val_loss")
    plt.title('Model loss')
    plt.ylabel('MSE')
    plt.xlabel('Epoch')
    plt.legend()
    plt.grid(True)
    plt.show()


#spliting the values
Train, Validation , Test  = np.split(DATA.sample(frac=1),[int(0.6 * len(DATA)), int(0.8 * len(DATA))])
#setting up the dataset :
Train,XTrain,YTrain = GET_XandY(Train,"Target",DATA.columns[:-1])
Validation,XValidation,YValidation = GET_XandY(Validation,"Target",DATA.columns[:-1])
Test,XTest,YTest = GET_XandY(Test,"Target",DATA.columns[:-1])
print(DATA.columns[:-1])

#using this variable we can store the best model
Best_model = None
Best_model_data = ""
Best_model_loss = float("inf")

Times = 0

#create the model and history
Model = CreateTheModel(len(DATA.columns[1:]),0,0.1,16,XTrain)
History = Train_theModel(Model,XTrain,YTrain,XValidation,YValidation,100,32,True)
valdLoss = Model.evaluate(XValidation, YValidation)

#saving the model data
print(Best_model_data)
Model.save("Train.h5")

plot_loss(History)

#testing model prediction
sample_input = np.array([[0,73,100,7]])
print(XTrain)
prediction = Model.predict(XTest)


for s in range(len(prediction)):
    print("Predicted Output:", round(prediction[s][0]))
    print("Actual Output:", YTest[s][0])





    
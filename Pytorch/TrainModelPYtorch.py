import torch.nn as nn
import numpy as np
import pandas as pd
import torch as torch
import torch.optim as opt
from sklearn.preprocessing import StandardScaler
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split as split_data





#creating the data
Data_set = pd.read_csv("planets_data.csv")
Data_set = Data_set.drop(["Planet Name","Radius (Earth Radii)"],axis=1)

#creating the features array
Features = Data_set.drop(["Target"],axis=1)
#creating the target array
Target = Data_set["Target"].values.reshape(-1,1)

#spliting the data between xtrain, ytrain, validation_x and validation_y
Train_x,validation_x,Train_y,validation_y  = split_data(Features,Target,test_size=0.2,random_state=42)




#transforming the arrays to pytorch tensor 

X_train_tensor = torch.FloatTensor(Train_x.values)
Y_train_tensor = torch.FloatTensor(Train_y)

X_validation_tensor = torch.FloatTensor(validation_x.values)
Y_validation_tensor = torch.FloatTensor(validation_y)

#creating the dataset and dataloader

Train_data_torch = TensorDataset(X_train_tensor,Y_train_tensor)
Validation_data_torch = TensorDataset(X_validation_tensor,Y_validation_tensor)


Train_loaded = DataLoader(Train_data_torch,batch_size=32, shuffle= True)
Validation_loaded = DataLoader(Validation_data_torch,batch_size=32)

Number_features = Train_x.shape[1]



class NerualNetwork(nn.Module):
    def __init__(self, num_inputs,  DropOut,Num_hidden,Num_outputs):
        super(NerualNetwork,self).__init__()
        #creating a normalized layer for inputs. in other word make the value of Xn between 0 or 1
        self.normal = nn.BatchNorm1d(num_inputs)
        #creating a relu function
        self.Relu_function = nn.ReLU()
        #adding the dropout
        self.DropOut = nn.Dropout(DropOut)
        #Input to first hidden layer
        self.layer1 = nn.Linear(num_inputs,Num_hidden)#
        #from first hidden layer to second hidden layer
        self.layer2 = nn.Linear(Num_hidden,Num_hidden)
        #from second hidden layer to the output lays
        self.layer3 = nn.Linear(Num_hidden,Num_outputs)
        self.sigmoid = nn.Sigmoid()

    def forward(self,x):
        x = self.normal(x)
        x = self.Relu_function(self.layer1(x))
        x = self.DropOut(x)
        x = self.Relu_function(self.layer2(x))
        x = self.sigmoid(self.layer3(x))
        return x


NNmodel = NerualNetwork(num_inputs=Number_features,DropOut=0.2,Num_hidden=64,Num_outputs=1)


#loss function :
loss_function = nn.BCELoss()
#optimizer : 
optimizer = opt.Adam(NNmodel.parameters(),lr=0.001)


epochs = 1000
history = {'trains : ':[],'validation : ': []}
for epoch in range(epochs):

    NNmodel.train()

    losses = []

    for inputs, targets in Train_loaded:
        optimizer.zero_grad() #reseting the gradient
        outputs = NNmodel(inputs) # predict the output base on the given inputs
        loss = loss_function(outputs,targets) # getting the loss
        loss.backward() # do backpropergation
        optimizer.step()
        losses.append(loss.item())

    ave_train_loss = sum(losses) / len(losses)

    NNmodel.eval()
    val_loss = []
    with torch.no_grad():
        for inputs, targets in Validation_loaded:
            output = NNmodel(inputs)
            loss = loss_function(output,targets)
            val_loss.append(loss.item())

    ave_validation_loss = sum(val_loss) / len(val_loss)


    print(f'Epochs : {epoch+1}/{epochs}, TrainLoss : {ave_train_loss}, validationLoss : {ave_validation_loss}')


torch.save(NNmodel.state_dict(),"Model.pth")


# -*- coding: utf-8 -*-
"""2A_original_mod.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PrtnkQIVpg6Of-H-lOg_hUXhYOe_UDsq
"""

#import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

#sigmoid function
def sigmoid(x):
  return 1/(1+np.exp(-x))

#LR loss function
def loss(h , y) : 
    return (-y * np.log(h) - (1 - y) * np.log(1 - h)).sum()

#predicting class function
def predict(weights  , bias , X):
        w = (X@weights) + bias
        y_pred = sigmoid(w)
        binary_pred = y_pred
        binary_pred[binary_pred>=0.5] = 1
        binary_pred[binary_pred<0.5] = 0
        return binary_pred

#calculating true/false positives/negatives:
def evaluate(y_pred , y):
    k=0
    tp=0
    fp=0
    fn=0
    tn=0
    for x in y_pred :
        if x==1 and y[k]==1:
          tp+=1
        elif x==1 and y[k]!=1:
          fp+=1
        else:
            if y[k] == 1:
                fn+=1
            else:
                tn+=1
        k+=1
    return tp,fp,tn,fn

#LR using gradient decent 

def LogisticRegression(lr  , iterations  , X  , y) :
  
    rows = X.shape[0] #rows x cols
    features = X.shape[1]
    weights = np.zeros(features)  #initialising weights
    bias = 0  #initialising bias
    y = y.reshape((y.shape[0],))
    
    l = []
    a = []
    #Gradient descent
    for i in range(iterations):
        w = (X@weights) + bias    #weight vector
        
        y_pred = sigmoid(w)    #predicting class
        
        #calculating weight and bias errors
        delta_w = (X.T) @ (y_pred - y)
        delta_b = np.sum(y_pred - y)
        
        #updating weights and bias 
        weights = weights - lr*(delta_w)
        bias = bias - lr*(delta_b)
        
        binary_pred = [1 if i>0.5 else 0 for i in y_pred]     #classifying class 
      
        if i%50 == 0 :
            l.append(loss(y_pred , y))     #appending loss
            a.append(((binary_pred == y).sum()/len(y)))     #appending accuracy
      
    return weights,bias,l,a

#LR using stochastic gradient decent 

def LogisticRegressionSGD(lr, iterations  , X  , y) :
    l=[]
    a=[]
    rows , features  = X.shape #rows x cols
    weights = np.zeros(features)    #initialising weights
    bias = 0    #initialising bias
    y = y.reshape((y.shape[0],))
    iter_no = 0
    
    #Stochastic Gradient descent
    for i in range(iterations):
         
        #chosing a random entry
        random_number = random.randint(0, len(y)-1)   
        x_b, y_b = X[random_number], y[random_number]

        w = np.dot(x_b, weights) + bias    #weight vector
        
        y_pred = 1/(1+np.exp(-w))    #predicting class
        
        #calculating weight and bias errors
        delta_w = np.dot(x_b.T , y_pred - y_b)
        delta_b = np.sum(y_pred - y_b)
        
        #updating weights and bias 
        weights = weights - lr*(delta_w)
        bias = bias - lr*(delta_b)
            
        binary_pred = predict(weights,bias,X)    #classifying class 
            
        iter_no+=1
            
        if iter_no%50==0:
            l.append(loss(y_pred , y_b))     #appending loss
            tp,fp,tn,fn = evaluate(binary_pred , y)   #calculating true/false positives/negatives
            a.append((tp+tn)/(tp+tn+fp+fn))     #appending accuracy
                
    return weights,bias,l,a

df = pd.read_csv('dataset_LR.csv')

col_names = np.array(df.columns)
col_names = col_names[:-1]
for i in col_names:
    col = np.array(df[i])
    mean_col = np.mean(col)
    std_col = np.std(col)
    norm_col = []
    for j in col:
        norm_col.append((j-mean_col)/std_col)
    df[i] = norm_col

df.head()

#creating lists to append them for calculation of averages
Accuracy =[]
Accuracy_t =[]
AccuracySGD=[]
AccuracySGD_t=[]

Loss=[]
LossSGD =[]

Fscore = []
Fscore_t = []
FscoreSGD=[]
FscoreSGD_t=[]

Precision=[]
Precision_t=[]
PrecisionSGD =[]
PrecisionSGD_t =[]

Recall=[]
Recall_t=[]
RecallSGD=[]
RecallSGD_t=[]

wGD=[]
bGD=[]
wSGD=[]
bSGD=[]

for j in range(10):     
    lrate= 0.001
    no_iter=10000
    
        
    #read and create 70:30 train-test splits
    df_random = df.sample(frac=1)
    rows , cols = df_random.shape
    a = int((70*rows)/100)
    df_train =  df_random.head(a)
    df_test =  df_random.tail(rows-a)

    X = df_train.iloc[: , 0:4]
    y = df_train.iloc[: ,-1:]

    np_X = X.to_numpy()
    np_y = y.to_numpy()

    #calling function return values
    weights,bias,los, acc = LogisticRegression(lrate , no_iter , np_X , np_y)
    wGD.append(weights)
    bGD.append(bias)
    weightsSGD , biasSGD , lSGD , aSGD = LogisticRegressionSGD(lrate , no_iter, np_X , np_y)
    wSGD.append(weightsSGD)
    bSGD.append(biasSGD)
        
    predicted = predict(weights , bias , np_X)
    tp,fp,tn,fn = evaluate(predicted , np_y)
    
    #calculating evaluation metrics
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f1 = 2/((1/recall) + (1/precision))
    accuracy= (tp+tn)/(tp+tn+fp+fn)
    
    #appending evaluation metrics list
    Accuracy.append(accuracy)
    Loss.append(los[-1])
    Fscore.append(f1)
    Precision.append(precision)
    Recall.append(recall)
        
    X_test = df_test.iloc[: , 0:4]
    y_test = df_test.iloc[: , -1:]

    np_X_t = X_test.to_numpy()
    np_y_t = y_test.to_numpy()
    np_y_t = np_y_t.reshape((np_y_t.shape[0],))
        
    predicted = predict(weights , bias , np_X_t)
    tp,fp,tn,fn = evaluate(predicted , np_y_t)
    
    #calculating evaluation metrics
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f1 = 2/((1/recall) + (1/precision))
    accuracy= (tp+tn)/(tp+tn+fp+fn)
    
    #appending evaluation metrics list
    Accuracy_t.append(accuracy)
    Fscore_t.append(f1)
    Precision_t.append(precision)
    Recall_t.append(recall)
    
    predicted = predict(weightsSGD , biasSGD , np_X)
    tp,fp,tn,fn = evaluate(predicted , np_y)
    
    #calculating evaluation metrics
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f1 = 2/((1/recall) + (1/precision))
    accuracy= (tp+tn)/(tp+tn+fp+fn)
    
    #appending evaluation metrics list
    AccuracySGD.append(accuracy)
    LossSGD.append(lSGD[-1])
    FscoreSGD.append(f1)
    PrecisionSGD.append(precision)
    RecallSGD.append(recall)
    
    predicted = predict(weightsSGD , biasSGD , np_X_t)
    tp,fp,tn,fn = evaluate(predicted , np_y_t)
    
    #calculating evaluation metrics
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f1 = 2/((1/recall) + (1/precision))
    accuracy= (tp+tn)/(tp+tn+fp+fn)
    
    #appending evaluation metrics lists
    AccuracySGD_t.append(accuracy)
    FscoreSGD_t.append(f1)
    PrecisionSGD_t.append(precision)
    RecallSGD_t.append(recall)

#calculating mean weights,bias GD

final_wGD=[0,0,0,0]

for i in range(10):
    final_wGD=final_wGD+wGD[i]
    
final_wGD=final_wGD/10
final_bGD=mean(bGD)

#calculating mean weights,bias SGD

final_wSGD=[0,0,0,0]

for i in range(10):
    final_wSGD=final_wSGD+wSGD[i]
    
final_wSGD=final_wSGD/10
final_bSGD=mean(bSGD)

#for 3 different learning rates

LearningRate = [0.001 , 0.0001 , 0.00001]

for lrate in LearningRate :
    print('-----------------Learning Rate :',lrate,'---------------------')
    print(' ')
    
    #reading, shuffling and making 70:30 split
    df_random = df.sample(frac=1)
    rows , cols = df_random.shape
    a = int((70*rows)/100)
    df_train =  df_random.head(a)
    df_test =  df_random.tail(rows-a)

    X = df_train.iloc[: , 0:4]
    y = df_train.iloc[: ,-1:]

    np_X = X.to_numpy()
    np_y = y.to_numpy()
    
    #calling function return values
    weights , bias , los, acc= LogisticRegression(lrate , no_iter , np_X , np_y)
    weightsSGD , biasSGD , lSGD , aSGD = LogisticRegressionSGD(lrate ,no_iter , np_X , np_y)

    iter = []
    for i in range(len(los)):
        iter.append(i*50)
 
    print("Final GD weights: ",weights)
    print("Final GD bias: ",bias)
    print("GD accuracy: ",(acc[-1]))
    plt.plot(iter,acc,label="Gradient Descent",color='red')
    plt.title("Accuracy per 50 iteration GD")
    plt.xlabel("Iterations")
    plt.ylabel("Accuracy")
    plt.show()
        
#     plt.plot(iter,los,label="Gradient Descent",color='orange')
#     plt.title("Loss per 50 iteration GD")
#     plt.xlabel("Iterations")
#     plt.ylabel("Loss")
#     plt.show()

    print("Final SGD weights: ",weightsSGD)
    print("Final SGD bias: ",biasSGD)
    print("SGD accuracy: ",(aSGD[-1]))
    plt.plot(iter,aSGD,label="Stochastic Gradient Descent",color='blue')
    plt.title("Accuracy per 50 iteration SGD")
    plt.xlabel("Iterations")
    plt.ylabel("Accuracy")
    plt.show()
    
#     plt.plot(iter,lSGD,label="Stochastic Gradient Descent")
#     plt.title("Loss per 50 iteration SGD")
#     plt.xlabel("Iterations")
#     plt.ylabel("Loss")
#     plt.show()


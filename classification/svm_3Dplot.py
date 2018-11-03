# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 19:57:16 2018

@author: Rajdeep Biswas
"""



import numpy as np
from sklearn import svm
import pickle as pk
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def svm_one_class(X_train,X_test,Y_test):

    # fit the model
    nu = np.logspace(-3,0,19)
    gamma = np.linspace(0.05,0.5,19)


    test_acc = []
    for m in range(len(nu)):
        test_acc_gamma = []
        for k in range(len(gamma)):
            clf = svm.OneClassSVM(nu=nu[m], kernel="rbf", gamma = gamma[k]) #gamma='scale' can be taken too
            clf.fit(X_train)
            y_pred_train = clf.predict(X_train)
            y_pred_test = clf.predict(X_test)
            n_error_train = y_pred_train[y_pred_train == -1].size     #No of training mislassifiations
            positive_user = y_pred_test[y_pred_test == Y_test].size       #No of Predictions that the user is i
            negative_user = y_pred_test[y_pred_test != Y_test].size       #No of Predictions that the user is not i
            tp=0
            fp=0
            fn=0
            tn=0
            for i in range(len(y_pred_test)):
                if(y_pred_test[i]==Y_test[i] and y_pred_test[i]==1):
                    tp=tp+1
                elif(y_pred_test[i]!=Y_test[i] and y_pred_test[i]==1):
                    fp=fp+1
                elif(y_pred_test[i]==Y_test[i] and y_pred_test[i]==-1):
                   tn=tn+1
                elif(y_pred_test[i]!=Y_test[i] and y_pred_test[i]==-1):
                	fn=fn+1
            precision = (tp*100)/(tp+fp+1e-7)
            recall = (tp*100)/(tp+fn+1e-7)
            specificity = (tn*100)/(tn+fp+1e-7)
            accuracy = 0.5*(tp*100.0/(tp+fn)+tn*100.0/(tn+fp))
            testing_error = 100-accuracy
            # print("Training Dataset Size : %s" %y_pred_train.size)
            # print("No of Training Misclassifications : %s" %n_error_train)
            # print("Training Error : %.2f percent" %((n_error_train*100)/y_pred_train.size))
            # print("Testing Dataset Size : %s" %Y_test.size)
            # print("Correct Decissions: %s" %positive_user)
            # print("Incorrect Decissions: %s" %negative_user)
            # print("Testing Accuracy: %.2f percent" %(accuracy))
            # print("Testing Error: %.2f percent" %((negative_user*100)/Y_test.size))
            # print("Precision: %.2f percent" %(precision))
            # print("Recall: %.2f percent" %(recall))
            # print("Specificity: %.2f percent" %(specificity))
            # print()
            test_acc_gamma.append(accuracy)
        test_acc.append(test_acc_gamma)
    return accuracy,precision, recall, test_acc

def plot(average_test_acc,roll):
    nu = np.logspace(-3,0,19)
    gamma = np.linspace(0.1,1,19)
    X,Y = np.meshgrid(nu,gamma)

    Z = np.array(average_test_acc)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z,label=roll)

    ax.set_xlabel('nu')
    ax.set_ylabel('gamma')
    ax.set_zlabel('average testing accuracy')
    # plt.xlabel("nu")
    # plt.ylabel("gamma")
    # plt.zlabel("average testing accuracy")
    # ax.legend(loc='upper center', bbox_to_anchor=(0.8, 1.25), ncol=4)
    plt.savefig( "./tests/3dplot/gamma_nu/" + roll + '.png',dpi=400, bbox_inches = 'tight')

def main():
    n = 0     #No of people
    data=[]    #Data Set
    roll=[]

    with open('roll_no2.txt') as f:
        for rollnum in f:
            n=n+1
            roll.append(rollnum.strip())
            with open('./pickled_vectors/'+rollnum.strip()+'.pickle', "rb") as input_file:
                ef = pk.load(input_file)
                ck=[]
                for item in ef:
                    ck.append(item)
                data.append(np.array(ck))


    for i in range(n):	# n is the number of roll numbers (users)
        #concatinate all the list together for testing as all column size same
        if(i==0):
            test=data[1]
            for k in range (2,n):
                test=np.vstack((test,data[k]))                     #Stack the datasets together
        else:
            test=data[0]
            for k in range (1,n):
                if(k!=i):
                    test=np.vstack((test,data[k]))                 #Stack the datasets together
        # print(test.shape)

        # print()
        print("For User %s" %roll[i])
        total_test_acc = []
        average_test_acc = []
        for j in range (5):
                                                    #5 Fold cross validation
            print("Validation Fold %s:" %(j+1))
            data_train=data[i]        
            np.random.shuffle(data_train)
            sz=int(0.2*data_train.shape[0])+1
            data_train_final=data_train[:-sz]                     #Discarding last 5% entries for training and add them in tesing
            data_test_final=data_train[-sz:]
    	    
            scaler = StandardScaler()
            data_train_final = scaler.fit_transform(data_train_final)

            pca = PCA(n_components = 8)
            data_train_final = pca.fit_transform(data_train_final)


            y=np.ones(sz)


            sz=int(0.05*data_train.shape[0])+1              #No of test sample needed more for 80:20 ratio 80 authentic (same user) and 20 other users
            np.random.shuffle(test)                               #Shuffle the whole set for testing
            data_test_final=np.vstack((data_test_final,test[:sz]))
            data_test_final = scaler.transform(data_test_final)
            data_test_final = pca.transform(data_test_final)
            print(data_test_final.shape)
            z=-np.ones(sz)
            y_final=np.append(y,z)                       #Result vector for Testing
            accuracy,precision, recall, test_acc = svm_one_class(data_train_final,data_test_final,y_final)       # calling SVM function
            total_test_acc.append(test_acc)
        # print(total_test_error)
        for m in range(len(test_acc)):
            average_test_acc_gamma = []
            for k in range(len(test_acc)): 
                average = 0
                for j in range(5):
                    average = total_test_acc[j][m][k]+ average
                average = average/5
                average_test_acc_gamma.append(average)
            average_test_acc.append(average_test_acc_gamma)
        print(average_test_acc)
        plot(average_test_acc,roll[i])

main()


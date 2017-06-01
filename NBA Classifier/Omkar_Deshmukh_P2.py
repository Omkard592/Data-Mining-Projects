#Omkar K Deshmukh
#1001275806


'''''''''''''''''''''''''''''''''  IMPORTS  '''''''''''''''''''''''''''''''''''
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
'''''''''''''''''''''''''''''''''  IMPORTS  '''''''''''''''''''''''''''''''''''


'''''''''''''''''''''''  READ & PROCESS FILE  '''''''''''''''''''''''''''''''''
#clear the console screen
clear = lambda: os.system('cls')
clear()

#read from the csv file and return a Pandas DataFrame.
nba = pd.read_csv('NBAstats.csv')

# "Position (pos)" is the class attribute we are predicting. 
class_column = 'Pos'

#The dataset contains attributes such as player name and team name. 
#We know that they are not useful for classification and thus do not 
#include them as features.
feature_columns = ['FG', 'FGA', '3P', '3PA', \
     '2P', '2PA',  'FT', 'FTA', 'ORB', 'DRB', \
     'AST', 'STL', 'BLK', 'TOV']

#Pandas DataFrame allows you to select columns.
#We use column selection to split the data into features and class. 
nba_feature = nba[feature_columns]
nba_class = nba[class_column]

train_feature, test_feature, train_class, test_class = \
    train_test_split(nba_feature, nba_class, stratify=nba_class, \
    train_size=0.75, test_size=0.25)
    

################# Code block to get class weights (Not used) ##################
'''all_class_instances = nba_class[:]
class_weights = {}
unique_classes = list(set(all_class_instances))
for ust in unique_classes:
    try:                                    
        x = class_weights[ust]
    except KeyError:
        class_weights[ust] = 0

for aci in all_class_instances:           
        class_weights[aci] = class_weights[aci] + 1
      
#print(class_weights)  
for ust in unique_classes:
    class_weights[ust] = class_weights[ust] / len(nba_class)'''
################# Code block to get class weights (Not used) ##################
'''''''''''''''''''''''  READ & PROCESS FILE  '''''''''''''''''''''''''''''''''


'''''''''''''''''''''''  SELECT CLASSIFIER MODEL  '''''''''''''''''''''''''''''
#I am using Neural Network as the classifier, reason given in the doc file.
clf = MLPClassifier(activation='identity', alpha=2, solver='lbfgs', hidden_layer_sizes=200, tol=0)
clf.fit(train_feature, train_class)
prediction = clf.predict(test_feature)

print('\nUsing the following classifier:')
print(35 * '-')
print(clf)
    
print("\n\nTest set accuracy:")
print(35 * '-')
print("{:.2f}".format(clf.score(test_feature, test_class)))
'''''''''''''''''''''''  SELECT CLASSIFIER MODEL  '''''''''''''''''''''''''''''


'''''''''''''''''''''''''''''  PRINT THE CONFUSION MATRIX '''''''''''''''''''''
print("\n\nConfusion matrix:")
print(35 * '-')
print(pd.crosstab(test_class, prediction, rownames=['True'], colnames=['Predicted'], margins=True))
'''''''''''''''''''''''''''''  PRINT THE CONFUSION MATRIX '''''''''''''''''''''


'''''''''''''''''''''''''''''''''  CROSS VALIDATION '''''''''''''''''''''''''''
scores = cross_val_score(clf, nba_feature, nba_class, cv=10)
print("\n\nCross validation:")
print(35 * '-')
for i in range(1,11):
    print("Cross-validation score for fold",i,": {}".format(scores[i-1]))
    
print("\nAverage cross-validation score: {:.2f}".format(scores.mean()))
'''''''''''''''''''''''''''''''''  CROSS VALIDATION '''''''''''''''''''''''''''
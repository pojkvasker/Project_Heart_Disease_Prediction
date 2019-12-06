import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

# model persistance from python to java
import pickle
import joblib
#from sklearn_porter import Porter

# -------------------data import----------------------------------------------------------
# https://archive.ics.uci.edu/ml/datasets/heart+Disease
# Cleveland dataset
data_cl = pd.read_csv('processed.cleveland_2.txt',\
                      sep=",", header=None) 
# Hungarian dataset
data_hu = pd.read_csv('processed.hungarian_2.txt',\
                      sep=",", header=None) 
# Swiz dataset
data_sw = pd.read_csv('processed.switzerland_2.txt',\
                      sep=",", header=None)
# Long beach dataset
data_va = pd.read_csv('processed.va_2.txt',\
                      sep=",", header=None)
# Merge all datasets into one dataset
data_cl = pd.concat([data_cl,data_hu,data_sw,data_va]).replace('?', np.nan).reset_index(drop=True)
# Column names, according to the web source
data_cl.columns = ['age','sex','cp','trestbps','chol','fbs','restecg',\
                'thalach','exang','oldpeak','slope','ca','thal','num']
# Filter out datapoints with missing values
filtered_data = data_cl.dropna()
# Define parameters used in training
age = filtered_data['age'].astype(float).values.tolist() 
sex = filtered_data['sex'].astype(bool).astype(int).values.tolist()
cp = filtered_data['cp'].astype(int).values.tolist()                        # chest pain type 1: typical angina, 2: atypical angina, 3: non-anginal pain, 4: asymptomatic
trestbps = filtered_data['trestbps'].astype(int).values.tolist()            # resting blood pressure (in mm Hg on admission to the hospital)
chol = filtered_data['chol'].astype(float).values.tolist()                  # serum cholestoral in mg/dl
fbs = filtered_data['fbs'].astype(float).values.tolist()                    # (fasting blood sugar > 120 mg/dl)  (1 = true; 0 = false)
restecg = filtered_data['restecg'].astype(bool).astype(int).values.tolist() # resting electrocardiographic results 0:normal, 1:abnormal ( having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV) orshowing probable or definite left ventricular hypertrophy by Estes' criteria)
thalach = filtered_data['thalach'].astype(float).values.tolist()            # maximum heart rate achieved
exang = filtered_data['exang'].astype(float).values.tolist()                # exercise induced angina (1 = yes; 0 = no)
oldpeak = filtered_data['oldpeak'].astype(float).values.tolist()            # ST depression induced by exercise relative to rest
slope = filtered_data['slope'].astype(int).values.tolist()                  # the slope of the peak exercise ST segment 1: upsloping, 2: flat, 3: downsloping
ca = filtered_data['ca'].astype(float).values.tolist()                      # number of major vessels (0-3) colored by flourosopy
thal = filtered_data['thal'].astype(float).values.tolist()                  # 3 = normal; 6 = fixed defect; 7 = reversable defect
label = filtered_data['num'].astype(bool).astype(int).values.tolist()       # prediction class label



# Define which parameters to be used in training as x
# uncomment row below for training will all parameters
x = np.transpose([age,sex,chol,trestbps,restecg,exang])
x = StandardScaler().fit_transform(x)  # normalization
#x = np.transpose([age,sex,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope])
# Define class to predict, here binary, to y
y = np.transpose([label])

names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Gaussian Process",
         "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
         "Naive Bayes", "QDA"]
classifiers = [
    KNeighborsClassifier(16),
    SVC(kernel="linear", C=0.025),
    SVC(gamma=2, C=1),
    GaussianProcessClassifier(1.0 * RBF(1.0)),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    MLPClassifier(alpha=1, max_iter=1000),
    AdaBoostClassifier(),
    GaussianNB(),
    QuadraticDiscriminantAnalysis()]
print('-----------------------------'+'\n'+'Training initialized...'+'\n'+'-----------------------------')
for name, clf in zip(names, classifiers):
    # Define number of folds in cross-validation to c
    c=10
    sc = cross_validate(clf, x, y.ravel(), cv=c)
    score = sum(sc['test_score'])/c
    print(str(name)+': '+str(score))
print('-----------------------------'+'\n'+'Training complete.'+'\n'+'-----------------------------')
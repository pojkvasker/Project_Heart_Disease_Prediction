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

def intrinsic_discrepancy(x,y):
    assert len(x)==len(y)
    sumx = sum(xval for xval in x)
    sumy = sum(yval for yval in y)
    id1  = 0.0
    id2  = 0.0
    for (xval,yval) in zip(x,y):
        if (xval>0) and (yval>0):
            id1 += (float(xval)/sumx) * np.log((float(xval)/sumx)/(float(yval)/sumy))
            id2 += (float(yval)/sumy) * np.log((float(yval)/sumy)/(float(xval)/sumx))
    return min(id1,id2)

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
data_cl = pd.concat([data_cl]).replace('?', np.nan).reset_index(drop=True)
# Column names, according to the web source
data_cl.columns = ['age','sex','cp','trestbps','chol','fbs','restecg',\
                'thalach','exang','oldpeak','slope','ca','thal','num']
# Filter out datapoints with missing values
filtered_data = data_cl.dropna()

sick = filtered_data.loc[filtered_data['num'] == 1]
good = filtered_data.loc[filtered_data['num'] == 0]



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

plt.style.use('seaborn-white')
kwargs = dict(histtype='step', alpha=0.3, density=True, ec="k")
bins = len(filtered_data)
print('bins'+str(bins))
int_discr = {}

plt.figure(1)
bins = np.linspace(20, 80, 25)
plt.xlabel('Age')
age_s = plt.hist(sick['age'], bins=bins, **kwargs, edgecolor='red')
age_g = plt.hist(good['age'], bins=bins, **kwargs, edgecolor='green')
int_discr["age"] = intrinsic_discrepancy(age_s[0],age_g[0])

plt.figure(2)
bins = 2
plt.xlabel('Gender (1 = male, 0 = female)')
sex_s = plt.hist(sick['sex'], bins=bins, **kwargs, edgecolor='red')
sex_g = plt.hist(good['sex'], bins=bins, **kwargs, edgecolor='green')
int_discr["sex"] = intrinsic_discrepancy(sex_s[0],sex_g[0])

plt.figure(3)
bins = 4
plt.xlabel(' chest pain type 1: typical angina, 2: atypical angina, 3: non-anginal pain, 4: asymptomatic')
cp_s = plt.hist(sick['cp'], bins=bins, **kwargs, edgecolor='red')
cp_g = plt.hist(good['cp'], bins=bins, **kwargs, edgecolor='green')
int_discr["cp"] = intrinsic_discrepancy(cp_s[0],cp_g[0])

plt.figure(4)
bins = np.linspace(80, 200, 15)
plt.xlabel('Resting blood pressure (in mm Hg)')
bp_s = plt.hist(sick['trestbps'].astype(float), bins=bins, **kwargs, edgecolor='red')
bp_g = plt.hist(good['trestbps'].astype(float), bins=bins, **kwargs, edgecolor='green')
int_discr["bp"] = intrinsic_discrepancy(bp_s[0],bp_g[0])

plt.figure(5)
bins = np.linspace(110, 200, 15)
plt.xlabel('serum cholestoral in mg/dl')
chol_s = plt.hist(sick['chol'].astype(float), bins=bins, **kwargs, edgecolor='red')
chol_g = plt.hist(good['chol'].astype(float), bins=bins, **kwargs, edgecolor='green')
int_discr["chol"] = intrinsic_discrepancy(chol_s[0],chol_g[0])

plt.figure(6)
bins = 2
plt.xlabel('Fasting blood sugar > 120 mg/dl  (1 = true, 0 = false)')
fbs_s = plt.hist(sick['fbs'].astype(int), bins=bins, **kwargs, edgecolor='red')
fbs_g = plt.hist(good['fbs'].astype(int), bins=bins, **kwargs, edgecolor='green')
int_discr["fbs"] = intrinsic_discrepancy(fbs_s[0],fbs_g[0])

plt.figure(7)
plt.xlabel('Resting electrocardiographic results (1 = arrythmia, 0 = normal)')
ecg_s = plt.hist(sick['restecg'].astype(bool).astype(int), bins=bins, **kwargs, edgecolor='red')
ecg_g = plt.hist(good['restecg'].astype(bool).astype(int), bins=bins, **kwargs, edgecolor='green')
int_discr["ecg"] = intrinsic_discrepancy(ecg_s[0],ecg_g[0])

plt.figure(8)
bins = np.linspace(80, 200, 15)
plt.xlabel('Maximum heart rate achieved')
thalach_s = plt.hist(sick['thalach'].astype(int), bins=bins, **kwargs, edgecolor='red')
thalach_g = plt.hist(good['thalach'].astype(int), bins=bins, **kwargs, edgecolor='green')
int_discr["thalach"] = intrinsic_discrepancy(thalach_s[0],thalach_g[0])

plt.figure(9)
bins = 2
plt.xlabel('Exercise induced angina (1 = yes 0 = no)')
exang_s = plt.hist(sick['exang'].astype(int), bins=bins, **kwargs, edgecolor='red')
exang_g = plt.hist(good['exang'].astype(int), bins=bins, **kwargs, edgecolor='green')
int_discr["exang"] = intrinsic_discrepancy(exang_s[0],exang_g[0])

plt.figure(10)
bins = np.linspace(0, 6, 15)
plt.xlabel('ST depression induced by exercise relative to rest')
old_s = plt.hist(sick['oldpeak'].astype(float), bins=bins, **kwargs, edgecolor='red')
old_g = plt.hist(good['oldpeak'].astype(float), bins=bins, **kwargs, edgecolor='green')
int_discr["old"] = intrinsic_discrepancy(old_s[0],old_g[0])

plt.figure(11)
bins = 3
plt.xlabel('The slope of the peak exercise ST segment (1 = upsloping, 2 = flat, 3 = downsloping)')
slope_s =plt.hist(sick['slope'].astype(int), bins=bins, **kwargs, edgecolor='red')
slope_g = plt.hist(good['slope'].astype(int), bins=bins, **kwargs, edgecolor='green')
int_discr["slope"] = intrinsic_discrepancy(slope_s[0],slope_g[0])

plt.figure(12)
bina = 4
plt.xlabel('Number of major vessels (0-3) colored by flourosopy')
ca_s = plt.hist(sick['ca'].astype(float).astype(int), bins=bins, **kwargs, edgecolor='red')
ca_g = plt.hist(good['ca'].astype(float).astype(int), bins=bins, **kwargs, edgecolor='green')
int_discr["ca"] = intrinsic_discrepancy(ca_s[0],ca_g[0])

plt.figure(13)
bins = 3
plt.xlabel('Thalassemia (3 = normal, 6 = fixed defect, 7 = reversable defect)')
thal_s = plt.hist(sick['thal'].astype(float).astype(int), bins=bins, **kwargs, edgecolor='red')
thal_g = plt.hist(good['thal'].astype(float).astype(int), bins=bins, **kwargs, edgecolor='green')
int_discr["thal"] = intrinsic_discrepancy(thal_s[0],thal_g[0])
print(int_discr)
plt.show()


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

sick = filtered_data.loc[filtered_data['num'] != 0]
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

sick_color = ['crimson']
good_color = ['mediumseagreen']


plt.figure(1)
bins = np.linspace(20, 80, 25)
plt.hist(sick['age'],bins,color=sick_color,histtype="step",label="disease",density=True)
plt.hist(good['age'],bins,color=good_color,histtype="step",label="no disease",density=True)
plt.xlabel("Age (years)",fontsize=15)

fig, axes = plt.subplots()

bins     = np.arange(2)
width    = 0.5
heights1 = sick["sex"].groupby(data_cl['sex']).count()
heights2 = good["sex"].groupby(data_cl["sex"]).count()
heights1 = heights1/sum(heights1)
heights2 = heights2/sum(heights2)
axes.bar(bins+0.025,heights1,width,align="center",edgecolor=sick_color,color=["none"],label="disease")
axes.bar(bins,heights2,width,align="center",edgecolor=good_color,color=["none"],label="no disease")
axes.set_xlabel("Sex",fontsize=15)
axes.set_xticks(bins)
axes.set_xticklabels(["female","male"],ha="center")


fig, axes = plt.subplots()
bins     = np.arange(4)
width    = 0.5
heights1 = sick["cp"].groupby(data_cl["cp"]).count()
heights2 = good["cp"].groupby(data_cl["cp"]).count()
heights1 = heights1/sum(heights1)
heights2 = heights2/sum(heights2)
axes.bar(bins+0.025,heights1,width,align="center",edgecolor=sick_color,color=["none"],label="disease")
axes.bar(bins,heights2,width,align="center",edgecolor=good_color,color=["none"],label="no disease")
axes.set_xlabel("Type of Chest Pain",fontsize=15)
axes.set_xticks(bins)
axes.set_xticklabels(["typical angina", "atypical angina", "non-angina", "asymptomatic angina"],
                          ha="right",rotation=10.)

fig, axes = plt.subplots()
bins = np.linspace(80, 200, 15)
axes.hist(sick['trestbps'].astype(float),bins,color=sick_color,histtype="step",label="disease",density=True)
axes.hist(good['trestbps'].astype(float),bins,color=good_color,histtype="step",label="no disease",density=True)
axes.set_xlabel("Resting Blood Pressure (mm Hg)",fontsize=15)

fig, axes = plt.subplots()
axes.hist(sick['chol'].astype(float),color=sick_color,histtype="step",label="disease",density=True)
axes.hist(good['chol'].astype(float),color=good_color,histtype="step",label="no disease",density=True)
axes.set_xlabel("Serum Cholesterol (mg/dl)",fontsize=15)

fig, axes = plt.subplots()
bins     = np.arange(2)
width    = 0.5
heights1 = sick["fbs"].groupby(data_cl["fbs"]).count()
heights2 = good["fbs"].groupby(data_cl["fbs"]).count()
heights1 = heights1/sum(heights1)
heights2 = heights2/sum(heights2)
axes.bar(bins+0.025,heights1,width,align="center",edgecolor=sick_color,color=["none"],label="disease")
axes.bar(bins,heights2,width,align="center",edgecolor=good_color,color=["none"],label="no disease")
axes.set_xlabel("Fasting Blood Sugar",fontsize=15)
axes.set_xticks(bins)
axes.set_xticklabels(["< 120 mg/dl","> 120 mg/dl"],ha="center")

fig, axes = plt.subplots()
bins     = np.arange(3)
width    = 0.5
heights1 = sick["restecg"].groupby(data_cl["restecg"]).count()
heights2 = good["restecg"].groupby(data_cl["restecg"]).count()
heights1 = heights1/sum(heights1)
heights2 = heights2/sum(heights2)
axes.bar(bins+0.025,heights1,width,align="center",edgecolor=sick_color,color=["none"],label="disease")
axes.bar(bins,heights2,width,align="center",edgecolor=good_color,color=["none"],label="no disease")
axes.set_xlabel("Rest ECG",fontsize=15)
axes.set_xticks(bins)
axes.set_xticklabels(["Normal","ST-T wave abnorm.","left ventr. hypertrophy"],ha="right",rotation=10.)

fig, axes = plt.subplots()
axes.hist(sick['thalach'],color=sick_color,histtype="step",label="disease",density=True)
axes.hist(good['thalach'],color=good_color,histtype="step",label="no disease",density=True)
axes.set_xlabel("Thalium Test: Max. Heart Rate",fontsize=15)

fig, axes = plt.subplots()
bins     = np.arange(2)
width    = 0.5
heights1 = sick["exang"].groupby(data_cl["exang"]).count()
heights2 = good["exang"].groupby(data_cl["exang"]).count()
heights1 = heights1/sum(heights1)
heights2 = heights2/sum(heights2)
axes.bar(bins+0.025,heights1,width,align="center",edgecolor=sick_color,color=["none"],label="disease")
axes.bar(bins,heights2,width,align="center",edgecolor=good_color,color=["none"],label="no disease")
axes.set_xlabel("Exercise Induced Angina",fontsize=15)
axes.set_xticks(bins)
axes.set_xticklabels(["No","Yes"],ha="center")

fig, axes = plt.subplots()
axes.hist(sick['oldpeak'],color=sick_color,histtype="step",label="disease",density=True)
axes.hist(good['oldpeak'],color=good_color,histtype="step",label="no disease",density=True)
axes.set_xlabel("ST Depression Induced by Exercise", fontsize=15)

fig, axes = plt.subplots()
bins     = np.arange(3)
width    = 0.5
heights1 = sick["slope"].groupby(data_cl["slope"]).count()
heights2 = good["slope"].groupby(data_cl["slope"]).count()
heights1 = heights1/sum(heights1)
heights2 = heights2/sum(heights2)
axes.bar(bins+0.025,heights1,width,align="center",edgecolor=sick_color,color=["none"],label="disease")
axes.bar(bins,heights2,width,align="center",edgecolor=good_color,color=["none"],label="no disease")
axes.set_xlabel("Slope of Peak Exercise ST Segment",fontsize=15)
axes.set_xticks(bins)
axes.set_xticklabels(["Upsloping","Flat","Downsloping"],ha="right")


fig, axes = plt.subplots()
bins     = np.arange(4)
width    = 0.5
heights1 = sick["ca"].groupby(data_cl["ca"]).count()
heights2 = good["ca"].groupby(data_cl["ca"]).count()
heights1 = heights1/sum(heights1)
heights2 = heights2/sum(heights2)
axes.bar(bins+0.025,heights1,width,align="center",edgecolor=sick_color,color=["none"],label="disease")
axes.bar(bins,heights2,width,align="center",edgecolor=good_color,color=["none"],label="no disease")
axes.set_xlabel("Major Vessels Colored by Fluoroscopy",fontsize=15)
axes.set_xticks(bins)
axes.set_xticklabels(["0","1","2","3"],ha="center")

fig, axes = plt.subplots()
bins     = np.arange(3)
width    = 0.5
heights1 = sick["thal"].groupby(data_cl["thal"]).count()
heights2 = good["thal"].groupby(data_cl["thal"]).count()
heights1 = heights1/sum(heights1)
heights2 = heights2/sum(heights2)
axes.bar(bins+0.025,heights1,width,align="center",edgecolor=sick_color,color=["none"],label="disease")
axes.bar(bins,heights2,width,align="center",edgecolor=good_color,color=["none"],label="no disease")
axes.set_xlabel("Thalium Stress Test Result",fontsize=15)
axes.set_xticks(bins)
axes.set_xticklabels(["Normal","Fixed Defect","Reversible Defect"],ha="right")
axes.set_ylim(0.0,1.0)

fig, axes = plt.subplots()
bins     = np.arange(5)
width    = 0.5
heights1 = np.array(list(map(float,[0]+sick["num"].groupby(data_cl["num"]).count().tolist())))
heights2 = np.array(list(map(float,good["num"].groupby(data_cl["num"]).count().tolist()+[0,0,0,0])))
heights1 = heights1/sum(heights1)
heights2 = heights2/sum(heights2)
axes.bar(bins,heights1,width,align="center",edgecolor=sick_color,color=["none"],label="disease")
axes.bar(bins,heights2,width,align="center",edgecolor=good_color,color=["none"],label="no disease")
axes.set_xlabel("Major Vessels with >50% Narrowing",fontsize=15)
axes.set_xticks(bins)
axes.set_xticklabels(["0","1","2","3","4"],ha="center")
axes.set_ylim(0.0,1.1)

plt.show()

# intrinsic discrepancy
int_discr = {}
hist,bin_edges   = np.histogram(data_cl['age'],density=False)
hist1,bin_edges1 = np.histogram(sick['age'],bins=bin_edges,density=False)
hist2,bin_edges2 = np.histogram(good['age'],bins=bin_edges,density=False)
int_discr["age"] = intrinsic_discrepancy(hist1,hist2)
hist1,bin_edges1 = np.histogram(sick['sex'],bins=(-0.5,0.5,1.5),density=False)
hist2,bin_edges2 = np.histogram(good['sex'],bins=(-0.5,0.5,1.5),density=False)
int_discr["sex"] = intrinsic_discrepancy(hist1,hist2)
hist1,bin_edges1 = np.histogram(sick['cp'],bins=(0.5,1.5,2.5,3.5,4.5),density=False)
hist2,bin_edges2 = np.histogram(good['cp'],bins=(0.5,1.5,2.5,3.5,4.5),density=False)
int_discr["cp"] = intrinsic_discrepancy(hist1,hist2)
hist,bin_edges   = np.histogram(data_cl['trestbps'],density=False)
hist1,bin_edges1 = np.histogram(sick['trestbps'],bins=bin_edges,density=False)
hist2,bin_edges2 = np.histogram(good['trestbps'],bins=bin_edges,density=False)
int_discr["trestbps"] = intrinsic_discrepancy(hist1,hist2)
hist,bin_edges   = np.histogram(data_cl['chol'],density=False)
hist1,bin_edges1 = np.histogram(sick['chol'],bins=bin_edges,density=False)
hist2,bin_edges2 = np.histogram(good['chol'],bins=bin_edges,density=False)
int_discr["chol"] = intrinsic_discrepancy(hist1,hist2)
hist1,bin_edges1 = np.histogram(sick['fbs'],bins=(-0.5,0.5,1.5),density=False)
hist2,bin_edges2 = np.histogram(good['fbs'],bins=(-0.5,0.5,1.5),density=False)
int_discr["fbs"] = intrinsic_discrepancy(hist1,hist2)
hist1,bin_edges1 = np.histogram(sick['restecg'],bins=(-0.5,0.5,1.5,2.5),density=False)
hist2,bin_edges2 = np.histogram(good['restecg'],bins=(-0.5,0.5,1.5,2.5),density=False)
int_discr["restecg"] = intrinsic_discrepancy(hist1,hist2)
hist,bin_edges   = np.histogram(data_cl['thalach'],density=False)
hist1,bin_edges1 = np.histogram(sick['thalach'],bins=bin_edges,density=False)
hist2,bin_edges2 = np.histogram(good['thalach'],bins=bin_edges,density=False)
int_discr["thalach"] = intrinsic_discrepancy(hist1,hist2)
hist1,bin_edges1 = np.histogram(sick['exang'],bins=(-0.5,0.5,1.5),density=False)
hist2,bin_edges2 = np.histogram(good['exang'],bins=(-0.5,0.5,1.5),density=False)
int_discr["exang"] = intrinsic_discrepancy(hist1,hist2)
hist,bin_edges   = np.histogram(data_cl['oldpeak'],density=False)
hist1,bin_edges1 = np.histogram(sick['oldpeak'],bins=bin_edges,density=False)
hist2,bin_edges2 = np.histogram(good['oldpeak'],bins=bin_edges,density=False)
int_discr["oldpeak"] = intrinsic_discrepancy(hist1,hist2)
hist1,bin_edges1 = np.histogram(sick['slope'],bins=(0.5,1.5,2.5,3.5),density=False)
hist2,bin_edges2 = np.histogram(good['slope'],bins=(0.5,1.5,2.5,3.5),density=False)
int_discr["slope"] = intrinsic_discrepancy(hist1,hist2)
hist1,bin_edges1 = np.histogram(sick['ca'].astype(float),bins=(-0.5,0.5,1.5,2.5,3.5),density=False)
hist2,bin_edges2 = np.histogram(good['ca'].astype(float),bins=(-0.5,0.5,1.5,2.5,3.5),density=False)
int_discr["ca"] = intrinsic_discrepancy(hist1,hist2)
hist1,bin_edges1 = np.histogram(sick['thal'].astype(float),bins=(2.5,3.5,6.5,7.5),density=False)
hist2,bin_edges2 = np.histogram(good['thal'].astype(float),bins=(2.5,3.5,6.5,7.5),density=False)
int_discr["thal"] = intrinsic_discrepancy(hist1,hist2)
print(int_discr)
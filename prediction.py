import sys
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import(Matern)
import numpy as np
import joblib

import os

print(os.getcwd())

age = float(sys.argv[1])
sex = float(sys.argv[2])
bp = float(sys.argv[3])
chol = float(sys.argv[4])
ecg = float(sys.argv[5])
exang = float(sys.argv[6])

gp_model_from_joblib = joblib.load('pythonForServer\gp_matern.joblib')
input = np.array([age, sex, exang, bp, chol, ecg])
pred = gp_model_from_joblib.predict(input.reshape(1,-1))
predProb = gp_model_from_joblib.predict_proba(input.reshape(1,-1))

print(pred)
print(predProb[0][1])
print(type(predProb[0][1]))

with open("Output.txt", "w") as text_file:
    print("{},".format(1), "{},".format(int(pred)), "{}".format(predProb[0][1]), file=text_file)

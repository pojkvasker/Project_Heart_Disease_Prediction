import sys
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import(Matern)
import numpy as np
import joblib
import json

import os

print(os.getcwd())

age = float(sys.argv[1])
sex = float(sys.argv[2])
bp = float(sys.argv[3])
chol = float(sys.argv[4])
ecg = float(sys.argv[5])
exang = float(sys.argv[6])

# import joblib model
gp_model_from_joblib = joblib.load('C:/xampp/htdocs/Working_Prototype_1.0/GPC_model.joblib')
# import json object
with open('C:/xampp/htdocs/Working_Prototype_1.0/training_info.json') as f:
  json_data = json.load(f)

# normalize input data to training normalization
age = (age-json_data['Mean of age'])/json_data['Std of age']
sex = (sex-json_data['Mean of sex'])/json_data['Std of sex']
chol = (chol-json_data['Mean of chol'])/json_data['Std of chol']
bp = (bp-json_data['Mean of trestbps'])/json_data['Std of trestbps']
ecg = (ecg-json_data['Mean of restecg'])/json_data['Std of restecg']
exang = (exang-json_data['Mean of exang'])/(json_data['Std of exang'])

# Form input vector and do prediction
input = np.array([age, sex, chol, bp, ecg, exang])
pred = gp_model_from_joblib.predict(input.reshape(1,-1))
predProb = gp_model_from_joblib.predict_proba(input.reshape(1,-1))

print(pred)
print(predProb[0][1])
print(type(predProb[0][1]))

with open("Output.txt", "w") as text_file:
    print("{},".format(1), "{},".format(int(pred)), "{}".format(predProb[0][1]), file=text_file)

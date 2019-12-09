import json
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import(Matern)
from sklearn.model_selection import train_test_split, cross_validate
import numpy as np
import pymysql
from datetime import datetime

# Define MySQL connectivty
connection = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "",
    db = "pdp", # Name of database
)
try:
    with connection.cursor() as cursor:
        # Define columns in the database, both class label(s) and parameters
         sql = "SELECT `age`, `sex`, `cp`, `trestbps`, `chol`, `fbs`, `restecg`, `thalac`, `exang`, `oldpeak`, `slope`, `ca`, `thal`, `num` FROM `heart disease prediction`"
         try:
             cursor.execute(sql)
             # Fetch db data locally
             db_data = cursor.fetchall()
             print("Data fetched from db.")
         except:
             print("Did not work!")
    connection.commit()
finally:
    connection.close()

# Import into separate vectors
age = [i[0] for i in db_data]
sex = [i[1] for i in db_data]
cp = [i[2] for i in db_data]
trestbps = [i[3] for i in db_data]
chol = [i[4] for i in db_data]
fbs = [i[5] for i in db_data]
restecg = [i[6] for i in db_data]
thalac = [i[7] for i in db_data]
exang = [i[8] for i in db_data]
oldpeak = [i[9] for i in db_data]
slope = [i[10] for i in db_data]
ca = [i[11] for i in db_data]
thal = [i[12] for i in db_data]
label = [i[13] for i in db_data]

# Short description of parameters and class label, used for JSON object, could be further and more deeply explained
params = ['age', 'sex', 'chest pain type', 'blood pressure', 'cholesterol', 'fasting blood sugar', 'electrocardiography', \
          'thalac', 'excercise induced chest pain', 'oldpeak', 'slope', 'ca', 'thal', 'heart disease' ]
params_used = [params[0], params[1], params[3], params[4], params[6], params[8], params[13]]
# Define x as training parameters, based on avaiable info
x = np.transpose([age,sex,chol,trestbps,restecg,exang])
# Define y as class label
y = np.transpose([label])

# Choice of model, here GP with Matern as kernel
kernel = 1.0 * Matern(length_scale=1.0,length_scale_bounds=(1e-1,10.0),nu=1.5)
model = GaussianProcessClassifier(kernel=kernel)
# Perform c-fold cross-validation for performance measure of the model
c = 10
sc = cross_validate(model, x, y.ravel(), cv=c)
score = sum(sc['test_score'])/c

# Define dict to JSON object 
model_dict = {'Classifier': str(model),
'Kernel': str(kernel),
'Score': str(score),
'Number of folds in cross validation': str(c),
'Min score': str(min(sc['test_score'])),
'Max score': str(max(sc['test_score'])),
'Full score list': str(sc['test_score']),
'Avg train time': str(np.mean(sc['fit_time'])),
'Tot train time': str(sum(sc['fit_time'])),
'Full train time list': str(sc['fit_time']),
'Avg test time': str(np.mean(sc['score_time'])),
'Tot test time': str(sum(sc['score_time'])),
'Full test time list': str(sc['score_time']),
'Parameters used': str(params_used),
'Timestamp of training': str(datetime.now())
}
# Creates a JSON object and dumps it to a file in the working folder
with open('C:/xampp/htdocs/phpTest/pythonForServer/training_info.json', 'w') as json_file:
  json.dump(model_dict, json_file)
#print(model_json)
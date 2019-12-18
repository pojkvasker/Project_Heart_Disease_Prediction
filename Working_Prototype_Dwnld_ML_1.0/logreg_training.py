from sklearn.linear_model import LogisticRegression
import numpy as np
import pymysql
import joblib
from datetime import datetime

def InitTrain(db_data):
    # Import into separate vectors
    age = [i[0] for i in db_data]
    sex = [i[1] for i in db_data]
    cp = [i[2] for i in db_data]
    trestbps = [i[3] for i in db_data]
    chol = [i[4] for i in db_data]
    fbs = [i[5] for i in db_data]
    restecg = [i[6] for i in db_data]
    thalach = [i[7] for i in db_data]
    exang = [i[8] for i in db_data]
    oldpeak = [i[9] for i in db_data]
    slope = [i[10] for i in db_data]
    ca = [i[11] for i in db_data]
    thal = [i[12] for i in db_data]
    label = [i[13] for i in db_data]

    # make class label binary
    for i in range(0,len(label)):
        if(label[i]>1):
            label[i] = 1

    # Define x as training parameters, based on avaiable info
    x = np.transpose([age,sex,trestbps,chol,restecg,exang])
    # Define y as class label
    y = np.transpose([label])

    # Model of choice: logistic regression.
    model = LogisticRegression(random_state=0, )

    # Train a model on data.
    model.fit(x, y.ravel())

    #print(model.coef_)
    #print(model.intercept_)
    logregBias = model.intercept_[0]
    #print(logregBias)
    logregCoeff = model.coef_
    #print(logregCoeff[0][0])

    # Write a txt file that http_interface
    with open("ParametersLogReg.txt", "w") as text_file:
        print("{},".format(logregBias), "{},".format(logregCoeff[0][0]), "{},".format(logregCoeff[0][1]),  "{},".format(logregCoeff[0][2]),\
            "{},".format(logregCoeff[0][3]), "{},".format(logregCoeff[0][4]), "{}".format(logregCoeff[0][5]), file=text_file)

# Define MySQL connectivty
connection = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "",
    db = "pdp", # Name of database
)
#try:
# define the SQL commmands as a cursor
with connection.cursor() as cursor:
# Define columns in the database, both class label(s) and parameters
    sql = "SELECT `age`, `sex`, `cp`, `trestbps`, `chol`, `fbs`, `restecg`, `thalach`, `exang`, `oldpeak`, `slope`, `ca`, `thal`, `num` FROM `heart disease prediction`"
    #try:
    cursor.execute(sql)
    # Fetch db data locally
    db_data = cursor.fetchall()
    print("Data fetched from db.")
    InitTrain(db_data)
    #except:
    #    print("Did not work!")
    connection.commit()
#finally:
#    connection.close()

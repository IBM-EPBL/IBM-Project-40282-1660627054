import numpy as np
import pandas as pd

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

gmail_list=[]
password_list=[]
gmail_list1=[]
password_list=[]


from flask import Flask, request, jsonify, render_template

import joblib

# load the model from the file
model = joblib.load('final_pickle_model.pkl')

# use the loaded model to make predictions

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def register():
    int_features2 = [str(x) for x in request.form.values()]
    r1=int_features2[0]
    print(r1)
    
    r2=int_features2[1]
    print(r2)
    logu1=int_features2[0]
    passw1=int_features2[1]

# if int_features2[0]==12345 and int_features2[1]==12345
 
    import MySQLdb

# open database connection

    db =  MySQLdb.connect("localhost","root",'',"ddbb")

# prepare a cursor object using cursor() method
    
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()

    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list1.append(str(row1[0]))


    print(gmail_list1)
    if logu1 in gmail_list1:
        return render_template('register.html',text="This Username is Already in use")

    else:


# prepare SQL query to INSERT a record into the database
           sql = "INSERT INTO user_register(user,password) VALUES (%s,%s)"
           val = (r1, r2)

           try:
# execute the SQL command
                              cursor.execute(sql,val)
# commit your changes in the database
                              db.commit()
           except:
# rollback in case there is any error
                              db.rollback()

# disconnect from server
           db.close()
           return render_template('register.html',text="succesfully Registered")

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/logedin',methods=['POST'])
def logedin():

    int_features3 = [str(x) for x in request.form.values()]
    print(int_features3)
    logu=int_features3[0]
    passw=int_features3[1]


    import MySQLdb

# open database connection
    db = MySQLdb.connect("localhost","root","","ddbb")

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()

    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list.append(str(row1[0]))

    print(gmail_list)


    cursor1 = db.cursor()
    cursor1.execute("SELECT password FROM user_register")
    result2 = cursor1.fetchall()

    for row2 in result2:
                      print(row2)
                      print(row2[0])
                      password_list.append(str(row2[0]))

    print(password_list)
    print(gmail_list.index(logu))
    print(password_list.index(passw))

    if gmail_list.index(logu)==password_list.index(passw):
        return render_template('index.html')
    else:
        return render_template('login.html',text='Use Proper Username and Password')




@app.route('/production')
def production():
    return render_template('index.html')

@app.route('/production/predict',methods=['POST'])
def predict():
    '''
    for rendering results on HTML GUI
    '''
    int_features = [str(x) for x in request.form.values()]
    a=int_features


# intialise data of lists
    data = {'Age':[float(a[0])],'Gender':[float(a[1])],'Total_Bilirubin':[float(a[2])],'Direct_bilirubin':[float(a[3])],'Alkaline_Phosphotase':[float(a[4])],'Alamine_Aminotransferase':[float(a[5])],'Aspartate_Aminotransferase':[float(a[6])],'Total_Protiens':[float(a[7])],'Albumin':[float(a[8])],'Albumin_and_Globulin_Ratio':[float(a[9])]}



# create dataframe
    df = pd.DataFrame(data) 
    print(df)

    df

    prediction=model.predict_proba(df)
    print(prediction)
    output='{0:.{1}f}'.format(prediction[0][0], 2)

    if output<str(0.5):
        return render_template('index.html',prediction_text='percentage of occuring the Liver Disease is {:.2f}%'.format(float(output)*100),prediction_text1="your liver is healthy enough and no need to worry",prediction_text2="Consume healthy food with balanced diet and takecare")
     
    if output>str(0.5) and output<str(0.85):
        return render_template('index.html',prediction_text='percentage of occuring the Liver Disease is {:.2f}%'.format(float(output)*100),prediction_text1="you are in 2nd stage and consult the doctor and follow the instructions strictly",prediction_text2="Talking vitamins,Exercising,losing weight and medicines prescribed by your health care provider",prediction_text3="avoid consumption of food that affects the liver (like alcohol, Added sugar, fried foods, salt...)",prediction_text4="Avoid risly behaviour and get vaccinated")
     
    if output>str(0.85):
        return render_template('index.html',prediction_text='percentage of occuring the Liver Disease is {:.2f}%'.format(float(output)*100),prediction_text1="you are in last stage and consult the doctor immediately",prediction_text2="For acute (sudden) liver failure, treatment includes:",prediction_text3="1.intravenous (IV) fluids to maintain blood pressure",prediction_text4="2.medications such as laxatives or enemas to help flush toxins(poisons)out",prediction_text5="3.blood gulcose (sugar) monitoring-gulcose is given to the patient if blood sugar drops",prediction_text6="For chronic liver failure take treatments like liver transplant surgery")
     

if __name__ == "__main__":
    app.run(debug=False)











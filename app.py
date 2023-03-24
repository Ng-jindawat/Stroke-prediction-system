import numpy as np
import pandas as pd
from joblib import load
from sklearn.preprocessing import StandardScaler
import sqlite3
from flask import Flask,request, render_template

scaler = StandardScaler()
app = Flask('__name__')
model = load('model_nb.joblib') 
df = pd.read_csv('train_data.csv')
col = ['age','hypertension','avg_glucose_level','ever_married',
       'heart_disease','self_employed_job','bmi','formerly_smoked',]
df2 = df[col]
scaler = StandardScaler()
scaler.fit(df2)

@app.route('/')
def get_index():
  return render_template('index.html')

@app.route('/form-register')
def get_form():
  return render_template('form.html')
  
@app.route('/getPredict', methods=['GET', 'POST'])
def get_Predict():
  if request.method == 'POST':
    try:
      
      glucose = float(request.form['glucose']) #รับค่าจาก form 
      glucose = float("{:0.2f}".format(glucose)) #แปลงให้เป็นทศนิยม 2 ตำแหน่ง เพราะ dataset ที่ใช้สอนเป็น 2 ตำแหน่ง
     
      weight = float(request.form['weight']) #รับค่าจาก form
      height = float(request.form['height']) #รับค่าจาก form หน่วยที่รับมาเป็น CM
      height = float("{:0.2f}".format(height/100 ))                   #แปลงหน่ว CM เป็น M
      calcBMI = weight/(height*height)       #คำนวณค่า BMI
      bmi = float("{:0.1f}".format(calcBMI))  #แปลงให้เป็นทศนิยม 1 ตำแหน่ง เพราะ dataset ที่ใช้สอนเป็น 1 ตำแหน่ง
      
      age = float(request.form['age'])
      age = float("{:0.1f}".format(age))
      heart_disease = int(request.form['heart_disease'])
      hypertension = int(request.form['hypertension'])
      ever_married = int(request.form['ever_married'])
      work_type = int(request.form['work_type'])
      smoking_status = int(request.form['smoking_status'])
      general_data = connectDTB(1)
      if heart_disease == 1:
          heart_disease_text = "เป็นโรคหัวใจ"
          heart_disease_data = connectDTB(3)
      else :
          heart_disease_text = "ไม่เป็นโรคหัวใจ"
          heart_disease_data = " "
      if hypertension == 1:
          hypertension_text = "เป็นโรคความดันโลหิตสูง"
          hypertension_data = connectDTB(2)
      else :
          hypertension_text = "ไม่เป็นโรคความดันโลหิตสูง"
          hypertension_data = " "
      
      if ever_married == 0 :
        ever_married_text = 'เคยแต่งงานแล้ว'
      else:
        ever_married_text = 'ยังไม่เคยแต่งงาน'
          
      if smoking_status == 0 :
        smoking_status_ = 0
        smoking_status_text = 'สูบบุหรี่'
      elif smoking_status == 1 :
        smoking_status_ = 0
        smoking_status_text = 'ไม่สูบบุหรี่'
      else:
        smoking_status_ = 0
        smoking_status_text = 'เคยสูบบุหรี่'
        
      if work_type == 0 :
        work_type_ = 0
        work_type_text = 'อาชีพข้าราชการ'
      elif work_type == 1 :
        work_type_ = 0
        work_type_text = 'อาชีพลูกจ้าง'
      elif work_type == 2 :
        work_type_ = 1
        work_type_text = 'อาชีพอิสระ'
      elif work_type == 3 :
        work_type_ = 0
        work_type_text = 'อาชีพนักเรียน/นักศึกษา'
      else:
        work_type_ = 0
        work_type_text = 'ว่างงาน'
      
      if bmi < 18.5 :
        bmi_text = "ค่าดัชนีมวลกายต่ำกว่าเกณฑ์"
        bmi_data = connectDTB(4)
      elif bmi > 24.9 :
        bmi_text = "ค่าดัชนีมวลกายสูงกว่าเกณฑ์"
        bmi_data = connectDTB(5)
      else :
        bmi_text = "ค่าดัชนีมวลกายอยู่ในเกณฑ์ปกติ"
        bmi_data = " "
        
      if ((glucose>= 100) and (glucose<= 125)) :
        avg_glucose_text = "ค่าน้ำตาลในเลือดเสี่ยงเป็นเบาหวาน"
        avg_glucose_data = connectDTB(6)
      elif glucose > 125 :
        avg_glucose_text = "ค่าน้ำตาลในเลือดอาจเป็นเบาหวาน"
        avg_glucose_data = connectDTB(7)
      else :
        avg_glucose_text = "ค่าน้ำตาลในเลือดอยู่ในเกณฑ์ปกติ"
        avg_glucose_data = " "
    except:
         print("Error")
  
  data = [[age,hypertension,glucose,ever_married,heart_disease,work_type_,bmi,smoking_status_]]
  data = scaler.transform(data)
  predicted = model.predict(data)
  
  if predicted == 1:
      prediction_text= 1
  elif predicted == 0 :
      prediction_text= 0

  return render_template('result.html',
                         data = 1, 
                         prediction_text = prediction_text, 
                         prediction = predicted, 
                         heart_disease_text = heart_disease_text, 
                         hypertension_text = hypertension_text, 
                         ever_married_text = ever_married_text, 
                         smoking_status_text = smoking_status_text, 
                         work_type_text = work_type_text,
                         bmi_text = bmi_text,
                         avg_glucose_text = avg_glucose_text,
                         glucose = glucose, 
                         age = int(age),
                         weight_data = weight, 
                         height_data = height, 
                         bmi = bmi, 
                         general_data = general_data, 
                         hypertension_data = hypertension_data,
                         heart_disease_data = heart_disease_data, 
                         bmi_data = bmi_data, 
                         avg_glucose_data = avg_glucose_data)

def connectDTB(id):
  conn = sqlite3.connect('health_advice.db')
  cur = conn.cursor()
  cur.execute("SELECT name,description FROM recommend WHERE id = ?",(id,))
  rows = cur.fetchall()
  for row in rows :
    name = row[0]
    describetion = row[1]
    cur.close()
  return name,describetion 
  
@app.route('/information-about-stroke')
def get_about_knowledge():
  return render_template('knowledge.html')
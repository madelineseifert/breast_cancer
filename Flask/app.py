from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, render_template, url_for
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder, StandardScaler
from Neural_Net import X_scaler, label_encoder
import numpy as np
from numpy import array
import tensorflow as tf

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database/breast_cancer.sqlite'
app.debug = True
db = SQLAlchemy(app)
model = load_model("models/cancer_model_trained.h5")
graph = tf.get_default_graph()

class Patient(db.Model):
      id = db.Column(db.Integer, primary_key = True)
      radius_worst = db.Column(db.Float)
      concave_points_worst = db.Column(db.Float)
      area_worst = db.Column(db.Float)
      perimeter_worst = db.Column(db.Float)

      def __init__(self, radius_worst, concave_points_worst, area_worst,perimeter_worst):
            self.radius_worst = radius_worst
            self.concave_points_worst = concave_points_worst
            self.area_worst = area_worst
            self.perimeter_worst = perimeter_worst                        

      # def __repr__(self):
      #       return '<Test %r>' %  self.diagnosis


@app.route('/')
def index():
      return render_template('add_patient_data.html')


@app.route('/post_patient_data',methods =['GET', 'POST']) 
def post_patient_data():
      patient = Patient(request.form['radius_worst'],
                        request.form['concave_points_worst'],\
                        request.form['area_worst'],\
                        request.form['perimeter_worst']) 
      print(patient)              
      db.session.add(patient)
      db.session.commit()

      return redirect(url_for('index'))

@app.route('/predict', methods=['GET', 'POST'])
def predict_tumor():
      parameters = []
      parameters.append(float(request.form['radius_worst']))
      parameters.append(float(request.form['concave_points_worst']))
      parameters.append(float(request.form['area_worst']))
      parameters.append(float(request.form['perimeter_worst']))
      

      reshaped_patient = np.asarray(parameters).reshape(1, 4)

      print("test 1")
      patient_test_scaled = X_scaler.transform(reshaped_patient)
      print("test2")
      with graph.as_default():
            yhat = model.predict_classes(patient_test_scaled)
            print("test3")

      prediction_labels = label_encoder.inverse_transform(yhat)
                  #result = patient

      return render_template('prediction.html', result=prediction_labels)

@app.route('/see_data') 
def see_data():
      myPatient = Patient.query.all()
      return render_template('see_data.html' , myPatient = myPatient)     


if __name__ == '__main__':
   app.run(debug = True)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, render_template, url_for


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database/breast_cancer.sqlite'
app.debug = True
db = SQLAlchemy(app)


class Patient(db.Model):
      id = db.Column(db.Integer, primary_key = True)
      radius_worst = db.Column(db.Float)
      concave_points_worst = db.Column(db.Float)
      area_worst = db.Column(db.Float)
      perimeter_worst = db.Column(db.Float)

      def __init__(self,radius_worst,concave_points_worst,area_worst,perimeter_worst):
            self.radius_worst = radius_worst
            self.concave_points_worst = concave_points_worst
            self.area_worst = area_worst
            self.perimeter_worst = perimeter_worst                        

      # def __repr__(self):
      #       return '<Test %r>' %  self.diagnosis


@app.route('/')
def index():
      # myPatient = Patient.query.all()
      return render_template('add_patient_data.html')


@app.route('/post_patient_data',methods =['POST']) 
def post_patient_data():
      patient = Patient(request.form['radius_worst'],
                        request.form['concave_points_worst'],\
                        request.form['area_worst'],\
                        request.form['perimeter_worst'])   
      db.session.add(patient)
      db.session.commit() 
      return redirect(url_for('index'))


@app.route('/see_data') 
def see_data():
      myPatient = Patient.query.all()
      return render_template('see_data.html' , myPatient = myPatient)     


if __name__ == '__main__':
   app.run(debug = True)
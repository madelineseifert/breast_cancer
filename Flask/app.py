from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, render_template, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///breast_cancer.sqlite'
app.debug = True
db = SQLAlchemy(app)

class Patient(db.Model):
      id = db.Column(db.Integer, primary_key = True)
      radius_mean = db.Column(db.Integer)
      texture_mean = db.Column(db.Integer)

      def __init__(self,radius_mean,texture_mean):
            self.radius_mean = radius_mean
            self.texture_mean = texture_mean

      def __repr__(self):
            return '<Test %r>' %  self.diagnosis

@app.route('/')
def index():
   return render_template('add_patient_data.html')


@app.route('/post_patient_data',methods =['POST']) 
def post_patient_data():
      patient = Patient(request.form['radius_mean'],request.form['texture_mean'])   
      db.session.add(patient)
      db.session.commit() 
      return redirect(url_for('index'))

if __name__ == '__main__':
   app.run(debug = True)
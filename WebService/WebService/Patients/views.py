#################
#### imports ####
#################

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from ..models import User , Patient, Foundations,Patient_Informations, db
from WebService import app
from flask_wtf import Form
from wtforms import DateField, TextField
from datetime import date, datetime
from .forms import *

################
#### config ####
################

Patients_blueprint = Blueprint('Patients', __name__)


################
#### routes ####
################
#@app.route('/')
#@login_required
#def index():
#    all_patients = Patient.query.all()
#    return render_template('index.html', allpatients = all_patients)

@app.route('/patients')
@login_required
def get_patients():
    all_patients = Patient.query.all()
    return render_template('patients.html', allpatients = all_patients)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')



@app.route('/addpatient', methods=["GET", "POST"])
@login_required
def addpatient_post():
    if request.method == "POST":
        form = DateForm(request.form)
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        birthdate = request.form.get('dt')
        address = request.form.get('address')
        city = request.form.get('city')
        email = request.form.get('email')
        phone = request.form.get('phone')
        #permission = request.form.getlist('permission')
        if request.form.getlist('permission')[0] == 'on':
            permission = True
        else:
            permission = False

        patient = Patient.query.filter_by(email=email).first()

        if patient:
            error = "The patient already exists"
            return render_template('addpatient.html', form=form, error=error)
    
        datetime_object = datetime.strptime(birthdate,'%d-%m-%Y')
        birth = date(datetime_object.year, datetime_object.month, datetime_object.day)
        new_patient = Patient(first_name = firstname, last_name = lastname, birth_date = birth, address = address, city = city, email = email, phone = phone, access_permission = permission)
        db.session.add(new_patient)
        db.session.commit()

        return redirect(url_for('get_patients'))
    else:
        form = DateForm()
        check = False
        if 'id' in request.args:
            patient_id = request.args.get('id')
            patient = Patient.query.get(patient_id)
            form.firstname.data = patient.first_name
            form.lastname.data = patient.last_name
            form.address.data = patient.address
            form.city.data = patient.city
            form.email.data = patient.email
            form.phone.data = patient.phone
            form.dt.data = patient.birth_date
            check = patient.access_permission
        return render_template('addpatient.html', form=form, check=check)

@app.route('/deletepatient')
@login_required
def deletepatient():
    if 'id' in request.args:
        patient_id = request.args.get('id')
        patient = Patient.query.get(patient_id)
        db.session.delete(patient)
        db.session.commit()
    return redirect(url_for('get_patients'))


@app.route('/patientresults')
@login_required
def get_results():
    if request.method == "GET":
        if 'id' in request.args:
            patient_id = request.args.get('id')
            allresults = Patient_Informations.query.filter_by(patient_id=patient_id).all()
            return render_template('overview_results.html', allresults = allresults)
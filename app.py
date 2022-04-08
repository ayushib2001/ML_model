from flask import Flask, render_template,request
import numpy as np
import pickle

app = Flask(__name__)

rf_model = pickle.load(open("model.pkl", "rb"))

@app.route('/')
def home() :
    return render_template('index.html')


def convert(Location, Fuel_Type, Transmission) :
    Loc_Bangalore = 0 
    Loc_Chennai = 0
    Loc_Coimbatore = 0
    Loc_Delhi = 0
    Loc_Hyderabad = 0
    Loc_Jaipur = 0
    Loc_Kochi = 0
    Loc_Kolkata = 0
    Loc_Mumbai = 0
    Loc_Pune = 0
    Fuel_Diesel = 0
    Fuel_LPG = 0
    Fuel_Petrol = 0
    Transmission_Manual = 0 

    if Location != 'Ahembadabad' :
        loc = ('Loc_' + Location)
        vars()[loc] = 1
    if Fuel_Type != 'CNG' :
        fuel = ('Fuel_' + Fuel_Type)
        vars()[fuel] = 1
    if Transmission == 'Manual' :
        Transmission_Manual = 1

    return (Loc_Bangalore, Loc_Chennai ,Loc_Coimbatore, Loc_Delhi, Loc_Hyderabad, Loc_Jaipur, Loc_Kochi, Loc_Kolkata, Loc_Mumbai, Loc_Pune, Fuel_Diesel, Fuel_LPG, Fuel_Petrol, Transmission_Manual)

@app.route('/', methods = ['POST'])
def predict() :
    name = request.form['name']
    Year = request.form['year']
    Kilometers_Driven = float(request.form['km'])
    Owner_type = request.form['owner']
    Seats = request.form['seats']
    Mileage = float(request.form['mileage'])
    Engine = float(request.form['engine'])
    Power = float(request.form['power'])
    Location = request.form['location']
    Fuel_Type = request.form['fuel']
    Transmission = request.form['trans']

    Loc_Bangalore, Loc_Chennai ,Loc_Coimbatore, Loc_Delhi, Loc_Hyderabad, Loc_Jaipur, Loc_Kochi, Loc_Kolkata, Loc_Mumbai, Loc_Pune, Fuel_Diesel, Fuel_LPG, Fuel_Petrol, Transmission_Manual  = convert(Location, Fuel_Type,Transmission)

    test_data = np.array([[Year, Kilometers_Driven, Owner_type, Seats, Mileage, Engine, Power,Loc_Bangalore, Loc_Chennai ,
    Loc_Coimbatore, Loc_Delhi, Loc_Hyderabad, Loc_Jaipur, Loc_Kochi, Loc_Kolkata, Loc_Mumbai, Loc_Pune, Fuel_Diesel, Fuel_LPG, 
    Fuel_Petrol, Transmission_Manual]])

    pred = rf_model.predict(test_data)

    return render_template('predict.html', name = name, data = np.round(pred[0],2))


if __name__ == '__main__':
     app.run(debug=True)
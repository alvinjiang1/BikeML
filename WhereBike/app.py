from flask import Flask, jsonify, render_template, request, redirect, url_for
from joblib import load
import pandas as pd
from helper import user_generate_df
import helper

app = Flask(__name__)

# Load the trained model
model = load('rf.pkl')
# Load the No lag model:
no_lag_model = load('no_lag_rf.pkl')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        result_map = {}
        result_map["temperature"] = request.form['temperature']
        result_map["time"] = request.form['time']
        result_map["weather"] = request.form['weather']
        result_map["humidity"] = request.form['humidity']
        result_map["windspeed"] = request.form['windspeed']   
        result_map["date"] = request.form["dateField"]            
        print(result_map)
        # Call predictions
        return predict(result_map)
    
def predict(args):
    print(args)
    # Make predictions based on the data that was input   

    # Temperature: Normalize the temperature: (t-t_min)/(t_max-t_min), t_min=-8, t_max=+39 
    args["temperature"] = ((int(args["temperature"]) + 8) / (47))

    # Time: Getting the hour from the time
    args["time"] = int(args["time"][:2])

    # Weather: Obtain the numerical value for the weather    
    if args["weather"] == '':
        args["weather"] = helper.MODE_WEATHER
    else:
        args["weather"] = int(args["weather"][7])

    # Humidity: Normalize the temperature, The values are divided to 100 (max)
    if args["humidity"] == '':
        args["humidity"] = helper.MEAN_HUM
    else:
        args["humidity"] = int(args["humidity"]) / 100

    # Windspeed: Normalize the windspeed, The values are divided to 67 (max)
    if args["windspeed"] == '':
        args["windspeed"] = helper.MEAN_WINDSPEED
    else:
        args["windspeed"] = int(args["windspeed"]) / 67

    result = None
    isUser = True
    # Use model to perform predictions
    if isUser:
        # Preprocess input
        processed_df = user_generate_df(args)
        result = no_lag_model.predict(processed_df)
    else:
        result = model.predict(processed_df)
    assert result != None
    predicted_demand = round(result[0])
    return jsonify(prediction=predicted_demand)

    
@app.route('/vendor.html')
def vendor():
    return render_template('vendor.html')

@app.route('/user.html')
def user():
    return render_template('user.html')

@app.route('/testpath')
def testpath():
    return url_for('static', filename='images/home.jpg')

if __name__ == '__main__':
    app.run(debug=True)

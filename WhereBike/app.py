from flask import Flask, jsonify, render_template, request, redirect, url_for
from joblib import load
import pandas as pd
from WhereBike.helper import user_generate_df
import helper

app = Flask(__name__)

# Load the trained model
model = load('rf.pkl')

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
    # Make predictions based on the data that was input   

    # Temperature: Normalize the temperature: (t-t_min)/(t_max-t_min), t_min=-8, t_max=+39 
    args["temperature"] = ((int(args["temperature"]) + 8) / (47))

    # Time: Getting the hour from the time
    args["time"] = int(args["time"][:2])

    # Weather: Obtain the numerical value for the weather
    args["weather"] = int(args["weather"][7])

    # Humidity: Normalize the temperature, The values are divided to 100 (max)
    args["humidity"] = int(args["humidity"]) / 100

    # Windspeed: Normalize the windspeed, The values are divided to 67 (max)
    args["windspeed"] = int(args["windspeed"]) / 67

    # Perform pre-processing on input to allow it to match    
    processed_df = user_generate_df(args)

    # Use model to perform predictions
    result = model.predict(processed_df)

    return jsonify(prediction=12345)

def preprocess(df):
    raise NotImplementedError
    
@app.route('/vendor.html')
def vendor():
    return render_template('vendor.html')

@app.route('/user.html')
def user():
    return render_template('user.html')

if __name__ == '__main__':
    app.run(debug=True)

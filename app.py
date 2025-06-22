from flask import Flask , render_template , request 
from weather import get_weather_info
import random

import pickle
import numpy as np

# Loading the model for Fertilizer Prediction
with open("models/fertilizer.pkl","rb") as f:
    model = pickle.load(f)



api_key = "52d129c124aaa073f4208583f3299b19"

app = Flask(__name__)

Global_location = "Kolhapur"
Global_weather_data = None

def create_weather_data(data):
    temp = data['main']['temp']
    humidity  = data['main']['humidity']
    rain = data.get('rain',{}).get('6h',0)
    weather_data = [("Temperature",temp),("Humidity",humidity),("Rain",rain)]
    return weather_data

def generate_quotes():
    farming_quotes = [
    "You reap what you sow.",
    "The farmer has to be an optimist or he wouldn’t still be a farmer.",
    "Farming is a profession of hope.",
    "The ultimate goal of farming is not the growing of crops, but the cultivation and perfection of human beings.",
    "Agriculture is the foundation of civilization and any stable economy.",
    "The soil is the great connector of lives, the source and destination of all.",
    "Good farming is a partnership between the farmer and the land.",
    "Patience and hard work are the seeds of success.",
    "Nature does not hurry, yet everything is accomplished.",
    "The farmer is the only man in our economy who buys everything at retail, sells everything at wholesale, and pays the freight both ways.",
    "Farming looks mighty easy when your plow is a pencil and you're a thousand miles from the corn field.",
    "The love of farming is a seed that grows with every season.",
    "Every blade of grass has its angel that bends over it and whispers, 'Grow, grow.'",
    "The farmer plants the seeds of tomorrow with the sweat of today.",
    "In farming, as in life, the harvest comes to those who wait and work.",
]
    return random.choice(farming_quotes)

# Main Index page
@app.route("/")
def index():
    quote = generate_quotes()
    return render_template("index.html",quote=quote)


# Gives Weather information like
# Temperature
# Humidity
# Rain in last 6 hours

@app.route("/weather" , methods=['POST','GET'])
def weather_data():
    weather_data = None

    if request.method=='POST':
        location = request.form['location']
        data = get_weather_info(location,api_key)
        
        Global_location = location

        weather_data = create_weather_data(data)

        Global_weather_data = weather_data
        
        return render_template("weather.html" ,weather_data=weather_data)

    return render_template("weather.html",weather_data=weather_data)


def get_advice(weather_data):
    temp = weather_data[0][1]
    humi = weather_data[1][1]
    rain = weather_data[2][1]

    advice = []
    # Temp based advice
    if temp<10:
          advice.append("Protect seedlings from cold; avoid sowing heat-loving crops.")
    elif temp > 10 and temp < 20:
          advice.append("Good for cool-season crops (wheat, peas, lettuce). Monitor for frost.")
    elif temp > 20 and temp < 30:
          advice.append("Ideal for most crops (rice, maize, soybeans). Maintain irrigation.")
    else :
          advice.append('Watch for heat stress. Increase irrigation. Shade young plants if possible.')

    # Humidity based
    if humi < 40 :
        advice.append("Dry conditions—risk of wilting. Mulch soil to retain moisture.")
    elif humi<70 and humi>40:
        advice.append("Ideal for most crop growth. Monitor pest/disease levels.")
    else:
        advice.append("High humidity increases fungal/pest risk. Apply preventive fungicides.")

    # Rain fall based advice
    if rain == 0:
        advice.append("Consider irrigation. Check soil moisture.")
    elif rain < 10 and rain >0 :
        advice.append("Light rain—useful but might not reach deep roots.")
    elif rain < 30 and rain > 10:
        advice.append("Moderate rain—sufficient moisture. Delay irrigation.")
    else:
        advice.append("Heavy rain—watch for waterlogging. Ensure drainage is working.")

    return " ".join(advice)



# Gives Weather based advice
@app.route("/advice",methods=["POST","GET"])
def advice():

    location = None
    advice = None
    weather_data = None

    if request.method=='POST':
        location = request.form['location']
        data = get_weather_info(location,api_key)
        weather_data = create_weather_data(data)

        advice = get_advice(weather_data)
 
        return render_template("advice.html",location=location ,weather_data=weather_data, advice=advice)

    return render_template("advice.html",location=location ,weather_data=weather_data, advice=advice)



#### Fertilizer Prediction

@app.route("/fertilizer" , methods=["POST","GET"])
def fertilizer():
    if request.method == "POST":
        crop = int(request.form["crop"])
        soil = int(request.form["soil"])
        #weather data
        weather_data = get_weather_info(Global_location,api_key)
        temp = weather_data['main']['temp']
        humid  = weather_data['main']['humidity']

        data = [temp, humid, soil , crop]

        n_data = np.array(data)

        prediction = model.predict([data])

        return render_template("fertilizer.html",prediction=prediction[0] , data=data)


    return render_template("fertilizer.html")



if __name__ == '__main__':
    app.run(debug=True)
    

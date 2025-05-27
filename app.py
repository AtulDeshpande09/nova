from flask import Flask , render_template , request
from weather import get_weather_info



api_key = "52d129c124aaa073f4208583f3299b19"

app = Flask(__name__)

Global_location = None
Global_weather_data = None

def create_weather_data(data):
    temp = data['main']['temp']
    humidity  = data['main']['humidity']
    rain = data.get('rain',{}).get('6h',0)
    weather_data = [("Temperature",temp),("Humidity",humidity),("Rain",rain)]
    return weather_data



# Main Index page
@app.route("/")
def index():
    return render_template("index.html")


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
    return "You Reap what you Sow!!!"

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


@app.route("/fertilizer" , methods=["POST","GET"])
def fertilizer():
    return render_template("fertilizer.html")



@app.route("/test",methods=["POST","GET"])
def test():
    city=None
    if request.method == "POST":
        city = request.form['city']

        return render_template("test.html",city=city)
    return render_template('test.html',city=city)

if __name__ == '__main__':
    app.run(debug=True)
    

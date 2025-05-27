from flask import Flask , render_template , request
from weather import get_weather_info



api_key = "52d129c124aaa073f4208583f3299b19"

app = Flask(__name__)

Global_location = None
Global_weather_data = None

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
        
        temp = data['main']['temp']
        humidity  = data['main']['humidity']
        rain = data.get('rain',{}).get('6h',0)

        Global_location = location

        weather_data = [("Temperature",temp),("Humidity",humidity),("Rain",rain)]
        Global_weather_data = weather_data
        return render_template("weather.html" ,weather_data=weather_data)

    return render_template("weather.html",weather_data=weather_data)


# Gives weather Based Advices
@app.route("/advice",methods=['POST','GET'])
def advice():
    advice = None
    if Global_location:
        advice = "This is some advice"
        return render_template("advice.html",advice=advice)
    
    location = None
    return render_template('advice.html',advice=advice , location=location)


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
    

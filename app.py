from flask import Flask , render_template , request
from weather import get_weather_info



api_key = "52d129c124aaa073f4208583f3299b19"

app = Flask(__name__)



@app.route("/")
def index():
    render_template("index.html")


@app.route("/weather" , methods=['POST','GET'])
def weather_data():
    weather_data = None
    if request.method=='POST':
        print("IF statement")
        location = request.form['location']
        data = get_weather_info(location,api_key)
        
        temp = data['main']['temp']
        humidity  = data['main']['humidity']
        rain = data.get('rain',{}).get('6h',0)


        weather_data = [("Temperature",temp),("Humidity",humidity),("Rain",rain)]
        print(weather_data)
        return render_template("weather.html" ,weather_data=weather_data)

    return render_template("weather.html",weather_data=weather_data)

@app.route("/test",methods=["POST","GET"])
def test():
    city=None
    if request.method == "POST":
        city = request.form['city']

        return render_template("test.html",city=city)
    return render_template('test.html',city=city)

if __name__ == '__main__':
    app.run(debug=True)
    

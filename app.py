from flask import Flask , request , make_response
import os, json
import pyowm
from flask_cors import CORS, cross_origin

app = Flask(__name__)

owmapikey='b352ddd4315c9e1155883455cda02694'
owm=pyowm.OWM(owmapikey)       # create obj for class OWM

@app.route('/webhook',methods=['POST'])            # convention that dialogflow uses for routname
@cross_origin()
def webhook():
    req=request.get_json(silent=True , force=True)     # request get from dialogflow
    print("Request: ")
    print(json.dumps(req))
    res=processRequest(req)

    res=json.dumps(res)
    print("Response : ")
    print(res)
    r=make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r




def processRequest(req):
  result=req.get("queryResult")
  parameters=result.get("parameters")
  city=parameters.get("cityName")

  observation=owm.weather_at_place(city)
  w=observation.get_weather()
  latlon_res=observation.get_location()
  lat=str(latlon_res.get_lat())
  lon=str(latlon_res.get_lon())

  wind_res=w.get_wind()
  wind_speed=str(wind_res.get('speed'))

  humidity=str(w.get_humidity())
  status = str(w.get_detailed_status())

  celsius_result=w.get_temperature('celsius')
  temp_min_celsius=str(celsius_result.get('temp_min'))
  temp_max_celsius = str(celsius_result.get('temp_max'))

  speech = "Today weather in " + city + " \nstatus : " + status + "\n" + "Humidity : " + humidity + "\nTempreature : " + temp_max_celsius + " celsius"
  return {
      "fulfillmentText" : speech,           # cause result is shown in dialogflow in fulfillment parameter
      "displayText" : speech
  }


if __name__=='__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" %port)
    app.run(debug=False , port=port)
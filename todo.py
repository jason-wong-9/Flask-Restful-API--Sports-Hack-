from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

import numpy as np
import pandas as pd
import patsy
import time
import json
from scipy.spatial import distance
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


app = Flask(__name__)
api = Api(app)


class ID(Resource):
    def get(self, height, weight, city, state):
        # combined = pd.read_csv("wonderfullyamazingdata.csv", encoding='ISO-8859-1')
        combined = pd.read_csv("newamazingdata.csv", encoding='ISO-8859-1')
        location =  str(city) + ' ' + str(state)
        geolocator = Nominatim()
        place = geolocator.geocode(location[0])
        latitude = place.latitude
        longitude = place.longitude


        users = [float(height), float(weight), latitude, longitude ]
        players = combined[["height", "weight", "latitude", "longitude"]]

        result = []
        for index in range(0,len(players)):

            result.append(1-distance.cosine(users, players.iloc[index]))

        result = sorted(range(len(result)), key=lambda i: result[i])[-5:]   
        result.reverse()

        ids = []
        for index in result:
            ids.append( combined.ID.iloc[index] )


        ids = str(ids)


        with open('reply.json', 'w') as outfile:
            json_stuff = json.dumps(ids)
            json.dump(json_stuff, outfile)

        return json_stuff


##
## Actually setup the Api resource routing here
##
# api.add_resource(TodoList, '/todos')
# api.add_resource(Todo, '/todos/<string:todo_id>')
api.add_resource(ID, '/height/<string:height>/weight/<string:weight>/city/<string:city>/state/<string:state>');


if __name__ == '__main__':
    app.run(debug=True)

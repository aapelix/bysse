import base64
import requests
from requests.models import Response
import gtfs_realtime_pb2
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

@app.route("/positions", methods=["GET"])
def position():

    username = '2024144504049313'
    password = 'HDrxOQyyNMKSQuuVw2vrU1ImJGQJdCAe'
    url = 'https://data.waltti.fi/tampere/api/gtfsrealtime/v1.0/feed/vehicleposition'

    response = requests.get(url, auth=(username, password))

    if response.status_code == 200:

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)

        message = []

        for entity in feed.entity:
            em = {}
            if entity.HasField('vehicle'):
                    vehicle = entity.vehicle
                    # f.write(f"Vehicle position for vehicle ID: {vehicle.vehicle.id}, label: {vehicle.vehicle.label}, license plate: {vehicle.vehicle.license_plate} \n")

                    em["vehicle_id"] = vehicle.vehicle.id
                    em["sign_label"] = vehicle.vehicle.label
                    em["license_plate"] = vehicle.vehicle.license_plate

                    pos = vehicle.position

                    if vehicle.position.HasField('latitude') and vehicle.position.HasField('longitude'):

                            # f.write(f"  Latitude: {vehicle.position.latitude}" + "\n")
                            # f.write(f"  Longitude: {vehicle.position.longitude}" + "\n")

                        em["lat"] = pos.latitude
                        em["lon"] = pos.longitude
                    if vehicle.position.HasField('speed'):
                            # f.write(f"  Speed: {vehicle.position.speed}" + "\n")
                        em["speed"] = pos.speed
                    if vehicle.position.HasField('bearing'):
                            # f.write(f"  Bearing: {vehicle.position.bearing}" + "\n")
                        em["bearing"] = pos.bearing
                    if vehicle.HasField('trip'):
                        trip = vehicle.trip

                            # f.write(f"  Trip ID: {trip.trip_id}" + "\n")
                            # f.write(f"  Route ID: {trip.route_id}" + "\n")
                            # f.write(f"  Start Time: {trip.start_time}" + "\n")
                            # f.write(f"  Start Date: {trip.start_date}" + "\n")

                        em["trip_id"] = trip.trip_id
                        em["route_id"] = trip.route_id
                        em["start_time"] = trip.start_time
                        em["start_date"] = trip.start_date

                        em["current_stop_sequence"] = vehicle.current_stop_sequence
                        em["stop_id"] = vehicle.stop_id
                        em["current_status"] = vehicle.current_status
            message.append(em)

        return jsonify(message)
    else:
        print(f"Failed to fetch data. HTTP status code: {response.status_code}")
        return jsonify({"message": f"Failed to fetch data. HTTP status code: {response.status_code}"})


if __name__ == '__main__':
    app.run(debug=True)

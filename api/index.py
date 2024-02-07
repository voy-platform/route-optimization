from flask import Flask, request, jsonify
from RoutesGenerator import RoutesGenerator

app = Flask(__name__)


@app.route("/api/optimize-route", methods=["POST"])
def optimize_route():
    data = request.json
    try:
        dc = data.get("dc")
        stops = data.get("stops")
        num_of_vehicles = data.get("num_of_vehicles", 1)
        max_stops_per_vehicle = data.get("max_stops_per_vehicle", 10)

        routes_generator = RoutesGenerator(
            dc,
            stops,
            num_of_vehicles=num_of_vehicles,
            max_stops_per_vehicle=max_stops_per_vehicle,
        )
        routes = routes_generator.generate_routes()

        return jsonify(
            {
                "message": "Route optimization processed successfully.",
                "routes": routes,
            }
        )
    except Exception as e:
        return jsonify({"message": "Server error", "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

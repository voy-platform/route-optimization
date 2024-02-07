import json
from RoutesGenerator import RoutesGenerator


def lambda_handler(event, context):
    # Initialize the response object
    responseObject = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": "",
    }

    try:
        # Assuming the event body is a JSON string, parse it into a dictionary
        body = json.loads(event.get("body", "{}"))

        # Extract parameters directly from the body
        transactionId = body.get("transactionId")
        transactionType = body.get("type")
        transactionAmount = body.get("amount")
        dc = body.get("dc")
        stops = body.get("stops")
        num_of_vehicles = body.get("num_of_vehicles", 1)  # Example default value
        max_stops_per_vehicle = body.get(
            "max_stops_per_vehicle", 10
        )  # Example default value

        # Check if essential parameters are available
        if not all([transactionId, transactionType, transactionAmount, dc, stops]):
            responseObject["statusCode"] = 400
            responseObject["body"] = json.dumps(
                {"message": "Missing required parameters"}
            )
            return responseObject

        # Initialize RoutesGenerator with the provided parameters
        routes_generator = RoutesGenerator(
            dc,
            stops,
            num_of_vehicles=num_of_vehicles,
            max_stops_per_vehicle=max_stops_per_vehicle,
        )
        routes = routes_generator.generate_routes()

        # Prepare the successful response including the generated routes
        responseObject["body"] = json.dumps(
            {
                "transactionId": transactionId,
                "transactionType": transactionType,
                "transactionAmount": transactionAmount,
                "message": "hello from lambda",
                "routes": routes,
            }
        )

    except Exception as e:
        # Handle any exceptions that occur during processing
        responseObject["statusCode"] = 500
        responseObject["body"] = json.dumps(
            {"message": "Server error", "error": str(e)}
        )

    return responseObject

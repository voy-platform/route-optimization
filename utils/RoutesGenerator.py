from geopy import distance
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


class RoutesGenerator:
    def __init__(self, dc, stops, num_of_vehicles, max_stops_per_vehicle):
        self.dc = dc
        self.stops = stops
        self.num_of_vehicles = num_of_vehicles
        self.max_stops_per_vehicle = max_stops_per_vehicle

    def _geopy_distance(self, point1, point2):
        return distance.distance(point1, point2).miles

    def _create_distance_matrix(self):
        # Initialize the distance matrix with zeros
        num_stops = len(self.stops)
        distance_matrix = [[0] * (num_stops + 1) for _ in range(num_stops + 1)]

        # Calculate distances from DC to each stop and between stops
        for i, stop_i in enumerate([self.dc] + self.stops):
            for j, stop_j in enumerate([self.dc] + self.stops):
                if i != j:
                    distance_matrix[i][j] = self._geopy_distance(
                        stop_i["coordinates"], stop_j["coordinates"]
                    )
        return distance_matrix

    def create_data_model(self):
        """Stores the data for the problem."""
        data = {}
        data["distance_matrix"] = self._create_distance_matrix()
        data["demands"] = [0] + [1] * len(self.stops)
        data["vehicle_capacities"] = [self.max_stops_per_vehicle] * self.num_of_vehicles
        data["num_vehicles"] = self.num_of_vehicles
        data["depot"] = 0
        return data

    def print_solution(self, data, manager, routing, assignment):
        """Prints assignment on console."""
        print(f"Objective: {assignment.ObjectiveValue()}")
        routes = {
            "routes": [],
            "dropped_stops": [],
            "total_distance": 0,
            "total_stops": 0,
        }

        # Display dropped nodes.
        dropped_nodes = "Dropped nodes:"
        dropped_stops = []
        for node in range(routing.Size()):
            if routing.IsStart(node) or routing.IsEnd(node):
                continue
            if assignment.Value(routing.NextVar(node)) == node:
                dropped_nodes += f" {manager.IndexToNode(node)}"
                dropped_stops.append(self.stops[manager.IndexToNode(node) - 1])
        print(dropped_nodes)

        # Display routes
        total_distance = 0
        total_load = 0
        for vehicle_id in range(data["num_vehicles"]):
            index = routing.Start(vehicle_id)
            route = {
                "stopIds": [],
                "distance": 0,
                "num_stops": 0,
            }

            plan_output = f"Route for vehicle {vehicle_id}:\n"
            route_distance = 0
            route_load = 0
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                if node_index != 0:
                    route["stopIds"].append(self.stops[node_index - 1])
                route_load += data["demands"][node_index]
                plan_output += f" {node_index} Load({route_load}) -> "
                previous_index = index
                index = assignment.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id
                )
            plan_output += f" {manager.IndexToNode(index)} Load({route_load})\n"
            plan_output += f"Distance of the route: {route_distance}m\n"
            plan_output += f"Load of the route: {route_load}\n"
            route["distance"] = route_distance
            route["num_stops"] = route_load
            print(plan_output)
            routes["routes"].append(route)
            total_distance += route_distance
            total_load += route_load
        print(f"Total Distance of all routes: {total_distance}m")
        print(f"Total Load of all routes: {total_load}")
        routes["dropped_stops"] = dropped_stops
        routes["total_distance"] = total_distance
        routes["total_stops"] = total_load
        return routes

    def generate_routes(self):
        """Entry point of the program."""
        # Instantiate the data problem.
        data = self.create_data_model()

        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(
            len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
        )
        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

        # Create and register a transit callback.
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data["distance_matrix"][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Add Capacity constraint.
        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            return data["demands"][from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            data["vehicle_capacities"],  # vehicle maximum capacities
            True,  # start cumul to zero
            "Capacity",
        )
        # Allow to drop nodes.
        penalty = 1000
        for node in range(1, len(data["distance_matrix"])):
            routing.AddDisjunction([manager.NodeToIndex(node)], penalty)

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.time_limit.FromSeconds(1)

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if solution:
            return self.print_solution(data, manager, routing, solution)



# {
#     "rewrites": [
#         { "source": "/(.*)", "destination": "/api/index" }
#     ]
# }
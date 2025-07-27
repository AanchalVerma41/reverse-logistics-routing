import pandas as pd
import matplotlib.pyplot as plt
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from plot_utils import plot_routes

def create_data_model(filename):
    df = pd.read_csv(filename)
    print(f"✅ CSV Columns: {list(df.columns)}")

    locations = list(zip(df['X_coord'], df['Y_coord']))
    demands = list(df['Delivery_Demand'])
    pickups = list(df['Pickup_Demand'])

    data = {
        'locations': locations,
        'num_vehicles': 3,
        'depot': 0,
        'demands': demands,
        'pickups': pickups
    }
    return data

def compute_euclidean_distance_matrix(locations):
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                distances[from_counter][to_counter] = int(
                    ((from_node[0] - to_node[0]) ** 2 + (from_node[1] - to_node[1]) ** 2) ** 0.5)
    return distances

def main():
    filename = 'vrp_20_Customers_.csv'  # Change filename for 15/20 customer sets
    data = create_data_model(filename)
    distance_matrix = compute_euclidean_distance_matrix(data['locations'])

    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Set search parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    # Solve
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print("✅ Solution found!")
        routes = []
        total_distance = 0
        for vehicle_id in range(data['num_vehicles']):
            index = routing.Start(vehicle_id)
            route = []
            route_distance = 0
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                route.append(node_index)
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
            route.append(manager.IndexToNode(index))
            print(f"🚚 Route for vehicle {vehicle_id}: {route} | Distance: {route_distance}")
            routes.append(route)
            total_distance += route_distance
        print(f"🌟 Total distance of all routes: {total_distance}")

        # 📊 Plot routes
        from plot_utils import plot_routes

# At the end of main(), after printing the solution
        plot_routes(data['locations'], routes, data['depot'])

    else:
        print("❌ No solution found.")

if __name__ == '__main__':
    main()

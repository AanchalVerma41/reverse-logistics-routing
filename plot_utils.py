import matplotlib.pyplot as plt

def plot_routes(locations, routes, depot):
    plt.figure(figsize=(10, 6))
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

    # Plot depot
    depot_x, depot_y = locations[depot]
    plt.plot(depot_x, depot_y, 'ks', markersize=10, label='Depot')

    for i, route in enumerate(routes):
        if len(route) > 1:
            route_x = [locations[node][0] for node in route]
            route_y = [locations[node][1] for node in route]
            plt.plot(route_x, route_y, marker='o', color=colors[i % len(colors)], label=f'Vehicle {i}')

    plt.title('Vehicle Routing Problem Solution')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


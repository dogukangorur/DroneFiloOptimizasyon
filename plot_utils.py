import matplotlib.pyplot as plt
import matplotlib.patches as patches
from a_star_solver import a_star_search

def plot_routes(drones, deliveries, assignments, nodes_map, nfzs, adj_list):
    fig, ax = plt.subplots(figsize=(10, 10))

    for nfz in nfzs:
        polygon = patches.Polygon(nfz.coordinates, closed=True, edgecolor='red', facecolor='salmon', alpha=0.4)
        ax.add_patch(polygon)
        centroid = tuple(map(lambda x: sum(x)/len(x), zip(*nfz.coordinates)))
        ax.text(*centroid, f"NFZ {nfz.zone_id}", fontsize=8, color='red')

    for drone in drones:
        x, y = drone.start_pos
        ax.plot(x, y, 'bo', markersize=10)
        ax.text(x+5, y+5, f"D{drone.drone_id}", fontsize=8)

    for delivery in deliveries:
        x, y = delivery.location
        ax.plot(x, y, 'gs', markersize=6)
        ax.text(x+5, y+5, f"T{delivery.point_id}", fontsize=8)

    for delivery_id, drone_id in assignments.items():
        drone_node = f"D{drone_id}_START"
        delivery_node = str(delivery_id)
        path, _ = a_star_search(adj_list, nodes_map, nfzs, drone_node, delivery_node)
        if path:
            coords = [nodes_map[node]["coords"] for node in path]
            xs, ys = zip(*coords)
            ax.plot(xs, ys, linestyle='--', linewidth=1.2, alpha=0.7)

    ax.set_title("Drone Teslimat Rotaları")
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1000)
    ax.set_aspect('equal')
    plt.grid(True)
    plt.tight_layout()
    plt.show()